from .base_recommender import BaseBookRecommender

class DummyBookRecommender(BaseBookRecommender):

    async def recommend(self, book_scores, size):
        return book_scores
