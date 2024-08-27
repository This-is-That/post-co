import requests
import base64
from PIL import Image
from io import BytesIO
import os
from openai import OpenAI
import urllib.request
import json
# URL 이미지를 다운로드하여 base64로 인코딩하는 함수
def download_and_encode_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        
        # GIF 파일을 PNG로 변환
        if not image_url.endswith('.png'):
            image_data = convert_image_to_png(image_data)

        image_base64 = base64.b64encode(image_data).decode("utf-8")
        return image_base64
    else:
        raise Exception(f"Failed to download image: {response.status_code} - {response.text}")

# GIF 이미지를 PNG로 변환하는 함수
def convert_image_to_png(image_data):
    with Image.open(BytesIO(image_data)) as img:
        # 첫 번째 프레임을 PNG로 변환
        png_image = BytesIO()
        img.save(png_image, format="PNG")
        return png_image.getvalue()

def translate(prompt, src='ko', tar='en'):
    client_id = os.environ['NAVER_PAPAGO_ID']
    client_secret = os.environ['NAVER_PAPAGO_SECRET']
    encText = urllib.parse.quote(prompt)
    data = f"source={src}&target={tar}&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_decode = json.loads(response.read().decode('utf-8'))
        return response_decode['message']['result']['translatedText']
    else:
        print("Error Code:" + rescode)

def generate_image() -> str:
    pass

def edit_image() -> str:
    pass

def advanced_prompt(prompt, client):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are an expert assistant in generating detailed and creative prompts for visual content, especially theatre posters. When a user provides a prompt, break it down into three parts: a basic prompt, an image style, and a detailed description, ensuring clarity and creativity."},
                {"role": "user", "content": prompt},
                ]
    )
    return completion.choices[0].message.content

if __name__ == '__main__':
    prompt = "바다의 신비로움과 웅장함을 강조하는 포스터"

    prompt_en = translate(prompt)
    print(prompt_en)

    client = OpenAI()
    # client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    completion = advanced_prompt(prompt_en, client)
    print(completion)