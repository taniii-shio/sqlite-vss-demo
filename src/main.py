import sys
sys.dont_write_bytecode = True
import pprint

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

  # 検索
  query_embedding = generate_embedding('Benchmarks')
  results = search_similar_embeddings(query_embedding)
  print(type(results))
  pprint.pprint(results)

  # summarys = [row[4] for row in results]
  # print(type(summarys))
  # print(summarys[0])

  # langchainのプロンプトを使用し、summarys[0]を要約する
