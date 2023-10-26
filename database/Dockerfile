FROM postgres:13

COPY database/init.sql /docker-entrypoint-initdb.d/
COPY data/raw/books_data.csv /data/
