import requests
import time

url = "http://localhost:5000/process"
files = {"image": ("test_image.jpg", open("app/image/test.jpg", "rb"))}

start_time = time.time()
print("Sending file:", files['image'][0])

response = requests.post(url, files=files)

# Response status code
print("Response status code:", response.status_code)

# Response content
print("Response text:", response.text)

end_time = time.time()
print("Time taken:", end_time - start_time)