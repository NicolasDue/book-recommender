from fastapi import FastAPI, HTTPException
from models.request_models import RecommendationRequest
from models.response_models import RecommendationResponse, BookRecommendation
from db_handler import connect, disconnect, get_book_titles_by_ids
from recommenders.recommender_factory import RECOMMENDERS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await connect()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect()


@app.get("/recommend", response_model=RecommendationResponse)
async def recommend_books(data: RecommendationRequest):
    try:
        recommender = RECOMMENDERS[data.recommender]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Recommender {data.recommender} not found")
    
    recommendations = await recommender.recommend([(book_score.book_id, book_score.score) for book_score in data.book_scores], size=data.size)

    # Get all book titles in one database call.
    book_ids = [book_id for book_id, _ in recommendations]
    titles = await get_book_titles_by_ids(book_ids)

    return {
        "recommendations": [
            BookRecommendation(
                book_id=book_id, 
                score=score, 
                title=titles[book_id]
            ) for book_id, score in recommendations
        ]
    }