from databases import Database
import os

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)

async def connect():
    await database.connect()

async def disconnect():
    await database.disconnect()

async def get_book_titles_by_ids(book_ids: list) -> dict:
    query = "SELECT id, title FROM books WHERE id = ANY(:ids)"
    results = await database.fetch_all(query, {"ids": book_ids})
    
    # Transform the results into a dictionary with book IDs as keys and titles as values.
    return {record["id"]: record["title"] for record in results}