import os
from dotenv import load_dotenv
from typing import List
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()

def generate_embedding(text: str) -> List[float]:
  embeddings = OpenAIEmbeddings(deployment=os.getenv("EMBE_DEPLOYMENT_NAME"), chunk_size=1)
  response = embeddings.embed_query(text)
  return response
