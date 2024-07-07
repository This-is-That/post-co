import json

# 설정 파일에서 인증키를 불러옵니다.
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    kopis_api_key = config["KOPIS_OPENAPI_KEY"]

print(kopis_api_key)
