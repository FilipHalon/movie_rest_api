from psycopg2 import connect, OperationalError
# import csv
# from csv_process import movies_csv
# from sqlalchemy import create_engine

try:
    conn = connect(user="movies",
                  password='movies',
                  host="127.0.0.1",
                  database="moviesdb")

    print("Connected to the database.")

    cur = conn.cursor()

    create_movies = """CREATE TABLE movies
                        (
                        movie_id    varchar(255)      PRIMARY KEY,
                        title       varchar(255),
                        genres      varchar(255),
                        year        varchar(255),
                        imdbId      varchar(255),
                        tags        varchar(10000),
                        rating      varchar(255)
                        )"""


    cur.execute(create_movies)
    conn.commit()

    f = open("movies_csv.csv", 'r')

    cur.copy_from(f, 'movies', '\t')
    conn.commit()

    # engine = create_engine('postgresql://movies:movies@localhost/moviesdb')
    # movies_csv.to_sql('movies1', engine)

    # cur.execute("DROP TABLE movies")
    # conn.commit()

    cur.close()
    conn.close()

except OperationalError:
    print("Unable to connect to the database.")