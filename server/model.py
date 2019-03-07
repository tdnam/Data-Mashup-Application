import argparse
import httplib2
import os.path
from configparser import SafeConfigParser
import requests, json
# Google Data API
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from apiclient.discovery import build
import oauth2client
from db import *

youtube = None
API_KEY = '190ed5e7d77b9f55eb52777f87d8bb88'
client_secret_path = "conf/client_secret.json"
oauth2_path = "conf/oauth2.json"
settings_path = "conf/settings.cfg"
nbr_songs_for_each_char = 10

def get_songs_from_last_fm_and_youtube(chars_and_talk):
	""" Call last.fm to get the tracks, given a list of words
	for each character. Then, call YouTube using the song name and
	artist as a query and take the first match.
	"""
	setup = load_setup_values()
	create_youtube_service(setup)
	chars_and_songs = dict()
	for name in chars_and_talk:
		print("\tCurrently processing: ", name)
		words = chars_and_talk[name]
		char_and_songs = dict()
		list_of_songs = []
		for word in words:
			tracks = get_tracks_from_last_fm(word)
			if len(tracks) > 0:
				song_name = str(list(tracks)[0])
				artist = tracks[song_name]
				artist_name = artist["name"]

				# Find song on YouTube.
				query = song_name + " " + artist_name
				youtube_id = search_youtube_id_by_name(query)
				if youtube_id == None:
					continue
				song = dict()
				song["name"] = song_name
				song["artist"] = artist_name
				song["youtube_id"] = youtube_id
				list_of_songs.append(song)

			if len(list_of_songs) >= nbr_songs_for_each_char:
				char_and_songs["songs"] = list_of_songs
				chars_and_songs[name] = char_and_songs
				break
	return chars_and_songs

def get_tracks_from_last_fm(tag):
	""" Given a tag, call last.fm and get the best track. """
	tracks_json = requests.get(
		'http://ws.audioscrobbler.com//2.0/?method=tag.gettoptracks&tag=' + tag + '&api_key=' + API_KEY + '&format=json')

	tracks_json = tracks_json.text  # convert response to string
	tracks_json = json.loads(tracks_json)  # convert string to dict

	tracks = tracks_processing(tracks_json)
	return tracks

########### LAST.FM API STUFF ############
def tracks_processing(tracks_json):
	""" Process tracks that collected from /getTopTrack to push to DB later. """
	temp_new_tracks = {} #filter only song information
	new_tracks = {}
	for key,val in tracks_json['tracks'].items():
		for v in val:
			if not isinstance(v, str):
				song_name = v['name']
				v.pop('name', None)
				temp_new_tracks[song_name] = v

	for song in temp_new_tracks:
		new_tracks[song] = temp_new_tracks[song]['artist']

	for song in new_tracks:
		new_tracks[song].pop('mbid',None)
		new_tracks[song].pop('url', None)
	return new_tracks

############# YOUTUBE API SEARCH ##################
def search_youtube_id_by_name(query):
	""" Return the first found video in the search. """
	res = youtube.search().list(
		q=query,
		part="id,snippet",
		maxResults=3,
		safeSearch="none",
		type="video",
		fields="items"
	).execute()

	videos = res.get('items', [])
	if not videos:
		return None
	for video in videos:
		if video['id']['kind'] == 'youtube#video':
			return video['id']['videoId']
		else:
			print("Result is not a video, continuing to next result")
	return None

def create_youtube_service(setup):
	""" Create Youtube instance. """
	global youtube
	SCOPE = "https://www.googleapis.com/auth/youtube"
	SERVICE_NAME = "youtube"
	VERSION = "v3"
	secret_file = os.path.dirname(os.path.realpath(__file__)) + '/' + client_secret_path
	MISSING_SECRETS_MESSAGE = "Error: {0} is missing".format(secret_file)
	REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

	#OAuth2 authentication
	flow = flow_from_clientsecrets(
		secret_file,
		message=MISSING_SECRETS_MESSAGE,
		scope=SCOPE,
		redirect_uri=REDIRECT_URI
	)

	storage = Storage(os.path.dirname(os.path.realpath(__file__)) + '/' + oauth2_path)
	credentials = storage.get()

	if credentials is None or credentials.invalid:
		parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[oauth2client.tools.argparser])
		flags = parser.parse_args()
		credentials = run_flow(flow, storage, flags)

	# Create the service to use throughout the script
	youtube = build(
		SERVICE_NAME,
		VERSION,
		developerKey=setup['api_key'],
		http=credentials.authorize(httplib2.Http())
	)

def load_setup_values():
	setup_path = os.path.dirname(os.path.realpath(__file__)) + '/' + settings_path
	section_name = 'accounts'

	if not os.path.exists(setup_path):
		print("No settings.cfg found.")
		exit()

	setup = SafeConfigParser()
	setup.read(setup_path)

	if not setup.has_section(section_name):
		print("The setting.cfg file doesn't have an accounts section. Check the settings file format.")
		exit()

	if not setup.has_option(section_name, 'api_key'):
		print("No API key found in the settings.cfg file")
		exit()

	setting_values = {
		'api_key': setup.get(section_name, 'api_key')
	}
	return setting_values
