import sqlite3, sqlite_vss, numpy as np
from typing import List
from functions.embedding import generate_embedding

db = sqlite3.connect('papers.db', timeout=10)
db.enable_load_extension(True)
sqlite_vss.load(db)
vss_version = db.execute('select vss_version()').fetchone()[0]
print('SQLite VSS Version: %s' % vss_version)

# papersテーブルの作成
db.execute('''
    CREATE TABLE IF NOT EXISTS papers(
        id INTEGER PRIMARY KEY,
        published DATETIME,
        title TEXT,
        primary_category TEXT,
        url TEXT,
        abstract TEXT
    );
''')

# vss_paperテーブルの作成
db.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS vss_papers USING vss0(
        abstract_embedding(1536)
    );
''')

def serialize(vector: List[float]) -> bytes:
  return np.asarray(vector).astype(np.float32).tobytes()

def insert_paper(published, title, primary_category, url, abstract):
  abstract_embedding = generate_embedding(abstract)

  with db:
    db.execute('''
        INSERT INTO papers(published, title, primary_category, url, abstract)
        VALUES (?, ?, ?, ?, ?)
    ''', (published, title, primary_category, url, abstract))

    last_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

    db.execute('''
        INSERT INTO vss_papers(rowid, abstract_embedding)
        VALUES (?, ?)
    ''', (last_id, serialize(abstract_embedding)))

def search_similar_embeddings(query_embedding, category, k):
  if category == "all":
    category = "%cs%"
  else:
    category = "cs." + category

  results = db.execute('''
      SELECT papers.*, vss_papers.distance
      FROM vss_papers
      JOIN papers ON vss_papers.rowid = papers.id
      WHERE papers.primary_category LIKE ?
      AND vss_search(vss_papers.abstract_embedding, vss_search_params(?, 10))
      ORDER BY vss_papers.distance
      LIMIT ?
  ''', (category, serialize(query_embedding), k))
  return results.fetchall()
