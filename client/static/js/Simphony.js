
// On page load we want to fetch all images
window.addEventListener('load', load_characters());

// JSON object representing selected characters
var selected_characters_json = null

// JSON object represening all characters available
var all_characters = null;

var YouTube_created = false;

// The playlist URLs
var playlist_ids = [];
var playlist_index = -1;

// Request character object from database
function get_character() {

	// Empty previous playlist
	playlist_ids = []

	var checkboxes = document.getElementsByName('team[]');
	var characters = "";
	for (var i=0, n=checkboxes.length;i<n;i++) {
    	if (checkboxes[i].checked) {
        	characters += "|"+checkboxes[i].value;
    	}
	}

	// Remove first pipe symbol
	if (characters) characters = characters.substring(1);

	// Create a request
	var xhttp = new XMLHttpRequest();
	xhttp.onload = function() {

  		if (this.readyState == 4) {

			if (this.status == 200) {
				selected_characters_json = JSON.parse(xhttp.responseText);
				update_playlist();

			} else if (this.status == 400) {
				alert("Bad request!");

			} else if (this.status == 401) {
				alert("Not authorized!");

			} else {
				console.log("There was a problem with the request: " + xhttp.responseText);
			}
		}
	};

	xhttp.open("GET", "http://127.0.0.1:5000/songs?characters=" + characters, true);
	xhttp.setRequestHeader("Content-Type", "text/plain");
	xhttp.setRequestHeader("Accept", "application/json");
	xhttp.send();
}

// Request all character images
function get_image(character) {

	// Create a request
	var xhttp = new XMLHttpRequest();
	xhttp.onload = function() {

  		if (this.readyState == 4) {

			if (this.status == 200) {

				var characters = JSON.parse(xhttp.responseText);
				var img_url = xhttp.responseText;
				return img_url;

			} else if (this.status == 400) {
				alert("Bad request!");

			} else if (this.status == 401) {
				alert("Not authorized!");

			} else {
				console.log("There was a problem with the request: " + xhttp.responseText);
			}
		}
	};

	//xhttp.open("GET", "http://127.0.0.1:5000/picture/" + character, true);
	xhttp.open("GET", "http://127.0.0.1:5000/characters", true);
	xhttp.setRequestHeader("Content-Type", "text/plain");
	xhttp.setRequestHeader("Accept", "application/json");
	xhttp.send();
}

//Get bar graph
function analytics(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:5000/analytics", true);
    xhttp.send();
}

// Get a list of all characters in the database
function load_characters() {
	// Create a request
	var xhttp = new XMLHttpRequest();
	xhttp.onload = function() {

  		if (this.readyState == 4) {

			if (this.status == 200) {
				var all_characters_json = JSON.parse(xhttp.responseText);
				var all_characters = all_characters_json.characters;
				update_all_characters(all_characters);

			} else if (this.status == 400) {
				alert("Bad request!");

			} else if (this.status == 401) {
				alert("Not authorized!");

			} else {
				console.log("There was a problem with the request: " + xhttp.responseText);
			}
		}
	};

	xhttp.open("GET", "http://127.0.0.1:5000/characters", true);
	xhttp.setRequestHeader("Content-Type", "text/plain");
	xhttp.setRequestHeader("Accept", "application/json");
	xhttp.send();

}

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}


//Update all characters
function update_all_characters(all_characters) {

	var num_characters = all_characters.length;

	var excess_characters = num_characters % 6;

	// If the number of characters are not divisble by 6
	if (excess_characters) {
		var num_blanks = 6 - excess_characters;

		var i;
		for (i = 0; i < num_blanks; i++) {
			var attributes = {};
			attributes["char_name"] = "";
			attributes["img_link"] = "";

			all_characters[num_characters + i] = attributes;
		}
	}

	var num_rows = Math.ceil(num_characters / 6);

	// Create a div tag for each row
	var row;
	for (row = 0; row < num_rows; row++) {

    	var row_div = document.createElement("div");
    	row_div.className = "row";
    	row_div.id = "row_" + row;

    	var feed = document.getElementById("feed");
    	feed.appendChild(row_div);
	}

	// Keep track of number of additions
	var counter = 0;

	// Create an entry of all characters
	for (character in all_characters) {

		// Get character info
		var char_name = all_characters[character].char_name;
		var img_link = all_characters[character].img_link;

		// Get the correct div
		var row_num = Math.floor(counter / 6);
		var row_div = document.getElementById("row_" + row_num);

		// Create a column element
		var div_col_sm = document.createElement("div");
		div_col_sm.className = "col-sm";

		// Create a label
		var label = document.createElement("label");
		label.className = "image-checkbox";

		// Create an image element
		var img = document.createElement("img");
		img.id = "img_" + char_name;
		img.source = "";
		img.style = "width:100%";

		// Create an input element
		var input = document.createElement("input");
		input.className = "checkbox_character";
		input.value = char_name;
		input.type = "checkbox";
		input.name = "team[]";

		// Create an overlay div
		var div_overlay = document.createElement("div");
		div_overlay.className = "text_overlay";

		// Create a text div
		var div_overlay_text = document.createElement("div");
		div_overlay_text.className = "overlay_text";
		var refined_name = char_name.replace(/_/g, ' '); // Remove underscore
		refined_name = toTitleCase(refined_name); // Capitalise each name
		div_overlay_text.innerHTML = refined_name;

		// Append elements bottom up:
		div_overlay.appendChild(div_overlay_text);

		label.appendChild(img);
		label.appendChild(input);
		label.appendChild(div_overlay);

		div_col_sm.appendChild(label);

		row_div.appendChild(div_col_sm);

		// Update images
		update_image(char_name, img_link);

		counter++;
	}
}


