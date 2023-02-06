#MAIN FILE
from ytmusicapi import YTMusic #YT MUSIC API
import spotipy #SPOTIFY API
from spotipy.oauth2 import SpotifyOAuth #SPOTIFY AUTHENTICATION
import cred #SPOTIFY AUTHENTICATION CREDENTIALS FILE
import msvcrt
import sys

top_search_results = 5 #ENTER HOW MANY RESULTS YOU WANT TO BE DISPLAYED

def time_format(seconds: int) -> str:
    if seconds is not None:
        seconds = int(seconds)
        d = seconds // (3600 * 24)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if d > 0:
            return '{:02d}:{:02d}:{:02d}:{:02d}'.format(d, h, m, s)
        elif h > 0:
            return '{:02d}:{:02d}:{:02d}'.format(h, m, s)
        elif m > 0:
            return '{:02d}:{:02d}'.format(m, s)
        elif s > 0:
            return '{:02d}'.format(s)
    return '-'

def check_number(max: int, song_input: str) -> bool:
    if int(song_input) <= max:
        return True
    else:
        return False

def spotify_search_func(search_request: str, search_amount: int, artist_string: str):
    search = sp.search(search_request, search_amount)
    print("\nTop " + str(search_amount) + " Spotify Results:")
    songs_id_array = []
    songs_array = []
    tracks_position = 1
    for x in search["tracks"]["items"]:
        print("\n" + str(tracks_position) + ".", x["name"], end="")
        song_name = ""
        song_name += x["name"]
        artist_string = ""
        for artists in x["artists"]:
            artist_string += artists["name"] + ", "
        artist_string = artist_string[:-2]
        song_name += " - " + artist_string
        print(" - " + artist_string, end="")
        print(" | " + time_format((int(x["duration_ms"])/1000)), end="")
        explicit = "No"
        if x["explicit"]:
            explicit = "Yes"
        print(" | Explicit:", explicit, end="")
        print(" | Album Type:", x["album"]["album_type"], end="")
        if x["album"]["album_type"] == "album":
            print(" | Album Name:", x["album"]["name"], end="")
        songs_id_array.append(x["id"])
        
        tracks_position = tracks_position + 1
    print("\n\nPlease enter the number you want to put in the Spotify playlist:")
    song_choice = "none"
    while song_choice == "none":
        song_input = msvcrt.getch()
        song_input = song_input.decode("utf-8")
        if song_input.lower() == "s" or song_input.lower() == "x":
            song_choice = "skip" #SKIP SONG
            print("\nSkipped song...")
        elif check_number(search_amount, song_input):
            song_choice = "add"
            track_id = songs_id_array[int(song_input)-1]
            track_uri = "spotify:track:" + track_id
            track_uri_list = [track_uri]
            sp.playlist_add_items(spotify_playlist_id, track_uri_list)
            print("\nSuccessfully added ", song_name, "(" + song_input + ") to", sp.playlist(spotify_playlist_id)["name"] + "!")

print("Starting YT Music API Session...")
ytmusic = YTMusic('headers_auth.json') #Access YT Music user credentials
print("YT Music Session successful!")
print("Starting Spotify API Session...")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url, scope="playlist-modify-private, playlist-modify-public")) #Setup Spotify Session
print("Spotify API Session successful!")

ytmusic_playlist = ytmusic.get_liked_songs(20) #Get YT Music songs playlist
spotify_playlist_id = "" #Spotify playlist to add the yt music songs 

print("Acquired Playlists from YT Music and Spotify...")
print("State start position of the playlist:")
start_pos = int(input())
print("\nStarting procedure...")
print("\n/**--**/")
for i in range(start_pos-1, len(ytmusic_playlist["tracks"])-1):
    liked_song = ytmusic_playlist["tracks"][i]
    print ("\nEntry: ", i+1)
    print("\nSong Name:")
    print(liked_song["title"])
    print(time_format(liked_song["duration_seconds"]))
    print("\nAuthors: ")
    artist_string = ""
    for artists in liked_song["artists"]:
       artist_string += artists["name"] + " "
       print(artists["name"], end="")
    print("\n\nInclude search with arists? (Y/N)")
    choice = "none"
    while choice == "none":
        choice_input = msvcrt.getch()
        if choice_input == b'y' or choice_input == b'Y':
            choice = "yes" #SEARCH WITH AUTHOR
        elif choice_input == b'n' or choice_input == b'N':
            choice = "no" #SEARCH WITHOUT AUTHOR
        elif choice_input == b's' or choice_input == b'S':
            choice = "skip" #SKIP THIS SEARCH
        elif choice_input == b'x' or choice_input == b'x':
            choice = "exit" #TERMINATE PROGRAM
    if choice == "yes":
        print("Searching Spotify with author name included...")
        spotify_search_func((liked_song["title"] + artist_string), top_search_results, artist_string)
        print("\n/**--**/")
    elif choice == "no":
        print("Searching Spotify without author name included...")
        spotify_search_func((liked_song["title"]), top_search_results, artist_string)
        print("\n/**--**/")
    elif choice == "exit":
        print("Reached position", i+1, "of", sp.playlist(spotify_playlist_id)["name"], "(YT Music)")
        break
print("\nTerminating program...")
sys.exit()