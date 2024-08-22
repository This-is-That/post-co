from flask import Flask, request, jsonify, render_template
from CLIP import CLIP
from googletrans import Translator
import mysql.connector
import os
from FAISS import load_faiss_index, find_similar_images, get_image_urls_from_db
from PIL import Image
import io

app = Flask(__name__)
clip = CLIP()
translator = Translator()
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

def translate_text(text, src='ko', dest='en'):
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text

def allowed_file(filename):
    # 파일이 허용된 유형인지 확인 (예: .jpg, .png, .gif)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/')
def index():
    # Render the index.html template from the templates folder
    return render_template('index.html')

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
                translated_text = translate_text(text)
                embedding = clip.extract_text_embedding(translated_text)
            else:
                return jsonify({'error': '유효한 JSON 데이터가 제공되지 않았습니다'}), 400
        else:
            return jsonify({'error': '유효한 입력이 제공되지 않았습니다'}), 400

        image_id_url, distances = process_embedding(embedding, db_connection, cursor)
        # print(image_id_url)
        return jsonify({'image_links': list(image_id_url.values()), 'embedding': embedding.cpu().tolist()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        db_connection.close()

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

if __name__ == '__main__':
    app.run(debug=True)