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
