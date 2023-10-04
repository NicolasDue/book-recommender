from .base_recommender import BaseBookRecommender

class DummyBookRecommender(BaseBookRecommender):

    def recommend(self, book_scores):
        return book_scores
