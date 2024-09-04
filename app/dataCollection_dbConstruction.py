import pandas as pd
import requests
import xml.etree.ElementTree as ET
import mysql.connector
import subprocess
import re
import shutil
import os
import json
from sqlalchemy import create_engine

api_key = os.environ['KOPIS_OPENAPI_KEY']

### OPEN API 포스터 링크 다운

# 해당 API 데이터가 json이 아닌 XML로 이루어져있기 때문에 XML을 파싱해서 추출한다.
def read_xml(url):
    # URL에서 XML 데이터를 가져오기
    response = requests.get(url)
    pg = response.content

    # XML 파싱
    doc = ET.fromstring(pg)

    # XML 노드에서 데이터 추출
    nodes = doc.findall(".//db")
    data = []
    for node in nodes:
        row = {}
        for child in node:
            row[child.tag] = child.text
        data.append(row)

    # DataFrame으로 변환
    xmldf = pd.DataFrame(data)

    return xmldf

# URL과 데이터 호출


# URL
## 13년부터 23년까지 11년간의 공연을 수집한다.
url_2013 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20130101&eddate=20131231"
url_2014 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20140101&eddate=20141231"
url_2015 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20150101&eddate=20151231"
url_2016 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20160101&eddate=20161231"
url_2017 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20170101&eddate=20171231"
url_2018 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20180101&eddate=20181231"
url_2019 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20190101&eddate=20191231"
url_2020 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20200101&eddate=20201231"
url_2021 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20210101&eddate=2021231"
url_2022 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20220101&eddate=20221231"
url_2023 = f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={api_key}&cpage=1&rows=30000&stdate=20230101&eddate=20231231"


# 정보 다운
xmldf_2013 = read_xml(url_2013)
xmldf_2014 = read_xml(url_2014)
xmldf_2015 = read_xml(url_2015)
xmldf_2016 = read_xml(url_2016)
xmldf_2017 = read_xml(url_2017)
xmldf_2018 = read_xml(url_2018)
xmldf_2019 = read_xml(url_2019)
xmldf_2020 = read_xml(url_2020)
xmldf_2021 = read_xml(url_2021)
xmldf_2022 = read_xml(url_2022)
xmldf_2023 = read_xml(url_2023)

# 데이터 출력 테스트
print(xmldf_2013.head())
print(xmldf_2013.columns)

# 포스터 추출에 필요한 컬럼만 사용한다.
poster_2013 = xmldf_2013[["mt20id","prfnm","poster"]]
poster_2014 = xmldf_2014[["mt20id","prfnm","poster"]]
poster_2015 = xmldf_2015[["mt20id","prfnm","poster"]]
poster_2016 = xmldf_2016[["mt20id","prfnm","poster"]]
poster_2017 = xmldf_2017[["mt20id","prfnm","poster"]]
poster_2018 = xmldf_2018[["mt20id","prfnm","poster"]]
poster_2019 = xmldf_2019[["mt20id","prfnm","poster"]]
poster_2020 = xmldf_2020[["mt20id","prfnm","poster"]]
poster_2021 = xmldf_2021[["mt20id","prfnm","poster"]]
poster_2022 = xmldf_2022[["mt20id","prfnm","poster"]]
poster_2023 = xmldf_2023[["mt20id","prfnm","poster"]]

# CSV 출력
poster_2013.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2014.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2015.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2016.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2017.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2018.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2019.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2020.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2021.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2022.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')
poster_2023.to_csv('포스터 링크2 2013.csv', index=False, encoding='utf-8-sig')



### 각 파일을 하나의 파일로 통합해 사용한다. 
data2013 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2013.csv")
data2014 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2014.csv")
data2015 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2015.csv")
data2016 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2016.csv")
data2017 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2017.csv")
data2018 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2018.csv")
data2019 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2019.csv")
data2020 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2020.csv")
data2021 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2021.csv")
data2022 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2022.csv")
data2023 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 raw2/포스터 링크2 2023.csv")


