import requests
from PIL import Image
from io import BytesIO

def convert_gif_to_png(gif_file):
    with Image.open(gif_file) as img:
        img = img.convert('RGB')  # 필요에 따라 RGB로 변환
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

if __name__ == "__main__":
    # URL에서 이미지 다운로드
    url = "http://www.kopis.or.kr/upload/pfmPoster/PF_PF150653_190702_141854.gif"

    response = requests.get(url)  # URL에서 이미지 다운로드
    gif_image = BytesIO(response.content)  # 다운로드한 이미지를 BytesIO로 변환
    png_image = convert_gif_to_png(gif_image)  # GIF를 PNG로 변환

    # 변환된 PNG 이미지를 저장
    with open("app/temp/output_image.png", "wb") as f:
        f.write(png_image.getvalue())