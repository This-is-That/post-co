import mysql.connector
import os

# MySQL 데이터베이스에 연결
db_connection = mysql.connector.connect(
    host=os.environ['KOPIS_DB_HOST'],       # MySQL 서버 호스트명 (로컬에서 실행 중이라면 "localhost")
    user=os.environ['KOPIS_DB_USER'],   # MySQL 사용자 이름
    password=os.environ['KOPIS_DB_PASSWORD'], # MySQL 비밀번호
    database=os.environ['KOPIS_DB_DATABASE']  # 연결할 데이터베이스 이름
)

# 커서 객체 생성
cursor = db_connection.cursor()

try:
    # 'images_main' 테이블에서 상위 3개의 'image_url' 값 선택
    cursor.execute("SELECT image_url FROM images_main LIMIT 3")
    
    # 결과를 리스트로 저장
    image_urls = [row[0] for row in cursor.fetchall()]

    # 리스트 출력
    print("Image URLs:", image_urls)

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # 리소스 정리
    cursor.close()
    db_connection.close()