from pydantic import BaseModel, Field

class PaperBase(BaseModel):
  id: int = Field(None, description="The id of the paper")
  title: str = Field(None, description="The title of the paper")
  published: str = Field(None, description="The published date of the paper")
  url: str = Field(None, description="The url of the paper")
  primary_category: str = Field(None, description="The primary category of the paper")

class SearchedPaper(PaperBase):
  abstract: str = Field(None, description="The abstract of the paper")

class SummarizedPaper(PaperBase):
  purpose: str = Field(None, description="The purpose of the paper")
  method: str = Field(None, description="The method of the paper")
  novelty: str = Field(None, description="The novelty of the paper")
