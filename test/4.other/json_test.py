import os

# # 설정 파일에서 인증키를 불러옴
# with open("config.json", "r") as config_file:
#     config = json.load(config_file)
#     kopis_api_key = config["KOPIS_OPENAPI_KEY"]

# 환경 변수로 인증키를 불러옴
kopis_api_key = os.getenv("KOPIS_OPENAPI_KEY")

print(kopis_api_key)
