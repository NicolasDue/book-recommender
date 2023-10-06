from .dummy_recommender import DummyBookRecommender

class LazyRecommenderDict(dict):
    def __missing__(self, key):
        if key == "dummy":
            value = DummyBookRecommender()
            self[key] = value
            return value
        raise KeyError(key)

RECOMMENDERS = LazyRecommenderDict()