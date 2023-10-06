from pydantic import BaseModel
from typing import List

class BookRecommendation(BaseModel):
    book_id: int
    score: float
    title: str

class RecommendationResponse(BaseModel):
    recommendations: List[BookRecommendation]
