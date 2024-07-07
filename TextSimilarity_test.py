# https://www.google.com/url?q=https%3A%2F%2Fhuggingface.co%2FKDHyun08%2FTAACO_STS
# !pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer, models, util
import torch

embedding_model = models.Transformer(
    model_name_or_path="KDHyun08/TAACO_STS", 
    max_seq_length=256,
    do_lower_case=True
)

pooling_model = models.Pooling(
    embedding_model.get_word_embedding_dimension(),
    pooling_mode_mean_tokens=True,
    pooling_mode_cls_token=False,
    pooling_mode_max_tokens=False,
)
model = SentenceTransformer(modules=[embedding_model, pooling_model])

docs = ["지구 멸망 후 우주에서 새로운 삶을 찾으려는 인류의 여정을 그린 영화", "시간 여행을 통해 과거와 미래를 오가는 모험을 다룬 영화", "사막에서 펼쳐지는 생존을 위한 싸움을 그린 영화", "우주 공간에서 일어나는 범죄와 그 해결 과정을 그린 영화", "미래 도시에서 벌어지는 사이버 범죄와의 전쟁을 그린 영화", "우주 탐사를 통해 새로운 행성을 발견하는 이야기를 다룬 영화", "재난에서 살아남기 위한 인류의 이야기를 그린 영화", "인공지능과 인간의 대립을 그린 영화", "우주 해적과의 싸움을 다룬 모험 영화", "사랑과 우정을 그린 감동적인 이야기"]
#각 문장의 vector값 encoding
document_embeddings = model.encode(docs)

query = "우주에서 살아남기 위한 인류의 모험을 그린 영화"
query_embedding = model.encode(query)

top_k = min(10, len(docs))

# 코사인 유사도 계산 후,
cos_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]

# 코사인 유사도 순으로 문장 추출
top_results = torch.topk(cos_scores, k=top_k)

print(f"입력 문장: {query}")
print(f"\n<입력 문장과 유사한 {top_k} 개의 문장>\n")

for i, (score, idx) in enumerate(zip(top_results[0], top_results[1])):
    print(f"{i+1}: {docs[idx]} {'(유사도: {:.4f})'.format(score)}\n")