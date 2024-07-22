import requests
import os

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

headers = {f"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def query(filename):

    with open(filename, "rb") as f:

        data = f.read()

    response = requests.post(API_URL, headers=headers, data=data)

    return response.json()

output_copy = query("test\ImageCaptioning\image\SecretaryKim_copy.jpg")
output_original = query("test\ImageCaptioning\image\SecretaryKim.jpg")
output_other1 = query("test\ImageCaptioning\image\LesMiserables.jpg")
output_other2 = query("test\ImageCaptioning\image\NewWaveDance.jpg")

print("copy: ", output_copy)
print("original: ", output_original)
print("other 1: ", output_other1)
print("other 2: ", output_other2)

# copy:  [{'generated_text': 'a close up of a person sitting on a couch with a woman'}]
# original:  [{'generated_text': 'arafed image of a man and a woman sitting on a couch'}]
# other 1:  [{'generated_text': 'they are performing a dance in a poster for a show'}]
# other 2:  [{'generated_text': 'arafed poster of a woman in a bikini holding a baseball bat'}]