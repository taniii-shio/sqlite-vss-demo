import os
from dotenv import load_dotenv

from typing import List
from datetime import datetime
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from db import db

load_dotenv()

def serialize(vector: List[float]) -> bytes:
  # """ serializes a list of floats into a compact "raw bytes" format """
  return np.asarray(vector).astype(np.float32).tobytes()

def generate_embedding(text: str) -> List[float]:
  embeddings = OpenAIEmbeddings(deployment=os.getenv("EMBE_DEPLOYMENT_NAME"), chunk_size=1)
  response = embeddings.embed_query(text)
  return response

def insert_paper(entry_id, published, title, summary):
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

def search_similar_embeddings(query_embedding, k=1):
  results = db.execute('''
      SELECT papers.*, vss_papers.distance
      FROM vss_papers
      JOIN papers ON vss_papers.rowid = papers.id
      WHERE vss_search(vss_papers.summary_embedding, vss_search_params(?, 10))
      ORDER BY vss_papers.distance
      LIMIT ?
  ''', (serialize(query_embedding), k))
  return results.fetchall()
