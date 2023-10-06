-- database/init.sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    authors TEXT,
    image TEXT,
    previewLink TEXT,
    publisher TEXT,
    publishedDate TEXT,
    infoLink TEXT,
    categories TEXT,
    ratingsCount FLOAT
);

COPY books(title, description, authors, image, previewLink, publisher, publishedDate, infoLink, categories, ratingsCount)
FROM '/data/books_data.csv' DELIMITER ',' CSV HEADER;
