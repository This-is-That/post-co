from flask import Flask, request, jsonify, render_template
from CLIP import CLIP
from googletrans import Translator
import mysql.connector
import os

app = Flask(__name__)
clip = CLIP()
translator = Translator()

def process_embedding(embedding, cursor):
    # 커서 객체 생성
    try:
        # 'images_main' 테이블에서 상위 3개의 'image_url' 값 선택
        cursor.execute("SELECT image_url FROM images_main LIMIT 3")
        
        # 결과를 리스트로 저장
        image_urls = [row[0] for row in cursor.fetchall()]

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # 리소스 정리
        cursor.close()
        # db_connection.close()

    return image_urls

def translate_text(text, src='ko', dest='en'):
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text

def allowed_file(filename):
    # Check if the file is an allowed type (e.g., .jpg, .png)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

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
                embedding = clip.extract_image_embedding(image_file)
            else:
                return jsonify({'error': 'No valid image file provided'}), 400
        elif request.content_type == 'application/json':
            if 'text' in request.json:
                text = request.json['text']
                translated_text = translate_text(text)
                embedding = clip.extract_text_embedding(translated_text)
            else:
                return jsonify({'error': 'No valid JSON data provided'}), 400
        else:
            return jsonify({'error': 'No valid input provided'}), 400

        image_links = process_embedding(embedding, cursor)
        return jsonify({'image_links': image_links, 'embedding': embedding.cpu().tolist()})
    
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