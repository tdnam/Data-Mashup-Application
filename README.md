# COMP9321 Assignment 3, Data-Mashup-Application
# Your Simpson Playlist

Create playlists defined by your favourite Simpson chararcters!

## Getting Started

### Server

In order to run the server from scratch (i.e. no datasets downloaded), a kaggle API key is needed. This key exists in the file server/conf/kaggle.json. For Linux, put this file in ~/.kaggle/kaggle.json. For other operating systems, see https://github.com/Kaggle/kaggle-api

To install all of the required packages, type: ```pip install -r server/conf/requirements.txt```

When installing the packages, the google api seems to be a bit weird. In order to get it to work, run the following command: ```pip install --force-reinstall google-api-python-client```

To run the server, cd to server/ and type: ```python server.py```

The will automatically download the big datasets. Since the characters are probably already in the database, this is not needed. In that case, simply comment the line "download_datasets()" in the "setup()" method in server.py

### Client

Open the HTML file client/templates/Simphony.html

## Tutorial

### Server API:

GET /character/"name"<br/>
HTTP responses: 200, 404, 500<br/>
Returns the character name and a link to its picture.<br/>
Example: /character/bart_simpson

GET /characters/<br/>
HTTP responses: 200, 500<br/>
Returns all of the characters with their names and links to their pictures.<br/>
Example: /characters

GET /picture/"name"<br/>
HTTP responses: 200, 404, 500<br/>
Returns the picture, as an mimitype="image/gif" for the given character.<br/>
Example: /picture/bart_simpson

GET /songs/<br/>
HTTP responses: 200, 400, 404, 500<br/>
The requester sends a list of characters as a parameter.The parameter name is called "characterse" and the characters are separated by the pipe "|" token.<br/>
Returns a list of songs given the characters.<br/>
Example: /songs?characters=bart_simpson|homer_simpson

GET /analytics/<br/>
HTTP responses: 200, 500<br/>
Opens a new tab with the statistics about each character, namely how many times their songs have been requested.<br/> 
Example: /analytics

### Client:

Select your favourite characters and press genereate playlist. Our application
will create a playlist tailored for each character and automatically start playing it.
The application gives you controll over the playlist, and lets you skip, pause, and
replay songs. If you really enjoy a playlist, you can press download, and you will download
a text file with all artists and song in the current playlist!

## Built With

* [Bootstrap](https://getbootstrap.com/) - The web framework used
* [Trello](https://trello.com) - Project Management ([our page](https://trello.com/b/UI12zl5r/jdnt))
* Python version 3.6.3

## Versioning

We use [Github](http://github.com/) for versioning. For the versions available, see our [repository](https://github.com/cseunswgithub/Data-Mashup-Application).

## Authors

* **Tim Borglund, z5198523**
* **Joachim Jorgensen, z5177766**
* **Nam Tran, z5090191**
* **David Wong, z3449265**
