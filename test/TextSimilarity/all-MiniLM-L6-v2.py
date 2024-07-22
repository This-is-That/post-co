import requests
import os

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

headers = {f"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
	"source_sentence": "arafed image of a man and a woman sitting on a couch",
	"sentences": [
		"a close up of a person sitting on a couch with a woman",
		"they are performing a dance in a poster for a show",
		"arafed poster of a woman in a bikini holding a baseball bat"
	]
},
})

print(output)
# [0.6997346878051758, 0.18067607283592224, 0.24358312785625458]
# 0.6997346878051758 is the most similar
# 0.18067607283592224 is the second most similar
# 0.24358312785625458 is the third most similar