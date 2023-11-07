from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import schemas.paper as paper_schema
from db.db import search_similar_embeddings
from functions.embedding import generate_embedding
from functions.summarize import summarize
from functions.translate import translate


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/papers", response_model=List[paper_schema.SummarizedPaper])
async def search_papers(keyword: str, category: str, num: int, lan: int):
  # キーワードとカテゴリーと件数でベクトル検索
    query_embedding = generate_embedding(keyword)
    search_results: List[paper_schema.SearchedPaper] = [paper_schema.SearchedPaper(**dict(zip(["id", "published", "title", "primary_category", "url", "abstract"], row))) for row in search_similar_embeddings(query_embedding, category, num)]

  # 目的、手法、新規性を要約
    summarize_results: List[paper_schema.SummarizedPaper] = []
    for row in search_results:
        summarized = summarize(row.abstract)
        summarize_results.append(paper_schema.SummarizedPaper(**dict(zip(["id", "published", "title", "primary_category", "url", "purpose", "method", "novelty"], [row.id, row.published, row.title, row.primary_category, row.url, summarized[0]["purpose"], summarized[0]["method"], summarized[0]["novelty"]]))))

  # 日本語の場合は翻訳する
    if lan == 0:
        pass
    elif lan == 1:
        # summarize_resultsのpurpose, method, noveltyをtranslateを使用し、日本語に翻訳
        for row in summarize_results:
            row.purpose = translate(row.purpose)
            row.method = translate(row.method)
            row.novelty = translate(row.novelty)
        
    return summarize_results
