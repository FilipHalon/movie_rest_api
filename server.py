from flask import Flask, request, render_template, redirect, url_for
from psycopg2 import connect
from csv_process import tag_list
import re

app = Flask(__name__)

conn = connect(user="movies",
               password='movies',
               host="127.0.0.1",
               database="moviesdb")

cur = conn.cursor()

@app.route('/')
def index():
    return redirect(url_for('movie_page'))

@app.route('/movies/', methods=['GET', 'POST'])
def movie_page():

    if request.method == 'GET':
        cur.execute("SELECT * FROM movies")
        movies_list = cur.fetchall()
        tags = tag_list
        return render_template("movies.html", movie_list=movies_list, tags=tags)

    elif request.method == 'POST':

        if 'year' in request.form:
            cur.execute(f"SELECT * FROM movies WHERE year LIKE \'%{request.form['year']}%\'" )
            movies_list = cur.fetchall()
            tags = tag_list
            return render_template("movies.html", movie_list=movies_list, tags=tags)

        elif 'sort' in request.form:

            if request.form["sort"] == "ascending":
                cur.execute("SELECT * FROM movies ORDER BY year asc")
                movies_list = cur.fetchall()
                tags = tag_list
                return render_template("movies.html", movie_list=movies_list, tags=tags)

            elif request.form["sort"] == 'descending':
                cur.execute("SELECT * FROM movies ORDER BY year desc")
                movies_list = cur.fetchall()
                tags = tag_list
                return render_template("movies.html", movie_list=movies_list, tags=tags)

        elif 'tag1' in request.form:
            cur.execute(f"SELECT * FROM movies WHERE tags LIKE \'%{request.form['tag1']}%\' AND tags LIKE \'%{request.form['tag2']}%\'")
            movies_list = cur.fetchall()
            tags = tag_list
            return render_template("movies.html", movie_list=movies_list, tags=tags)

@app.route('/movie/<string:movieId>')
def get_a_movie(movieId):
    cur.execute(f"SELECT * FROM movies WHERE movie_id = \'{movieId}\'")
    movie_id = cur.fetchall()
    cur.execute(f"SELECT imdbId FROM movies WHERE movie_id = \'{movieId}\'")
    link = str(cur.fetchall())
    #link = ''.join(link)
    #link = re.match(r'(\d+)', link)
    return render_template("movie.html", movie_id=movie_id, link=link)

@app.route('/db', methods=['POST'])
def db():
    cur.execute("DELETE FROM movies")

if __name__ == '__main__':
    app.run(debug=True)
