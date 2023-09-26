from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()


year_search = input("What year would you like to research? (YYYY-MM-DD): ")
MUSIC_URL = f"https://www.billboard.com/charts/rock-songs/{year_search}/"

#================== Get List =========================

contents = requests.get(MUSIC_URL)
music_data = contents.text

soup = BeautifulSoup(music_data, "html.parser")

title = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in title]
year = year_search.split("-")[0]


#============== Spotipy ==================

SPOTIFY_ID = os.getenv("SPOTIFY_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("redirect_uri")
scope = "playlist-modify-private"


auth_url = "https://accounts.spotify.com/autherize"
token_url = "https://accounts.spotify.com/api/token"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    state=None,
    scope=scope,
    cache_path=None,
    username=None,
    proxies=None,
    show_dialog=False,
    requests_session=True,
    requests_timeout=None,
    open_browser=True,
    cache_handler=None,
))


user_id = sp.current_user()["id"]
# print(user_id)

print(song_names)

track_list = []
for items in song_names:
    track = sp.search(q=f"track: {items} year: {year}", limit=1, type="track")
    try:
        track_id = track["tracks"]["items"][0]["uri"]
        track_list.append(track_id)
    except IndexError:
        print("Track not found")

pprint(track_list)

print(sp.user_playlist_create(
    user=user_id,
    name=f"{year_search} Billboard 100",
    public=False,
    collaborative=False,
    description="Rock from round my Grad"
))

playlist_id = "792JCddz4EPqdLMi16wGOg"

sp.playlist_add_items(playlist_id=playlist_id, items=track_list)
