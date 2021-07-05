import pandas as pd

# Read the user ratings csv file into a pandas DataFrame
user_ratings = pd.read_csv('./files/RatingsInput.csv')

# Initialize the dictionary includes all user ratings
# index by user age
rating_by_age_dict = {}

# Read the new user's (users to recommend for) csv file
# into a Pandas DataFrame
movie_recommendations = pd.read_csv('./files/NewUsers.csv')


def _separate_movie_id_name() -> None:
	"""
	Separate the movie id and movie name columns
	in the user_ratings DataFrame
	:return:
	"""
	movie_name_parts = user_ratings['MovieName'].str.split(',')
	user_ratings['MovieID'] = movie_name_parts.str[0]
	user_ratings['MovieName'] = movie_name_parts.str[1:].str.join(',')


def _capitalize_movie_names() -> None:
	"""
	Capitalize the first letters of all words
	of the movie names in the user_ratings DataFrame
	:return:
	"""
	user_ratings['MovieName'] = user_ratings['MovieName'].str.title()


def _construct_age_ratings_dict() -> None:
	"""
	Updates the rating_by_age_dict dictionary with
	all data processed from the user_ratings DataFrame
	:return:
	"""
	for index, row in user_ratings.iterrows():
		age_rating = rating_by_age_dict.get(row['UserAge'], {})
		movies = age_rating.get(row['Rating'], [])
		movies.append(row['MovieName'])
		age_rating[row['Rating']] = movies
		rating_by_age_dict[row['UserAge']] = age_rating


def _recommend_movies(user_age, max_recommendations) -> list:
	"""
	Returns a list of recommend movies from the rating_by_age_dict
	based on the given user_age.

	:param user_age: int, the age of the user to recommend movies
	for.
	:param max_recommendations: int, the maximum number of movies
	to recommend for the user.
	:return: list of str, names of the movies recommended for the user.
	"""

	def closest_user_age():
		"""
		The user age to consider for the user.
		If user age is not present in the
		rating_by_age_dict, return the closest
		age available.
		:return: int, user age.
		"""
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


def _update_recommendation_list() -> None:
	"""
	Update the movies column of the movie_recommendations
	DataFrame with the recommended movies list.
	:return:
	"""
	movie_recommendations['Movies'] =\
		movie_recommendations.apply(
			lambda row: _recommend_movies(row.UserAge, row.NoOfMoviesToRecommend),
			axis=1
		).str.join(', ')


def _save_recommendations() -> None:
	"""
	Write the movie_recommendations DataFrame
	to a csv file.
	:return:
	"""
	movie_recommendations.to_csv('./files/results.csv')


if __name__ == '__main__':
	_separate_movie_id_name()
	_capitalize_movie_names()
	_construct_age_ratings_dict()
	_update_recommendation_list()
	_save_recommendations()
