import torch
import clip
import io
from PIL import Image

class CLIP:
    def __init__(self):
        # CLIP 모델 및 처리기를 로드합니다.
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def extract_text_embedding(self, text):
        """
        주어진 텍스트로부터 CLIP 임베딩 벡터를 추출합니다.
        
        Args:
            text (str): 텍스트 입력.
            
        Returns:
            torch.Tensor: 텍스트의 임베딩 벡터.
        """
        # 텍스트를 CLIP 모델의 입력 형식으로 변환합니다.
        text_input = clip.tokenize([text]).to(self.device)
        
        # 임베딩 벡터를 추출합니다.
        with torch.no_grad():
            text_embedding = self.model.encode_text(text_input)
            
        return text_embedding

    def extract_image_embedding(self, image_file):
        """
        주어진 이미지 파일로부터 CLIP 임베딩 벡터를 추출합니다.
        
        Args:
            image_file: 이미지 파일.
            
        Returns:
            torch.Tensor: 이미지의 임베딩 벡터.
        """
        # 이미지를 로드하고 전처리합니다.
        image = self.preprocess(Image.open(io.BytesIO(image_file.read()))).unsqueeze(0).to(self.device)
        
        # 임베딩 벡터를 추출합니다.
        with torch.no_grad():
            image_embedding = self.model.encode_image(image)
            
        return image_embedding

# 예시 사용법
if __name__ == "__main__":
    clip_instance = CLIP()  # CLIP 클래스 인스턴스 생성

    # 텍스트 임베딩 추출 예제
    text = "A photo of a cat"
    text_embedding = clip_instance.extract_text_embedding(text)
    print("Text Embedding:", text_embedding)

    # 이미지 임베딩 추출 예제
    # 이미지 파일을 읽어 io.BytesIO 객체로 변환하여 사용합니다.
    with open("app/image/test.jpg", "rb") as img_file:
        image_embedding = clip_instance.extract_image_embedding(io.BytesIO(img_file.read()))
    print("Image Embedding:", image_embedding)