data = data2013.merge(data2014, how="outer")
data = data.merge(data2015, how="outer")
data = data.merge(data2016, how="outer")
data = data.merge(data2017, how="outer")
data = data.merge(data2018, how="outer")
data = data.merge(data2019, how="outer")
data = data.merge(data2020, how="outer")
data = data.merge(data2021, how="outer")
data = data.merge(data2022, how="outer")
data = data.merge(data2023, how="outer")
data.info()

# 영화 시리즈를 그룹화할 열 추가
## 공연 시리즈 같은 경우 같은 포스터로 지역명만 바꾸어 사용하는 경우가 빈번해 모델 학습에 지장을 줄 가능성이 높다 판단해 시리즈를 지워주는 함수 사용.
def get_series(title):
    match = re.match(r'(.+?)\s*\[.*\]$', title)
    if match:
        return match.group(1).strip()
    return title

data['prfnm'] = data['prfnm'].apply(get_series) # 공연 제목 열에 시리즈 제거
data['prfnm'] = data['prfnm'].str.replace("/", "") # / 문자열 교체로 문자 제거 (포스터를 다운받을 때 경로 선택에 영향을 주어 삭제)
data = data.drop_duplicates(subset=['prfnm']) # 중복 제거 
data.info()

data.isnull().sum()
data.dropna()
data.to_csv('포스터 링크 새로운버전.csv', index=False, encoding='utf-8-sig')


### 포스터 다운 전 작업

df = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 링크 새로운버전.csv")
df
df.rename(columns={'mt20id': 'ID', 'prfnm': 'image_id', 'poster': 'image_url'}, inplace=True) # 컬럼 이름 데이터베이스랑 똑같이 맞추기.

df['image_id'] = df['image_id'].str.lower() # 문자열 영여 소문자로 변경
df = df.drop_duplicates(subset=['image_id']) # 중복제거
df

