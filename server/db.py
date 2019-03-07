from mongoengine import connect, Document, StringField, IntField, DictField
from flask import url_for

class Character(Document):
	""" Store the data for a character. """
	name = StringField(required=True, primary_key=True)
	picture = StringField(required=True)
	list_of_songs = DictField(required=True)
	count = IntField(required=True)
	def __init__(self, name, picture, list_of_songs, *args, **values):
		super().__init__(*args, **values)
		self.name = name
		self.picture = picture
		self.list_of_songs = list_of_songs
		if self.count is None:
			self.count = 0
	def incr_count(self):
		self.count += 1

def db_connect():
	""" Connect to the database using the parameters stored in the config file. """
	config_file = open("conf/config.txt").read().splitlines()
	config = dict()
	for line in config_file:
		line = line.split(" ")
		config[line[0]] = line[2]
	host = "mongodb://" + config["db_user"] + ":" + config["db_password"] + "@" + \
		   config["ds_number"] + ".mlab.com:" + config["port"] + "/" + config["db_name"]
	connect(host=host)

def add_character(name, picture, list_of_songs):
	""" Add a character and their list of songs. """
	name = name.lower()
	char = Character(name, picture, list_of_songs)
	char.save()

def add_characters(chars_and_songs, chars_and_pics):
	""" Add a list of characters and their songs. """
	for name in chars_and_songs:
		char_and_songs = chars_and_songs[name]
		picture = chars_and_pics[name]
		add_character(name, picture, char_and_songs)

def get_all_count():
	""" Retrieve all character counts. Used for the Analytics. """
	count_list = []
	chars = Character.objects()
	chars_and_pictures = dict()
	chars_and_picture_list = []
	for char in chars:
		count_list.append(char.count)
	return count_list


def get_all_char_name():
	""" Retrieve all character names """
	name_list = []
	chars = Character.objects()
	chars_and_pictures = dict()
	chars_and_picture_list = []
	for char in chars:
		name_list.append(char.name)
	return name_list

def get_one_character(char_name):
	""" Return a character name a link to picture. """
	char_name = char_name.lower()
	chars = Character.objects(name=char_name)
	if len(chars) == 0:
		return None
	char = chars[0]
	name = char.name
	picture = char.picture
	char_and_picture = dict()
	char_and_picture["char_name"] = name
	return char_and_picture

def get_all_characters(base_url):
	""" Return all of the characters. """
	chars = Character.objects()
	chars_and_pictures = dict()
	chars_and_picture_list = []
	for char in chars:
		name = char.name
		picture = char.picture
		char_and_picture = dict()
		char_and_picture["char_name"] = name
		url_suffix = url_for("get_picture", name=name)
		url = base_url + url_suffix
		char_and_picture["img_link"] = url
		chars_and_picture_list.append(char_and_picture)
	chars_and_pictures["characters"] = chars_and_picture_list
	return chars_and_pictures

def get_nbr_of_characters():
	""" Return the number of characters in the database. """
	chars = Character.objects()
	return len(chars)

def get_songs_from_names(char_names):
	""" Return a list of songs given name. """
	chars_and_songs = dict()
	chars_and_songs_list = []
	for char_name in char_names:
		char_name = char_name.lower()
		chars = Character.objects(name=char_name)
		if len(chars) == 0:
			return None, False
			continue
		char = chars[0]

		char.incr_count()
		char.save()

		songs = char.list_of_songs
		char_and_song = dict()
		char_and_song["char_name"] = char_name
		char_and_song["songs"] = songs["songs"]
		chars_and_songs_list.append(char_and_song)
	chars_and_songs["characters"] = chars_and_songs_list
	return chars_and_songs, True

def get_picture_from_name(char_name):
	""" Return a picture given a name. """
	char = char_name.lower()
	chars = Character.objects(name=char)
	if len(chars) == 0:
		return None
	char = chars[0]
	picture = char.picture
	return picture
