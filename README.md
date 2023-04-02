# BillBoard Spotify Playlist

The purpose of this project is to scrape the BillBoard website and get the top 100 songs as at a date specified by the user in the command line interface (yes!! this is a cli program....).
Thereafter, using the spotify api and spotipy library, it creates a playlist in your spotify account and add the songs in the playlist.

To use this project, 
- First clone the repo
- If you have no spotify account already, kindly create one.
- Then, move to the spotify api website : https://developer.spotify.com/documentation/web-api
- Log in or create an account using the same credentials as your spotify account
- Read the documentation to see how to  create an app so you can acquire a client ID and client secret which you can add as environment variables. This is needed for authenticating the spotify app. In this script the variables are as follows:

	- SPOTIFY_CLIENT_ID
	- SPOTIFY_CLIENT_SECRET
	- SPOTIFY_REDIRECT_URI 

- Make sure to use this same variable name when adding it to your environment, otherwise, if you use a different name, ensure to update it inside the main.py script.
- When creating an app in the spotify web api site, you have to add a redirect uri ( check the documentation on why and how to do this) which is custom made ,i.e., you can use any name of your choosing.


# Please note: 
that when you run the script for the first time, after asking for the date to get music data from, the script will automatically open a webpage and asks you to enter the url. Copy the 	full url of the page and paste it in required position in the cli. This will create a .cache file and will not request for it when you run the script subsequently.


When all is done successfully, check your spotify account, you should see new playlist for your enjoyment!!

Annnndddd that's it!!!