// Update image of a character
function update_image(character, img_link) {

	if (document.getElementById("img_" + character)) {

		// Get the character tag to be updated
		var img = document.getElementById("img_" + character);
		img.src=img_link;
	}
}


// Update playlist ids
function update_playlist_ids() {

	var characters = selected_characters_json.characters;

	for (character in characters) {
		var current_character = selected_characters_json.characters[character];

		for (song in current_character.songs) {
			playlist_ids.push(current_character.songs[song].youtube_id);
		}
	}
}


// Get the name of current characters
function get_names() {
	var names = ""

	var characters = selected_characters_json.characters;

	for (character in characters) {
		var current_character = selected_characters_json.characters[character];
		names += current_character.char_name + " ";
	}
	return names;
}


// Update the playlist
function update_playlist() {

	update_playlist_ids();

	if (YouTube_created) {
		play_next_song();
	} else {
		YouTube_created = true;
		create_youtube_player();
	}
}


// Get the ID of the next song in the queue
function next_song() {

	// Update the index
	playlist_index += 1;

	// Loop back to the beginning of the playlist
	// if necessary
	if (playlist_index == playlist_ids.length){
		playlist_index = 0;
	}

	// Get the id from the song index list
	next_song_id = playlist_ids[playlist_index];

	// Return the next song
	return next_song_id;
}


// Get the ID of the previous song in the queue
function previous_song() {

	//Update index
	playlist_index -= 1;

	// Loop to the end of the playlist if
	// current song is the first in the queue
	if (playlist_index == -1) {
		playlist_index = playlist_ids.length - 1;
	}

	// Get the id from the song index list
	previous_song_id = playlist_ids[playlist_index];

	// Return the previous song
	return previous_song_id;
}


// Download the playlist
function download_playlist() {

	var names = get_names();
	var playlist_songs = ""
	playlist_songs += "Artist:".padEnd(25);
	playlist_songs += "  Title:".padEnd(25);
	playlist_songs += "\n";

	var characters = selected_characters_json.characters;

	for (character in characters) {
		var current_character = selected_characters_json.characters[character];

		for (song in current_character.songs) {
			var artist = current_character.songs[song].artist;
			var title = current_character.songs[song].name;
			playlist_songs += artist.padEnd(25);
			playlist_songs += "- ";
			playlist_songs += title.padEnd(25);
			playlist_songs += " \n";
		}
	}

	// Create a file-like representation of the playlist
	var blob = new Blob([playlist_songs], {type: "text/plain"});

	// Create a temporary link-element to activate the download
	var link = document.createElement('a');
	link.download = names + ".txt";
	link.href = window.URL.createObjectURL(blob);

	link.onclick = function(e) {
		// revokeObjectURL needs a delay to work properly
		var that = this;
		setTimeout(function() {
			window.URL.revokeObjectURL(that.href);
		}, 1500);
	};

	// initiate and remove the download link
	link.click();
	llink.remove();
}


function create_youtube_player() {
	document.getElementById("video").innerHTML = "<div id='player'></div>";

	// Load the IFrame Player API code asynchronously.
	var tag = document.createElement('script');

	tag.src = "https://www.youtube.com/iframe_api";
	var firstScriptTag = document.getElementsByTagName('script')[0];
	firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

	var controls = document.getElementById("controls");

	// Display controls
	if (controls.style.display === "none") {
        //controls.style.display = "inline-block";
        controls.style = "display: inline-block";
    } else {
        controls.style.display = "none";
    }
}

// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
		height: '390',
		width: '640',
		videoId: next_song(),
		events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange
		}
	});

}

// The Youtube API will call this function when the video player is ready.
function onPlayerReady(event) {
	event.target.playVideo();

}

// When the song ends, ply the next one in the queue.
function onPlayerStateChange(event) {
	if (event.data == 0) {
		play_next_song();
	}
}

// Play the next son in the queue.
function play_next_song() {
	player.cueVideoById(next_song());
	player.playVideo();
}


// Play the previous song in the queue
function play_previous_song() {
	player.cueVideoById(previous_song());
	player.playVideo();
}


// Pause the current song
function pause_current_song() {
	player.pauseVideo();
}


// Resume the current song
function resume_current_song() {
	player.playVideo();
}

// Set so that checkboxes will be highlighted when pressed.
// To avoid race condition, have a 1 sec timmeout.
setTimeout(function(){
    jQuery(function ($) {
  // init the state from the input
  $(".image-checkbox").each(function () {
      if ($(this).find('input[type="checkbox"]').first().attr("checked")) {
          $(this).addClass('image-checkbox-checked');
      }
      else {
          $(this).removeClass('image-checkbox-checked');
      }
  });

  // sync the state to the input
  $(".image-checkbox").on("click", function (e) {
      if ($(this).hasClass('image-checkbox-checked')) {
          $(this).removeClass('image-checkbox-checked');
          $(this).find('input[type="checkbox"]').first().removeAttr("checked");
      }
      else {
          $(this).addClass('image-checkbox-checked');
          $(this).find('input[type="checkbox"]').first().attr("checked", "checked");
      }

      e.preventDefault();
  });
});
}, 1000);
