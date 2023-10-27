from databases import Database
import os
from typing import List, Dict

DATABASE_URL: str = os.getenv("DATABASE_URL")
database: Database = Database(DATABASE_URL)

async def connect() -> None:
    """Establish a database connection."""
    await database.connect()

async def disconnect() -> None:
    """Close the database connection."""
    await database.disconnect()

async def get_book_titles_by_ids(book_ids: List[int]) -> Dict[int, str]:
    """
    Fetch book titles from the database by their IDs.
    
    Parameters:
        book_ids (List[int]): List of book IDs.
        
    Returns:
        Dict[int, str]: Dictionary with book IDs as keys and titles as values.
    """
    query: str = "SELECT id, title FROM books WHERE id = ANY(:ids)"
    results = await database.fetch_all(query, {"ids": book_ids})
    
    return {record["id"]: record["title"] for record in results}

async def get_book_id_title_mapping() -> Dict[str, int]:
    """
    Fetch title-to-ID mapping from the database.
    
    Returns:
        Dict[str, int]: Dictionary with book titles as keys and IDs as values.
    """
    query: str = "SELECT id, title FROM books"
    results = await database.fetch_all(query)
    return {record["title"]: record["id"] for record in results}


async def get_book_ids_by_titles(book_titles: List[str]) -> Dict[str, int]:
    """
    Fetch book IDs from the database by their titles.
    
    Parameters:
        book_titles (List[str]): List of book titles.
        
    Returns:
        Dict[str, int]: Dictionary with book titles as keys and IDs as values.
    """
    query: str = "SELECT id, title FROM books WHERE title = ANY(:titles)"
    results = await database.fetch_all(query, {"titles": book_titles})
    
    return {record["title"]: record["id"] for record in results}