## 해당 특수문자들 경우 파이썬에서는 중복으로 인식하지 못하는데 MySQL에서는 중복으로 인식하는 경우들이 존재한다. 이를 해결하기 위해 제거한다.
df['image_id'] = df['image_id'].str.strip() # 앞 뒤 공백 제거
df['image_id'] = df['image_id'].str.replace(' ', '', regex=False) # 중간 공백 제거
df['image_id'] = df['image_id'].str.replace('#', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace('&', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace('!', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace('?', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace(':', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace('-', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace('.', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace('+', '')
df.loc[:, 'image_id'] = df['image_id'].str.replace('x', '')



# 정규 표현식을 사용하여 문자열 맨 뒤의 i, ii, iii, iv 등을 제거하는 함수
## 해당 표현식 또한 위와 마찬가지
def remove_trailing_numerals(text):
    return re.sub(r'[\s\-]*[ivxIVX0-9]+$', '', text)

# 'image_id' 열에 함수 적용
df.loc[:, 'image_id'] = df['image_id'].apply(remove_trailing_numerals)

## 아래 항목들을 제거하는 이유도 위와 동일
df = df[df['image_id'] != '광화문연가']
df = df[df['image_id'] != "acl-korea국제음악제콘서트ⅰ"]
df = df[df['image_id'] != "acl-korea국제음악제콘서트ⅲ"]
df = df[df['image_id'] != "body＆voice"]
df = df[df['image_id'] != "cjⅹberkleemusicconcert"]
df = df[df['image_id'] != "magic＆illusion"]
df = df[df['image_id'] != "showbreakers:소란＆타린"]
df = df[df['image_id'] != "showbreakers:스웨덴세탁소＆정흠밴드"]
df = df[df['image_id'] != "show－breakers:이지형＆폴킴"]
df = df[df['image_id'] != "showbreakers:최낙타＆문센트"]
df = df[df['image_id'] != "the최현우:ask？＆answer！"]
df = df[df['image_id'] != "v.o.s콘서트:퇴근하고여기어때？"]
df = df[df['image_id'] != "개굴개굴고래고래"]
df = df[df['image_id'] != "경기필마스터시리즈xi,베토벤&브람스ii"]
df = df.loc[~df['image_id'].str.contains('경기필하모닉마스터피스시리즈')]
df = df.loc[~df['image_id'].str.contains('국립창극단,절창')]
df = df.loc[~df['image_id'].str.contains('대한민국국제실내악페스티벌i')]
df = df.loc[~df['image_id'].str.contains('대한민국실내악작곡제전')]
df = df.loc[~df['image_id'].str.contains('부천필하모닉오케스트라어린이를위한음악놀이')]
df = df[df['image_id'] != '누가내머리에똥쌌어？']
df = df[df['image_id'] != '대전시립교향악단마티네콘서트１']
df = df[df['image_id'] != '루돌프부흐빈더&베토벤']
df = df[df['image_id'] != "바이올린신희선＆피아노현영경듀오리사이틀"]
df = df[df['image_id'] != "보수동쿨러ⅹ해서웨이:lovesand"]
df = df[df['image_id'] != "보헤미안랩소디퀸내한공연＆프레디머큐리미공개사진전"]
df = df[df['image_id'] != "봄봄＆아리랑난장굿"]
df = df[df['image_id'] != '부산마루국제음악제,앙상블콘서트ⅱ']
df = df[df['image_id'] != '부산시립교향악단기획음악회,미완성음악회iv']
df = df[df['image_id'] != '사운드온디엣지ⅰ,한국작곡가의밤']
df = df[df['image_id'] != '생생지락(生生之樂)']
df = df[df['image_id'] != '서울시향실내악시리즈ⅴ']
df = df[df['image_id'] != '운지회체임버오케스트라시리즈xⅵ']
df = df[df['image_id'] != '사운드온디엣지ⅰ,한국작곡가의밤']



df = df.drop_duplicates(subset=['image_id']) # 중복제거
df.to_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 링크 새로운버전 최종.csv", index=False, encoding='utf-8-sig')


### 포스터 정보 다운!
df = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 링크 새로운버전 최종.csv")

# ID를 리스트화
# ID를 기준으로 공연 정보를 API를 통해 추출해야하기 때문
id_list = df['ID'].tolist()

# 모든 데이터를 저장할 빈 데이터프레임 생성
all_data = pd.DataFrame()

# API 호출을 위한 URL 템플릿
url_template = f"https://www.kopis.or.kr/openApi/restful/pblprfr/{id}?service={api_key}&newsql=Y"

for poster_id in id_list:
    # 각 포스터에 대해 API 호출
    url = url_template.format(id=poster_id)
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류 확인
        xmldf = read_xml(url)  # XML 파싱 시도
        all_data = pd.concat([all_data, xmldf], ignore_index=True)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for ID: {poster_id}. Error: {http_err}")
    except ET.ParseError as parse_err:
        print(f"Failed to parse XML for ID: {poster_id}. Error: {parse_err}")
    except Exception as e:
        print(f"Failed to process ID: {poster_id}. Error: {str(e)}")


# 결과 확인
all_data.head()
all_data.columns
all_data = all_data[["mt20id", 'prfnm', 'prfpdfrom', 'prfpdto', 'fcltynm', 'prfcast', 'prfruntime', 'prfage']]

'''
Mt20id 공연 id
Prfnm 공연 이름
Prfpdfrom 공연시작일
Prfpdto 공연 종료일
Fcltynm 공연시설명
Precast 공연출연진
Prfruntime 공연시간
Prfage 공연관람연령
'''

all_data.rename(columns={'mt20id': 'ID', 'prfnm': 'image_id', 'prfpdfrom': 'start_date', 'prfpdto': 'end_date', \
                         'fcltynm': 'place_name',  'prfcast': 'actor', 'prfruntime': 'runtime', 'prfage': 'age',}, inplace=True)
all_data.to_csv('포스터 정보 테스트.csv', index=False, encoding='utf-8-sig')



### 이미지 다운!
df = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 링크 새로운버전 최종.csv")
df

# 저장할 디렉토리 설정 (여기서 경로를 원하는 디렉토리로 변경)
image_dir = '/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 최종최종최종'

# 이미지 다운로드 및 저장
for index, row in df.iterrows():
    image_id = row['ID']
    poster_url = row['image_url']
    
    # 파일 이름 생성: 공연 제목을 파일 이름으로 사용
    file_name = f"{image_id}.jpg"
    # 파일 경로 설정
    file_path = os.path.join(image_dir, file_name)

    try:
        # 이미지 다운로드
        response = requests.get(poster_url)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킴

        # 이미지 저장
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded and saved {file_name}")
    except requests.RequestException as e:
        print(f"Failed to download {poster_url}: {e}")

print("All images have been downloaded and saved.") 


### 이미지 포스터 파일 분할 
# 6만개가 넘는 포스터 이미지를 CLIP모델로 한번에 특징벡터를 추출할 수 없서 1000개씩 쪼개어 진행하기 위함.

folder_path = '/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 최종최종' # 이미지 포스터 원본 폴더 경로
# 모든 파일 리스트 가져오기
all_files = os.listdir(folder_path)
all_files

# 원본 이미지들이 있는 폴더 경로
source_folder = '/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 최종최종'

# 이미지를 나눌 목적지 폴더의 루트 경로
destination_root = '/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터분할분할'

# 폴더 당 나눌 이미지 파일 개수
files_per_folder = 1000


# 파일을 1000개씩 나누어서 새로운 폴더에 저장
for i in range(0, len(all_files), files_per_folder):
    # 각 폴더의 이름 지정
    folder_name = f"batch_{i//files_per_folder + 1}"
    destination_folder = os.path.join(destination_root, folder_name)

    # 목적지 폴더가 없으면 생성
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 파일 복사
    for file_name in all_files[i:i + files_per_folder]:
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        shutil.copy(source_file, destination_file)

    print("작업이 완료되었습니다.")

### 특징 벡터 다운 
### 코랩 파일
'''
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

!pip install torch torchvision ftfy regex tqdm
!pip install git+https://github.com/openai/CLIP.git
!pip install googletrans==4.0.0-rc1
!pip show torch torchvision clip
!du -sh /usr/local/lib/python3.10/dist-packages/clip

import os
import torch
import clip
from PIL import Image
from tqdm.auto import tqdm
import pandas as pd

# CLIP 모델 및 처리기를 로드합니다.
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def load_images_and_extract_features(image_folder):
    # 이미지를 로드하고 특징 벡터를 추출합니다.
    image_features = []
    file_names = []

    print("start loading images and extracting features...")
    for filename in tqdm(os.listdir(image_folder)):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            img_path = os.path.join(image_folder, filename)
            image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)

            with torch.no_grad():
                features = model.encode_image(image)
                image_features.append(features.cpu().numpy().flatten())  # GPU에서 CPU로 이동 및 flatten
                file_names.append(filename)

    print("end loading images and extracting features!")
    return image_features, file_names

def features_to_dataframe(image_features, file_names):
    # 특징 벡터와 파일명을 데이터프레임으로 변환합니다.
    df = pd.DataFrame(image_features)
    df.insert(0, "file_name", file_names)
    return df

def save_dataframe(df, save_path):
    # 데이터프레임을 CSV 파일로 저장합니다.
    df.to_csv(save_path, index=False)
    print(f"Dataframe saved to {save_path}")

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

for i in range(1,61):
  image_folder = f"/content/drive/MyDrive/KOPIS/data/분할해제/batch_{i}"
  save_path = f"/content/drive/MyDrive/KOPIS/data/특징 벡터/batch_factor_{i}.csv"

  image_features, file_names = load_images_and_extract_features(image_folder)
  df = features_to_dataframe(image_features, file_names)
  save_dataframe(df, save_path)
  print(f'batch_factor_{i} complete.')

'''

### 특징벡터 벤치 60개 통합해서 json 변경

import json

batch_1 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_1.csv")
batch_2 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_2.csv")
batch_3 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_3.csv")
batch_4 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_4.csv")
batch_5 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_5.csv")
batch_6 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_6.csv")
batch_7 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_7.csv")
batch_8 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_8.csv")
batch_9 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_9.csv")
batch_10 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_10.csv")
batch_11 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_11.csv")
batch_12 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_12.csv")
batch_13 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_13.csv")
batch_14 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_14.csv")
batch_15 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_15.csv")
batch_16 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_16.csv")
batch_17 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_17.csv")
batch_18 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_18.csv")
batch_19 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_19.csv")
batch_20 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_20.csv")
batch_21 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_21.csv")
batch_22 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_22.csv")
batch_23 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_23.csv")
batch_24 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_24.csv")
batch_25 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_25.csv")
batch_26 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_26.csv")
batch_27 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_27.csv")
batch_28 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_28.csv")
batch_29 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_29.csv")
batch_30 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_30.csv")
batch_31 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_31.csv")
batch_32 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_32.csv")
batch_33 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_33.csv")
batch_34 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_34.csv")
batch_35 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_35.csv")
batch_36 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_36.csv")
batch_37 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_37.csv")
batch_38 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_38.csv")
batch_39 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_39.csv")
batch_40 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_40.csv")
batch_41 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_41.csv")
batch_42 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_42.csv")
batch_43 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_43.csv")
batch_44 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_44.csv")
batch_45 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_45.csv")
batch_46 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_46.csv")
batch_47 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_47.csv")
batch_48 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_48.csv")
batch_49 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_49.csv")
batch_50 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_50.csv")
batch_51 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_51.csv")
batch_52 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_52.csv")
batch_53 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_53.csv")
batch_54 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_54.csv")
batch_55 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_55.csv")
batch_56 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_56.csv")
batch_57 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_57.csv")
batch_58 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_58.csv")
batch_59 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_59.csv")
batch_60 = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/특징 벡터/batch_factor_60.csv")

images_feature = pd.concat([batch_1, batch_2, batch_3, batch_4, batch_5, batch_6, batch_7, batch_8, batch_9, batch_10,\
                            batch_11, batch_12, batch_13, batch_14, batch_15, batch_16, batch_17, batch_18, batch_19, batch_20,\
                            batch_21, batch_22, batch_23, batch_24, batch_25, batch_26, batch_27, batch_28, batch_29, batch_30,\
                            batch_31, batch_32, batch_33, batch_34, batch_35, batch_36, batch_37, batch_38, batch_39, batch_40,\
                            batch_41, batch_42, batch_43, batch_44, batch_45, batch_46, batch_47, batch_48, batch_49, batch_50,\
                            batch_51, batch_52, batch_53, batch_54, batch_55, batch_56, batch_57, batch_58, batch_59, batch_60])

images_feature

images_feature.rename(columns={'file_name' : 'ID'}, inplace=True)
images_feature['ID'] = images_feature['ID'].str.replace('.jpg', '', regex=False) # 파일명에 jpg 제거

#512개 컬럼 문자형으로 리스트 정렬
embedding_columns = [str(i) for i in range(512)]

# 512개 열 합쳐서 하나로 만들기.
images_feature['feature_factor'] = images_feature[embedding_columns].values.tolist()

images_feature['feature_factor'] = images_feature['feature_factor'].apply(json.dumps) # 특징벡터 json으로 변경
images_feature = images_feature[["ID", "feature_factor"]]

images_feature.to_csv("feature_factor.csv", index=False, encoding='utf-8-sig')


images_main = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 링크 새로운버전 최종.csv")
images_main.isnull().sum()
images_main = images_main.dropna()

images_feature = images_main.merge(images_feature, on='ID', how='left')
images_feature = images_feature[['ID', 'image_id', 'feature_factor']]
images_feature.rename(columns={'feature_factor': 'feature_vector'}, inplace=True)

images_feature.to_csv('images_vector.csv', index=False, encoding='utf-8-sig')

### 최종 데이터 베이스 업로드

# 데이터베이스 연결 정보 설정
config = os.environ['MySQL_DB']

config = {
    'user': 'root',
    'password': '01093382277',
    'host': 'localhost',
    'database': 'KOPIS_bigdata_contest'
}

# 데이터베이스에 연결
conn = mysql.connector.connect(**config)

# 데이터베이스 연결 확인
if conn.is_connected():
    print('MySQL database connection successful')
else:
    print("Mysql database not connection")

# SQLAlchemy 엔진 생성
connection_string = (
    f"mysql+mysqlconnector://{config['user']}:{config['password']}@"
    f"{config['host']}/{config['database']}"
)
engine = create_engine(connection_string)


## images_main
images_main = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 링크 새로운버전 최종.csv")
images_main.isnull().sum()
images_main = images_main.dropna()
images_main.to_sql(name='images_main', con=engine, if_exists='append', index=False)

query = "SELECT * FROM images_main"
testing = pd.read_sql(query, engine)
print(testing)
images_main.to_csv('images_main.csv', index=False, encoding='utf-8-sig')



## images_features
images_feature = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/데이터베이스 최종 파일/images_vector.csv")
images_feature

images_feature = images_main.merge(images_feature, on='ID', how='left')
images_feature = images_feature[['ID', 'image_id', 'feature_vector']]

images_feature.to_csv('images_features.csv', index=False, encoding='utf-8-sig')

# 데이터프레임을 청크로 나누어 업로드
chunk_size = 10
for start in range(0, len(images_feature), chunk_size):
    end = start + chunk_size
    chunk = images_feature[start:end]
    chunk.to_sql(name='images_features', con=engine, if_exists='append', index=False)
    print(f'Uploaded rows {start} to {end}')

query = "SELECT * FROM images_features"
testing = pd.read_sql(query, engine)
print(testing)


## images_info
images_info = pd.read_csv("/Users/eomjaeyong/Desktop/공모전/KOPIS 데이터 공모전/데이터 모음/포스터 정보 최종최종.csv")
images_info

images_info = images_info.drop(columns=['image_id'])
images_info = images_main.merge(images_info, on='ID', how='left')
images_info.columns
images_info = images_info.drop(columns=['image_url'])

images_info.to_csv('images_info.csv',  index=False, encoding='utf-8-sig')

images_info.to_sql(name='images_info', con=engine, if_exists='append', index=False)

query = "SELECT * FROM images_info"
testing = pd.read_sql(query, engine)
print(testing)


### 덤프파일 생성

config = {
    'user': 'root',
    'password': '01093382277',
    'host': 'localhost',
    'database': 'KOPIS_bigdata_contest'
}

# 덤프 파일 이름 설정
dump_file = 'final_database.sql'

# mysqldump 명령어 생성
dump_command = [
    'mysqldump',
    f'--user={config["user"]}',
    f'--password={config["password"]}',
    f'--host={config["host"]}',
    config['database']
]

dump_command
# 덤프 파일 생성
with open(dump_file, 'w') as output_file:
    result = subprocess.run(dump_command, stdout=output_file)

if result.returncode == 0:
    print(f'Successfully created dump file: {dump_file}')
else:
    print('Failed to create dump file')


# 연결 종료 꼭! 해주기
if conn.is_connected(): 
    conn.close()
    print('MySQL connection is closed')
else:
    print("MySQL already shut down")
