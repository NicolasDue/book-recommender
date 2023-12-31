from pydantic import BaseModel
from typing import List

class BookScore(BaseModel):
    book_id: int
    score: float

class RecommendationRequest(BaseModel):
    recommender: str
    book_scores: List[BookScore]
    size: int
