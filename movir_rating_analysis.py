#MovieLens 1M Data Set

import pandas as pd
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('users.dat', sep='::', header=None, names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('ratings.dat', sep='::', header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('movies.dat', sep='::', header=None, names=mnames)

data = pd.merge(pd.merge(ratings, users), movies)

data[:5]
data.ix[0]

mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc=mean)

#filter down to movies that received at least 250 ratings
ratings_by_title = data.groupby('title').size()
active_titles = ratings_by_title[ratings_by_title >=250]

mean_ratings = mean_ratings.ix[active_titles]

#sorting
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)

#Measuring rating disagreement
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')

#Reversing the order of the rows and again slicing off the top 15 rows, we get the movies
#preferred by men that women didn’t rate as highly
sorted_by_diff[::-1][:15]

# Standard deviation of rating grouped by title
rating_std_by_title =  data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.ix[active_titles]

# Order Series by value in descending order
rating_std_by_title.order(ascending=False)[:10]



