import cv2
import os
from parser import *

clean_folder = "cleaned_pictures/"
simpsons_picture_folder_pics = "datasets/the-simpsons-characters-dataset/simpsons_dataset/"
fileformat = ".jpg"

def find_matching_folder(character):
	""" Find the matching picture folder corresponding to the character.
	First the first name is compared, then the second name, and so on.
	"""
	char_names = character.lower().split("_")
	for char_name in char_names:
		for folder_name in os.listdir(simpsons_picture_folder_pics):
			parts_of_folder_name = folder_name.split("_")
			if char_name in parts_of_folder_name:
				return folder_name
	return None

def find_matching_picture(folder_path, folder_name):
	""" Find the first best matching photo. Only the dimension matters.
	The picture has to have a larger height than width. """
	for pic in os.listdir(folder_path):
		path_unclean = simpsons_picture_folder_pics + folder_name + "/" + pic
		img = cv2.imread(path_unclean)
		height, width, channels = img.shape
		if height > width:
			return img
	return None

def resize_pictures():
	""" Find the first picture for each character and resize it. """
	os.makedirs(clean_folder, exist_ok=True)
	if len(os.listdir(clean_folder)) >= len(custom_chars):
		return
	for character in custom_chars:
		folder_name = find_matching_folder(character)
		if folder_name is None:
			continue
		folder_path = simpsons_picture_folder_pics + folder_name
		clean_filename = character + fileformat
		path_clean = clean_folder + clean_filename
		img = find_matching_picture(folder_path, folder_name)
		if img is None:
			continue
		resized = cv2.resize(img, (480, 640))
		cv2.imwrite(path_clean, resized)

def get_pictures():
	""" Retrieve the corresponding image to each character. """
	chars_and_pics = dict()
	for character in custom_chars:
		filename = character + fileformat
		path_clean = clean_folder + filename
		chars_and_pics[character] = path_clean
	return chars_and_pics
