import faiss
import numpy as np
import mysql.connector
import os
from tqdm.auto import tqdm
import json
import re

# 데이터베이스에서 특징 벡터와 이미지 ID를 가져오는 함수
def get_feature_vectors_and_ids_from_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT ID, feature_vector FROM images_features") 

    vectors = []
    ids = []

    for row in tqdm(cursor.fetchall()):
        image_id, vector_json = row
        
        # feature_vector가 None인 경우 건너뛰기
        if vector_json is None:
            continue
        
        try:
            vector = json.loads(vector_json)  # JSON 문자열을 리스트로 변환
            vector = np.array(vector, dtype=np.float32)  # numpy 배열로 변환
        except (json.JSONDecodeError, ValueError):
            print(f"Error decoding or converting JSON for image ID: {image_id}")
            continue
        
        # 문자열 ID에서 PF를 제거하고 정수로 변환
        numeric_id = int(re.sub(r'[^0-9]', '', image_id))  # 숫자만 추출
        
        vectors.append(vector)
        ids.append(numeric_id)  # 숫자 ID를 저장
    
    vectors = np.array(vectors, dtype=np.float32)  # Numpy 배열로 변환
    
    cursor.close()
    db_connection.close()
    
    return ids, vectors

# FAISS 인덱스 생성 및 학습
def build_faiss_index(vectors, ids):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension) # IndexFlatL2 대신에 IndexFlatIP
    faiss.normalize_L2(vectors) # vector를 add하기 전에 normalize_L2
    id_index = faiss.IndexIDMap2(index)   # ID와 벡터를 매핑할 인덱스
    
    # 벡터와 정수 ID를 함께 추가
    id_index.add_with_ids(vectors, np.array(ids, dtype=np.int64))
    
    return id_index

# 인덱스 저장
def save_faiss_index(index, index_filename="app/data/faiss_indices/faiss_index.bin"):
    os.makedirs(os.path.dirname(index_filename), exist_ok=True)  # 인덱스 파일 디렉토리 생성
    faiss.write_index(index, index_filename)  # FAISS 인덱스 저장

if __name__ == "__main__":
    db_connection = mysql.connector.connect(
        host=os.environ['KOPIS_DB_HOST'],       # MySQL 서버 호스트명
        user=os.environ['KOPIS_DB_USER'],   # MySQL 사용자 이름
        password=os.environ['KOPIS_DB_PASSWORD'], # MySQL 비밀번호
        database=os.environ['KOPIS_DB_DATABASE']  # 연결할 데이터베이스 이름
    )
    # 데이터베이스에서 특징 벡터와 이미지 ID를 가져옴
    print('[START] 데이터베이스에서 특징 벡터와 이미지 ID를 가져옴')
    ids, feature_vectors = get_feature_vectors_and_ids_from_db(db_connection)

    # FAISS 인덱스 생성
    print('[START] FAISS 인덱스 생성')
    index = build_faiss_index(feature_vectors, ids)
    
    # 인덱스 저장
    print('[START] 인덱스 저장')
    save_faiss_index(index, "app/data/faiss_indices/faiss_index.bin")
