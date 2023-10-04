FROM postgres:13

COPY init.sql /docker-entrypoint-initdb.d/
COPY books_data.csv /data/

# Additional steps to insert data from CSV to the database can be added.
