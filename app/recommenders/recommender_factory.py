from .dummy_recommender import DummyBookRecommender
from .collaborative_filtering_recommender import CollaborativeFilteringRecommender

class LazyRecommenderDict(dict):
    def __missing__(self, key):
        if key == "dummy":
            value = DummyBookRecommender()
            self[key] = value
            return value
        if key == "collaborative":
            value = CollaborativeFilteringRecommender()
            self[key] = value
            return value
        raise KeyError(key)

RECOMMENDERS = LazyRecommenderDict()