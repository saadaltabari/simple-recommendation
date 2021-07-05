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


def _save_dataframe_as_csv(df: pd.DataFrame, file_name: str) -> None:
	"""
	Write the contents of the provided DataFrame
	to a csv file.

	:param df: pandas.DataFrame, the data that will
	be saved to a csv file.
	:param file_name: str, the name of the csv file
	the data will be saved to.
	:return:
	"""
	df.to_csv(f"./files/{file_name}.csv")


if __name__ == '__main__':
	# Task 1 - Separate Movie IDs and Movie names.
	_separate_movie_id_name()
	_save_dataframe_as_csv(
		df=user_ratings,
		file_name='UpdatedMovieIDs'
	)
	print("Separated Movie IDs and Movie names. Output in "
		  "file UpdatedMovieIDs.csv")

	# Task 2 - Capitalizing the first letter of
	# every word in the movie names.
	_capitalize_movie_names()
	_save_dataframe_as_csv(
		df=user_ratings,
		file_name='CapitalizedMovieNames'
	)
	print("Capitalized all movie names. Output in file "
		  "CapitalizedMovieNames.csv")

	# Task 3 - Read in from your new CSV file
	# from Task 2 and parse data into
	# lists and dictionaries
	_construct_age_ratings_dict()
	print("Parsed ratings data into dictionary.")

	# Task 4 - Find the recommended movies for
	# a given age from best to worst ratings
	_update_recommendation_list()
	print("Recommended movies to all users in the NewUsers.csv file")

	# Task 5 - Recommend movies to users in the
	# second input file.
	_save_dataframe_as_csv(
		df=movie_recommendations,
		file_name='results'
	)
	print("Saved recommended movies to the results.csv file.")
