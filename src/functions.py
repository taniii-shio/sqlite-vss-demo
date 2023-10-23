import os
from dotenv import load_dotenv

from typing import List
from datetime import datetime
import numpy as np
import openai
from db import db

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def serialize(vector: List[float]) -> bytes:
  # """ serializes a list of floats into a compact "raw bytes" format """
  return np.asarray(vector).astype(np.float32).tobytes()

def generate_embedding(text: str) -> List[float]:
  response = openai.Embedding.create(
    engine="text-embedding-ada-002",
    input=[text]
  )
  return response['data'][0]['embedding']

def insert_paper(entry_id, published, title, summary):
  # current_time = datetime.now()
  summary_embedding = generate_embedding(summary)

  with db:
    db.execute('''
        INSERT INTO papers(entry_id, published, title, summary)
        VALUES (?, ?, ?, ?)
    ''', (entry_id, published, title, summary))

    last_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

    db.execute('''
        INSERT INTO vss_papers(rowid, summary_embedding)
        VALUES (?, ?)
    ''', (last_id, serialize(summary_embedding)))

def search_similar_embeddings(query_embedding, k=5):
  results = db.execute('''
      SELECT papers.*, vss_papers.distance
      FROM vss_papers
      JOIN papers ON vss_papers.rowid = papers.id
      WHERE vss_search(vss_papers.summary_embedding, vss_search_params(?, 10))
      ORDER BY vss_papers.distance
      LIMIT ?
  ''', (serialize(query_embedding), k))
  return results.fetchall()
