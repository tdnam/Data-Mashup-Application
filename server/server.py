from flask import Flask, request, send_file, url_for
from flask_restful import reqparse
from flask_cors import CORS
from model import *
from db import *
from parser import *
from http_responses import *
from image_parser import *
from analytics import *
from datasets import *

def setup():
	""" Setup the initial things for the server. This includes connecting
	to the database, parsing the input to get the list of songs for each
	character, and populating the database (if the database is not already
	populated). """
	print("Starting setup...")
	print("Connecting to database...")
	db_connect()
	print("Downloading datasets...")
	download_datasets()
	nbr_of_characters = get_nbr_of_characters()
	if nbr_of_characters >= len(custom_chars):
		print("Setup complete")
		return
	print("Getting pictures...")
	resize_pictures()
	chars_and_pics = get_pictures()
	print("Parsing the text file...")
	chars_and_talk = parse_textfile()
	print("Getting songs from last fm and then YouTube...")
	chars_and_songs = get_songs_from_last_fm_and_youtube(chars_and_talk)
	print("Adding characters to the database...")
	add_characters(chars_and_songs, chars_and_pics)
	print("Setup complete!")

protocol = "http://"
host = "127.0.0.1"
port = 5000
base_url = protocol + host + ":" + str(port)
app = Flask(__name__)
CORS(app)
setup()

def get_accept_type(request):
	""" Return the accept type that the user has provided for the
	return value. application/json will be used if nothing is set. """
	accept_type = request.headers.getlist('accept')[0]
	if accept_type == "*/*":
		# If not specified, will be set to JSON.
		accept_type = "application/json"
	return accept_type

@app.route('/character/<name>', methods=['GET'])
def get_character(name):
	""" Return a list of characters and their info. """
	try:
		accept_type = get_accept_type(request)
		url_suffix = url_for("get_picture", name=name.lower())
		url = base_url + url_suffix
		char = get_one_character(name)
		if char is None:
			return resource_not_found()
		char["img_link"] = url
		return return_object(char, accept_type)
	except:
		return server_error()

@app.route('/characters', methods=['GET'])
def get_characters():
	""" Return a list of characters and their info. """
	try:
		accept_type = get_accept_type(request)
		chars = get_all_characters(base_url)
		return return_object(chars, accept_type)
	except:
		return server_error()

@app.route('/picture/<name>', methods=['GET'])
def get_picture(name):
	""" Return the picture corresponding to a given character. """
	try:
		accept_type = get_accept_type(request)
		picture = get_picture_from_name(name)
		if picture is None:
			return resource_not_found()
		return send_file(picture, mimetype='image/gif')
	except:
		return server_error()

@app.route('/songs', methods=['GET'])
def get_songs():
	""" Return a list of songs, based on the sent in characters. """
	try:
		accept_type = get_accept_type(request)
		parser = reqparse.RequestParser()
		parser.add_argument('characters', type=str)
		args = parser.parse_args()
		characters = args.get("characters")
		if characters is None:
			return field_names_incorrect()
		characters = characters.split("|")
		list_of_songs, all_exists = get_songs_from_names(characters)
		if not all_exists:
			return resources_not_found()
		return return_object(list_of_songs, accept_type)
	except:
		return server_error()

@app.route('/analytics', methods=['GET'])
def get_analytics_characters():
	""" Return statistics in a bar graph regarding how many times
	each character has been called.
	"""
	try:
		accept_type = get_accept_type(request)
		get_analytics()
		return return_analytics(accept_type)
	except:
		return server_error()

if __name__ == "__main__":
	app.run(host=host, port=port)
