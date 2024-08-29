import requests
import os
import urllib.request
import json

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
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1792",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def generate_image(pipe, client, prompt, img_url = None) -> str:
    prompt_en = translate(prompt)
    if img_url:
        response = requests.get(img_url)
        if response.status_code == 200:
            data = response.content
        else:
            raise Exception(f"Failed to download image: {response.status_code} - {response.text}")

        generated_text = pipe(img_url)
            
        prompt_advanced = (
            f"Original Image Description:\n{generated_text}\n\n"
            f"Modification Instructions:\n{prompt_en}"
        )
    else:
        prompt_advanced = advanced_prompt(client, prompt_en)
    return dalle3(client, prompt_advanced)


def advanced_prompt(client, prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are an expert assistant in generating detailed and creative prompts for visual content, especially theatre posters. When a user provides a prompt, break it down into three parts: a basic prompt, an image style, and a detailed description, ensuring clarity and creativity."},
                {"role": "user", "content": prompt},
                ],
    )
    return completion.choices[0].message.content