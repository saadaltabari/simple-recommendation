import pandas as pd

user_ratings = pd.read_csv('~/Downloads/RatingsInput.csv')
rating_by_age_dict = {}
movie_recommendations = pd.read_csv('~/Downloads/NewUsers.csv')


def separate_movie_id_name():
	movie_name_parts = user_ratings['MovieName'].str.split(',')
	user_ratings['MovieID'] = movie_name_parts.str[0]
	user_ratings['MovieName'] = movie_name_parts.str[1:].str.join(',')


def capitalize_movie_names():
	user_ratings['MovieName'] = user_ratings['MovieName'].str.title()


def construct_age_ratings_dict():
	for index, row in user_ratings.iterrows():
		age_rating = rating_by_age_dict.get(row['UserAge'], {})
		movies = age_rating.get(row['Rating'], [])
		movies.append(row['MovieName'])
		age_rating[row['Rating']] = movies
		rating_by_age_dict[row['UserAge']] = age_rating


def __closest_user_age(user_age):
	if user_age in rating_by_age_dict:
		return user_age
	return min(
		rating_by_age_dict.keys(),
		key=lambda x: abs(x - user_age)
	)


def recommend_movies(user_age, max_recommendations):
	recommended_movies = []
	user_age = __closest_user_age(user_age)
	rating = 5
	while len(recommended_movies) < max_recommendations and rating > 2:
		recommended_movies.extend(
			rating_by_age_dict[user_age].get(rating, [])
		)
		rating -= 1

	for i in range(len(recommended_movies) - max_recommendations):
		recommended_movies.pop()

	return recommended_movies


def update_recommendation_list():
	movie_recommendations['Movies'] =\
		movie_recommendations.apply(
			lambda row: recommend_movies(row.UserAge, row.NoOfMoviesToRecommend),
			axis=1
		).str.join(', ')


def save_recommendations():
	movie_recommendations.to_csv('./recommendations.csv')


if __name__ == '__main__':
	separate_movie_id_name()
	capitalize_movie_names()
	construct_age_ratings_dict()
	update_recommendation_list()
	save_recommendations()
