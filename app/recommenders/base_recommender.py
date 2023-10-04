from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseBookRecommender(ABC):

    @abstractmethod
    def recommend(self, book_scores: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        pass
