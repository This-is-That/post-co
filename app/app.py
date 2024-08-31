from flask import Flask, request, jsonify, render_template
from CLIP import CLIP
import mysql.connector
import os
from FAISS import load_faiss_index, find_similar_images, get_image_urls_from_db
from PIL import Image
import io
from datetime import date
from API import translate, generate_image
from openai import OpenAI
from transformers import pipeline

app = Flask(__name__)
clip = CLIP()
client = OpenAI()
pipe = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning", device=-1)
faiss_index = load_faiss_index("app/data/faiss_indices/faiss_index.bin")

def convert_gif_to_png(gif_file):
    with Image.open(gif_file) as img:
        img = img.convert('RGB')  # 필요에 따라 RGB로 변환
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

def process_embedding(embedding, db_connection, cursor):
    try:
        similar_image_ids, distances = find_similar_images(embedding, faiss_index, top_n=6)
        
        image_urls = get_image_urls_from_db(similar_image_ids, db_connection, cursor)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return image_urls, distances

def allowed_file(filename):
    # 파일이 허용된 유형인지 확인 (예: .jpg, .png, .gif)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

def get_info(image_ids, cursor):
    try:
        # Convert image_ids to a format suitable for SQL IN clause
        ids_placeholder = ', '.join(['%s'] * len(image_ids))

        # SQL query to fetch the required information
        query = f"SELECT ID, image_id, start_date, end_date, place_name, actor, runtime, age FROM images_info WHERE ID IN ({ids_placeholder})"
        
        # Execute the query with the image_ids as parameters
        cursor.execute(query, image_ids)
        
        # Fetch all the results
        results = cursor.fetchall()
        
        # Process results into a list of dictionaries
        image_info = []
        for row in results:
            info = {'ID': row[0], 'image_id': row[1],
                    'start_date': str(row[2].isoformat()) if isinstance(row[2], date) else row[2],
                    'end_date': str(row[3].isoformat()) if isinstance(row[3], date) else row[3],
                    'place_name': row[4], 'actor': row[5], 'runtime': row[6], 'age': row[7]}
            image_info.append(info)
        
    except Exception as e:
        print(f"An error occurred while fetching image info: {e}")
        image_info = []

    return image_info

@app.route('/')
def index():
    # Render the index.html template from the templates folder
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/process', methods=['POST'])
def process_input():
    db_connection = mysql.connector.connect(
        host=os.environ['KOPIS_DB_HOST'],       # MySQL 서버 호스트명
        user=os.environ['KOPIS_DB_USER'],   # MySQL 사용자 이름
        password=os.environ['KOPIS_DB_PASSWORD'], # MySQL 비밀번호
        database=os.environ['KOPIS_DB_DATABASE']  # 연결할 데이터베이스 이름
    )
    cursor = db_connection.cursor()

    try:
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                if image_file.filename.lower().endswith('gif'):
                    image_file = convert_gif_to_png(image_file)
                embedding = clip.extract_image_embedding(image_file)
            else:
                return jsonify({'error': '유효한 이미지 파일이 제공되지 않았습니다'}), 400
        elif request.content_type == 'application/json':
            if 'text' in request.json:
                text = request.json['text']
                translated_text = translate(text)
                embedding = clip.extract_text_embedding(translated_text)
            else:
                return jsonify({'error': '유효한 JSON 데이터가 제공되지 않았습니다'}), 400
        else:
            return jsonify({'error': '유효한 입력이 제공되지 않았습니다'}), 400

        image_id_url, distances = process_embedding(embedding, db_connection, cursor)
        distances = distances.tolist()
        image_info = get_info(list(image_id_url.keys()), cursor)
        return jsonify({'image_ids': list(image_id_url.keys()), 'image_links': list(image_id_url.values()), 'image_info': image_info})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        db_connection.close()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()  # JSON 형식으로 데이터를 받아옵니다.
    selected_item = None
    
    # 'prompt'와 'selectedItems'가 POST 데이터에 포함되어 있는지 확인합니다.
    if 'prompt' in data and isinstance(data['prompt'], str):
        prompt = data['prompt'] # str 타입, prompt 반환
        selected_item = data['selectedItem'] # str 타입, 포스터 url 반환
        
        img_url = generate_image(pipe, client, prompt, img_url=selected_item)
        
        return jsonify({'gen_image_urls': [img_url]}), 200  # 성공 메시지 반환
        
    else:
        return jsonify({'error': 'Invalid input'}), 400  # 에러 메시지 반환

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

if __name__ == '__main__':
    app.run(debug=True)