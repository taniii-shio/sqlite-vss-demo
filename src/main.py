import sys
sys.dont_write_bytecode = True

from data import papers
from db import db
from functions import insert_paper, generate_embedding, search_similar_embeddings

if __name__ == '__main__':
  # papersテーブルにデータを挿入
  for paper in papers:
    paper_id = insert_paper(paper['title'], paper['abstract'], paper['summary'], paper['url'])

  # クエリを作成して実行
  query_embedding = generate_embedding('ロボット')
  results = search_similar_embeddings(query_embedding)
  print(results[0])

  titles = [row[1] for row in results]
  print(titles)
