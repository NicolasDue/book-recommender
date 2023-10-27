from typing import List, Tuple
import pandas as pd
from db_handler import get_book_titles_by_ids, get_book_ids_by_titles
from .base_recommender import BaseBookRecommender


class CollaborativeFilteringRecommender(BaseBookRecommender):
    """
    Recommender class that employs collaborative filtering.
    Reads and stores book data and ratings for efficient recommendations.
    """

    def __init__(self) -> None:
        """
        Initialize the CollaborativeFilteringRecommender instance.
        
        Reads the books_data.csv and Books_rating.csv files once and stores them.
        Fetches the title-to-ID mapping from the database and stores it.
        """

        # Load ratings data and keep only necessary columns
        reviews_data = pd.read_csv('data/raw/Books_rating.csv', usecols=['Id', 'Title', 'User_id', 'review/score', 'review/time'])

        # Drop duplicates and sort by review time
        reviews_data = (reviews_data
                        .sort_values('review/time', ascending=False)
                        .drop_duplicates(subset=['Id', 'User_id']))

        # Filter users who have given more than one unique score
        user_unique_scores = reviews_data.groupby("User_id")["review/score"].nunique()
        valid_users = user_unique_scores[user_unique_scores > 1].index
        reviews_data = reviews_data[reviews_data.User_id.isin(valid_users)]

        # Calculate user average score and deviation from average
        user_avg_score = reviews_data.groupby("User_id")["review/score"].transform('mean')
        reviews_data['dev'] = reviews_data["review/score"] - user_avg_score

        # Drop users with suspiciously high numbers of reviews (e.g., more than 30)
        user_review_count = reviews_data.groupby("User_id").size()
        less_suspicious_users = user_review_count[user_review_count < 30].index
        reviews_data = reviews_data[reviews_data.User_id.isin(less_suspicious_users)]

        # Create final ratings DataFrame
        self.books_rating = reviews_data[['Id', 'User_id', 'dev']]

        # Create a DataFrame containing unique book Ids and Titles
        self.reviews_titles = reviews_data[['Id', 'Title']].drop_duplicates()


    async def recommend(self, book_scores: List[Tuple[int, float]], size: int) -> List[Tuple[int, float]]:
        """
        Recommend books based on the provided book_scores.
        
        Parameters:
            book_scores (List[Tuple[int, float]]): List of tuples containing book IDs and their scores.
            size (int): The number of recommendations to return.
            
        Returns:
            List[Tuple[int, float]]: List of recommended book IDs and their scores.
        """
        
        # Step 1: Map Database IDs to File IDs
        book_ids = [book_id for book_id, _ in book_scores]
        title_dict = await get_book_titles_by_ids(book_ids)
        file_id_dict = (self.reviews_titles[self.reviews_titles['Title'].isin(title_dict.values())]
                        .set_index('Title')['Id'].to_dict())
        file_id_map = {db_id: file_id_dict[title] for db_id, title in title_dict.items()}
        
        # Step 2: Filter Relevant Reviews
        book_scores_file_id = {file_id_map[db_id]: score for db_id, score in book_scores}
        relevant_reviews = self.books_rating[self.books_rating['Id'].isin(book_scores_file_id.keys())]
        
        # Step 3: Create User-Item Matrix
        user_item_matrix = relevant_reviews.pivot_table(index='User_id', columns='Id', values='dev')
        
        # Step 4: Calculate User Similarities
        input_scores = pd.Series(book_scores_file_id)
        dev_input_scores = input_scores - input_scores.mean()
        user_similarity = user_item_matrix.apply(lambda row: row.corr(dev_input_scores), axis=1).dropna()
        
        # Step 5: Weighted Scores for Recommendations
        weighted_scores = (self.books_rating[self.books_rating['User_id'].isin(user_similarity.index)]
                        .merge(user_similarity.rename('user_weight'), left_on='User_id', right_index=True)
                        .assign(weighted_score=lambda df: df['dev'] * df['user_weight'])
                        .groupby('Id')['weighted_score'].sum())
        
        # Step 6: Finalize Recommendations
        top_recommendations = (self.reviews_titles
                            .merge(weighted_scores.rename('score'), left_on='Id', right_index=True)
                            .sort_values('score', ascending=False)
                            .head(size))
        
        db_id_dict = await get_book_ids_by_titles(top_recommendations['Title'].tolist())  
        result = [(db_id_dict[row['Title']], row['score']) for _, row in top_recommendations.iterrows()]
        
        return result
