import pandas as pd
import re

# def preprocess():

# reading the csv files
movies_csv = pd.read_csv('./ml-latest-small/movies.csv')
links_csv = pd.read_csv('./ml-latest-small/links.csv')
tags_csv = pd.read_csv('./ml-latest-small/tags.csv')
ratings_csv = pd.read_csv('./ml-latest-small/ratings.csv')

# splitting values in the second column to 2 different columns
scnd_col = movies_csv['title']
scnd_col_title = [re.findall("([\w\W]+) \(", row) for row in scnd_col]
scnd_col_year = [re.findall("\((\w+)\)", row) for row in scnd_col]

# turning the third column into a list
thrd_col = movies_csv['genres']
thrd_col_list = [row.split('|') for row in thrd_col]

# putting everything back together
movies_csv['title'] = scnd_col_title
movies_csv['genres'] = thrd_col_list
movies_csv.insert(3, 'year', 'year')
movies_csv['year'] = scnd_col_year

# merging links with movies
movies_csv = movies_csv.merge(links_csv.loc [:, ['movieId', 'imdbId']], on='movieId')

# making a dictionary of tags and merging it with movies
tags = {}

for row in tags_csv["movieId"]:
    if row not in tags:
        tags.update({f'{row}': []})

for row_num in range(len(tags_csv)):
    movie_row = tags_csv["movieId"][row_num]
    tag_row = tags_csv['tag'][row_num]
    if tag_row not in tags[f'{movie_row}']:
        tags[f'{movie_row}'].append(tag_row)

tags_df = pd.DataFrame()
tags_df['movieId'] = tags.keys()
tags_df['movieId'] = tags_df['movieId'].astype(int)
tags_df['tags'] = tags.values()

movies_csv = movies_csv.merge(tags_df.loc [:, ['movieId', 'tags']], on='movieId', how='left')

# preparing a uniform list of tags
tag_list = []

for key in tags:
    for value in tags[key]:
        if value not in tag_list:
            tag_list.append(value)

# counting ratings for the movies
ratings = {}

for row in ratings_csv["movieId"]:
    if row not in ratings:
        ratings.update({f'{row}': []})

for row_num in range(len(ratings_csv)):
    ratings[f'{ratings_csv["movieId"][row_num]}'].append(ratings_csv['rating'][row_num])

for key in ratings:
    ratings[key] = round(sum(ratings[key])/len(ratings[key]), 2)

# merging the ratings with movies

ratings_df = pd.DataFrame()
ratings_df['movieId'] = ratings.keys()
ratings_df['movieId'] = ratings_df['movieId'].astype(int)
ratings_df['rating'] = ratings.values()

movies_csv = movies_csv.merge(ratings_df.loc [:, ['movieId', 'rating']], on='movieId', how='left')

# changing NaN to NULL
movies_csv = movies_csv.fillna('NULL')

# to csv
movies_csv.to_csv(r'movies_csv.csv', sep='\t', index=False)

    # return tag_list
