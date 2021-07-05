import pandas as pd


user_ratings = pd.read_csv('./files/RatingsInput.csv')
rating_by_age_dict = {}
movie_recommendations = pd.read_csv('./files/NewUsers.csv')


def _separate_movie_id_name():
	movie_name_parts = user_ratings['MovieName'].str.split(',')
	user_ratings['MovieID'] = movie_name_parts.str[0]
	user_ratings['MovieName'] = movie_name_parts.str[1:].str.join(',')


def _capitalize_movie_names():
	user_ratings['MovieName'] = user_ratings['MovieName'].str.title()


def _construct_age_ratings_dict():
	for index, row in user_ratings.iterrows():
		age_rating = rating_by_age_dict.get(row['UserAge'], {})
		movies = age_rating.get(row['Rating'], [])
		movies.append(row['MovieName'])
		age_rating[row['Rating']] = movies
		rating_by_age_dict[row['UserAge']] = age_rating


def _recommend_movies(user_age, max_recommendations):

	def closest_user_age():
		if user_age in rating_by_age_dict:
			return user_age
		return min(
			rating_by_age_dict.keys(),
			key=lambda x: abs(x - user_age)
		)

	recommended_movies = []
	user_age = closest_user_age()
	rating = 5
	while len(recommended_movies) < max_recommendations and rating > 2:
		recommended_movies.extend(
			rating_by_age_dict[user_age].get(rating, [])
		)
		rating -= 1

	for i in range(len(recommended_movies) - max_recommendations):
		recommended_movies.pop()

	return recommended_movies


def _update_recommendation_list():
	movie_recommendations['Movies'] =\
		movie_recommendations.apply(
			lambda row: _recommend_movies(row.UserAge, row.NoOfMoviesToRecommend),
			axis=1
		).str.join(', ')


def _save_recommendations():
	movie_recommendations.to_csv('./files/results.csv')


if __name__ == '__main__':
	_separate_movie_id_name()
	_capitalize_movie_names()
	_construct_age_ratings_dict()
	_update_recommendation_list()
	_save_recommendations()
