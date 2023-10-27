import sys
sys.dont_write_bytecode = True
import pprint
import json

from functions import insert_paper, generate_embedding, search_similar_embeddings
from summarize import summarize

import arxiv

if __name__ == '__main__':
  # papersテーブルにデータを挿入
  # with open('data.json') as f:
  #   all_results = json.load(f)

  # for data in all_results:
  #   insert_paper(data['entry_id'], data['published'], data['title'], data['summary'])

  # 検索
  query = "LLM"
  query_embedding = generate_embedding(query)
  results = search_similar_embeddings(query_embedding)
  # 検索結果を要約のみのリストに整形（4列目がsummary）
  # summarys = [row[1] for row in results]
  # pprint.pprint(summarys)
  # print(len(summarys))

  pprint.pprint(results[0])

  # print("query : " + query)
  # for row in results:
  #   print('------------------')
  #   print("title : " + row[3])
  #   print("url : " + row[1]) 

  #   # 要約する
  #   summary = summarize(row[4])
  #   print(summary)

  # arxivAPIでpdfをダウンロードする
  # paper = next(arxiv.Client().results(arxiv.Search(id_list=[entry_ids[0].replace("http://arxiv.org/abs/", "")])))
  # paper.download_pdf()
