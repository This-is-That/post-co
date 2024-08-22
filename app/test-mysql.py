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
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        
        # 각 테이블의 컬럼 명 가져오기
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]  # 컬럼 명 리스트 생성
        
        # 각 테이블의 총 데이터 개수 가져오기
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        # 각 테이블의 상위 5개 값 가져오기
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 6")
        rows = cursor.fetchall()
        
        # 결과 출력
        print(f"Table: {table_name}, Columns: {column_names}, Total Count: {count}, Top 6 Rows: {rows}")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # 리소스 정리
    cursor.close()
    db_connection.close()