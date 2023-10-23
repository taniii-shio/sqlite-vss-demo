import sys
sys.dont_write_bytecode = True

import json
# from data import papers
from db import db
from functions import insert_paper, generate_embedding, search_similar_embeddings

if __name__ == '__main__':
  # papersテーブルにデータを挿入
  with open('data.json') as f:
    all_results = json.load(f)

  for data in all_results:
    insert_paper(data['entry_id'], data['published'], data['title'], data['summary'])

  # クエリを作成して実行
  query_embedding = generate_embedding('量子')
  results = search_similar_embeddings(query_embedding)
  print(results[0])

  # titles = [row[1] for row in results]
  # print(titles)
