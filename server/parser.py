import pandas as pd
import numpy as np
from db import *

simpsons_text_folder = "datasets/the-simpsons-by-the-data/"
simpsons_characters = simpsons_text_folder + "simpsons_characters.csv"
simpsons_script_lines = simpsons_text_folder + "simpsons_script_lines.csv"

custom_chars = {
				"marge_simpson", "bart_simpson", "lisa_simpson",
				"moe_szyslak", "ned_flanders", "grampa_simpson",
				"chief_wiggum", "milhouse_van_houten", "waylon_smithers",
				"nelson_muntz", "edna_krabappel-flanders", "selma_bouvier",
				"barney_gumble", "patty_bouvier", "homer_simpson",
				"cletus_spuckler", "gil_gunderson", "apu_nahasapeemapetilon",
				"c_montgomery_burns", "krusty_the_clown", "snake_jailbird",
				"ralph_wiggum"
				}

def calculate_tf_idf_scores(tfs, idfs):
	""" Given tfs values and idfs values, calculate the tf_idf scores. """
	tf_idf_scores = dict()
	for word in tfs:
		tf_idf_scores[word] = tfs[word] * idfs[word]
	return tf_idf_scores

def calculate_idfs(tfs, N):
	""" Given the tfs and the number of documents, get the idf values. """
	idfs = dict()
	for name in tfs:
		char_data = tfs[name]
		for word in char_data:
			if word in idfs:
				idfs[word] += 1
			else:
				idfs[word] = 1
	for word in idfs:
		idfs[word] = np.log(N/idfs[word])
	return idfs

def tokens_to_probs(data):
	""" Transforms the tokens into a dict containing the
	probability of each token.
	"""
	tokens = {}
	count = 0
	for word in data:
		count += 1
		if word in tokens:
			tokens[word] += 1
		else:
			tokens[word] = 1
	for pair in tokens:
		tokens[pair] /= count
	return tokens

def char_words(character, data_script_lines, custom_chars_index):
	""" Get the words from a character. Unnecesary words are removed. """
	chosen_char_id = custom_chars_index[character]
	char_cvs_cells = data_script_lines[data_script_lines["character_id"]==str(chosen_char_id)]
	char_lines = list(char_cvs_cells["normalized_text"].values.astype(str))
	# Transform into one big string:
	char_lines_one_str = ' '.join(char_lines)
	words = char_lines_one_str.split(" ")
	# Remove '--' and digits from words.
	words = [x for x in words if x != '--']
	words = [word[:-2] if word.endswith('--') else word for word in words]
	words = [word[2:] if word.startswith('--') else word for word in words]
	words = [x for x in words if not (x.isdigit())]
	return words

def calculate_tfs(data_script_lines, custom_chars_index):
	""" Find the term frequencies for a character given its name. """
	tfs = dict()
	for name in custom_chars_index:
		words_char = char_words(name, data_script_lines, custom_chars_index)
		tfs_char = tokens_to_probs(words_char)
		tfs[name] = tfs_char
	return tfs

def make_custom_chars_index(df_char_index):
	""" Make a dictionary that maps each character to their id in the cvs. """
	custom_chars_index = dict()
	for name in custom_chars:
		name_with_spaces = ' '.join(name.split("_"))
		id_row = df_char_index[df_char_index["normalized_name"] == name_with_spaces]["id"]
		if len(id_row) == 0:
			continue
		id = id_row.values.astype(int)[0]
		custom_chars_index[name] = id
	return custom_chars_index

def parse_textfile():
	""" Parse the dataset input and return a sorted list
	of characteristic words for each character.
	"""
	df_char_index = pd.read_csv(simpsons_characters)
	custom_chars_index = make_custom_chars_index(df_char_index)
	data_script_lines = pd.read_csv(simpsons_script_lines,
		error_bad_lines=False,
		warn_bad_lines=False,
		low_memory=False)

	tfs = calculate_tfs(data_script_lines, custom_chars_index)
	idfs = calculate_idfs(tfs, len(custom_chars_index))
	chars_and_talk = dict()
	for name in custom_chars_index:
		tf_idf_scores = calculate_tf_idf_scores(tfs[name], idfs)
		sorted_words_and_tf_idf = sorted(tf_idf_scores.items(), key=lambda x: x[1], reverse=True)
		sorted_words = [x[0] for x in sorted_words_and_tf_idf]
		chars_and_talk[name] = sorted_words
	return chars_and_talk
