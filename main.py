import os
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow
import spotipy
import spotipy.util as util

# Replace these with your own API keys
YOUTUBE_API_KEY = ""
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""

# Replace this with the ID of your YouTube playlist
YOUTUBE_PLAYLIST_ID = ""

# Replace this with the name of your Spotify playlist
SPOTIFY_PLAYLIST_NAME = "Don Moen Worship songs"

# Set the scope for the Spotify API
SCOPE = "playlist-modify-public"

# Get the authorization token for the Spotify API
token = util.prompt_for_user_token(
    username="t56gj8pnahvrhcctfnguutdp3",
    scope="playlist-modify-public",
    client_id= "",
    client_secret="",
    redirect_uri="https://lemashon.netlify.app/"
)

# Create the Spotify API client
spotify = spotipy.Spotify(auth=token)

# Create the YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Get the list of videos in the YouTube playlist
request = youtube.playlistItems().list(
    part="snippet",
    playlistId="",
    key="",
)
response = request.execute()

# Create a new Spotify playlist
playlist = spotify.user_playlist_create(
    user="t56gj8pnahvrhcctfnguutdp3",
    name="Don Moen Worship songs",
    public="True",
)
playlist_id = playlist["id"]

# Add each track to the Spotify playlist
for item in response["items"]:
    video_id = item["snippet"]["resourceId"]["videoId"]

    # Get the video's title and artist
    request = youtube.videos().list(
    part="snippet",
    id=video_id,
    key=""
)
response = request.execute()
video_title = response["items"][0]["snippet"]["title"]
video_artist = response["items"][0]["snippet"]["channelTitle"]

# Search for the track on Spotify
results = spotify.search(q=f"track:{video_title} artist:{video_artist}", type="track")
track_uri = results["tracks"]["items"][0]["uri"]

# Add the track to the playlist
spotify.user_playlist_add_tracks(user="",
playlist_id=playlist_id,
tracks=[track_uri]
)

print("Playlist transfer complete!")
