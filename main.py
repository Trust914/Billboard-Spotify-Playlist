from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from datetime import *
import requests
import spotipy
import pprint as pp
import os

pp = pp.PrettyPrinter(indent=4)

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")


def validate(date_text):
    """
        @param date_text: the date string entered by the user
        @return: True if the date_text is a valid date else False
    """
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


def get_user_date():
    """
        @return: the date specified by the user
    """
    date_to_scrap = input("what year you would like to travel to in YYYY-MM-DD format? ")
    if validate(date_to_scrap):
        return date_to_scrap
    else:
        print("Wrong date format. Try again!!")
        date_to_scrap = get_user_date()
    return date_to_scrap


def scrap_bill_board():
    """
    This function uses Beautiful soup to scrap the top 100 songs from a date specified by the user from the bill
    board website @return: the final created music data that contains the top 100 songs and respective artiste(s)
    """
    response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{user_date}")
    web_data = response.text

    soup = BeautifulSoup(web_data, "html.parser")

    music_title_tags = soup.select('li ul li h3', class_="title-of-a-story")
    music_list = [tag.text.replace("\n", "").replace("\t", "") for tag in music_title_tags]

    music_artistes_tags = soup.find_all("span", class_="u-letter-spacing-0021")
    artistes = [tags.getText().replace("\n", "").replace("\t", "") for tags in music_artistes_tags if
                "u-letter-spacing-0021" in tags.get("class")]
    # pp.pprint(artistes)

    music_dict = {music: artiste for music, artiste in zip(music_list, artistes)}
    # pp.pprint(music_dict)
    return music_dict


def spotify_playlist(song_data):
    """
        @param song_data: the music data gotten from scraping the bill board website
        This function authorises the spotify web API using the python module:spotipy,  creates a playlist in the spotify
        account and adds the songs in the song_data to the playlist
    """
    # _________ Authorise the spotify Web API using python,i.e,spotipy
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIFY_REDIRECT_URI,
                                                   scope="playlist-modify-private",
                                                   cache_path=".cache"))
    # ____ Get the user ID of the spotify account
    user_info = sp.current_user()
    user_id = user_info.get("id")
    # _________ Create a private playlist in the spotify account
    my_playlist = sp.user_playlist_create(user=user_id, name=f"Billboard Top Tracks -->> {user_date}",
                                          description=f"Top 100 songs as at : {user_date}",
                                          public=False)
    playlist_id = my_playlist.get("id")  # gets the ID of the created playlist
    spotify_song_uris = []  # this is the list that stores the uris for each song  that will be added in the playlist...
    # the uris are used to as an identification when searching for a song in spotify Search for the uri of each song
    # in the music dictionary
    for key, value in song_data.items():
        spotify_result = sp.search(q=f"artist:{value} track:{key} year:{str(int(year) - 5)}-{str(int(year) + 5)}",
                                   limit=20)
        try:
            song_uri = spotify_result['tracks'].get("items")[0].get("uri")
        except IndexError:
            # print(spotify_result)
            # print(f"The following was not found -->> Song: {key} ; Artist: {value}")
            continue
        else:
            spotify_song_uris.append(song_uri)

    pp.pprint(spotify_song_uris)
    sp.playlist_add_items(playlist_id=playlist_id, items=spotify_song_uris)  # all the songs to the playlist


user_date = get_user_date()
year = user_date.split("-")[0]
music_data = scrap_bill_board()
spotify_playlist(music_data)
