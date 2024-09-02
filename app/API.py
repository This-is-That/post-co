import os
import urllib.request
import json
from openai import OpenAI

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

def dalle3(client, prompt) -> str:
    def call_dalle(client, prompt):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",
            quality="standard",
            n=1,
        )
        return response

    try:
        response = call_dalle(client, prompt)
        
        # 응답 코드가 200이 아닐 경우 예외를 발생시킴
        if response.status_code != 200:
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
            response = call_dalle(client, prompt)

        return response.data[0].url

    except Exception as e:
        print(f"Error occurred: {e}")
        
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        try:
            response = call_dalle(client, prompt)
            return response.data[0].url
        
        except Exception as e:
            print(f"Retry failed: {e}")
            raise e  # 필요에 따라 예외를 다시 발생시킬 수 있음


def advanced_prompt(client, prompt):
    def call_openai(client, prompt):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert assistant in generating detailed and creative prompts for visual content, especially theatre posters. When a user provides a prompt, break it down into three parts: a basic prompt, an image style, and a detailed description, ensuring clarity and creativity."},
                {"role": "user", "content": prompt},
            ],
        )
        return response

    try:
        response = call_openai(client, prompt)
        
        # 응답 코드가 200이 아닐 경우
        if response.status_code != 200:
            print("response status code is not 200")
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
            response = call_openai(client, prompt)
        
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error occurred: {e}")
        
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        try:
            response = call_openai(client, prompt)
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Retry failed: {e}")
            raise e  # 필요에 따라 예외를 다시 발생시킬 수 있음

def generate_image(pipe, client, prompt, img_url = None) -> str:
    prompt_en = translate(prompt)
    if img_url:
        try:
            generated_text = pipe(img_url)

        except Exception as e:
            print(f"An error occurred: {e}")
            generated_text = None  # 오류 발생 시 기본값 설정
            
        prompt_advanced = (
            f"Original Image Description:\n{generated_text}\n\n"
            f"Modification Instructions:\n{prompt_en}"
        )
    else:
        prompt_advanced = advanced_prompt(client, prompt_en)
    return dalle3(client, prompt_advanced)