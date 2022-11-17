
import json
import requests
import os

from secrets import spotify_user_id
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


class CreatePlaylist:
    
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_client=self.get_youtube_client()
        self.all_song_info={}
        
     #Log into youTube
    def get_youTube_Client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = ""
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"
        pass
     #grab your YouTube playlist and create a dictionary of important song information
    def get_youtube_plalist_videos(self):
        request = self.youTube_client.videos().list(
            part="",
            myRating="like"
        )
        response = request.execute()
        #collect each video and get important info
        for item in response["Items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/playlist?list=PL2VeCRc2Bsr8BM9fBX9a3q0tcpLHY0o_L".format(item["id"])
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]
            
        #save all important information
        self.all_song_info[video_title]={
            "youtube_url":youtube_url,
            "song_name":song_name,
            "artist":artist,
            
            #add the uri, easy to get song into playlist
            "spotify_uri":self.get_spotify_url(song_name,artist)
        }
    #create a new Spotify playlist
    def create_playlist(self):
        pass
        request_body = json.dumps({
            "name": "My YouTube Song Playlist",
            "description": "My favourite YouTube Songs",
            "public": True
        })
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format()
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format()
            }
        )
        response_json = response.json()
        #playlist id
        return response_json["id"]  
    
    
    
    #search for the song
    def get_spotify_url(self,song_name,artist):
        query="https://api.spotify.com/v1/search?query=track%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format()
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        
        #Using the first song
        url = songs[0]["url"]
        
    #add this song into the new spotify playlist
    def add_song_to_playlist(self):
        
        #populate our songs dictionary
        self.get_youtube_plalist_videos()
        
        #collect uri
        uris = []
        for song,info in self.all_song_info.items():
            uris.append(info["spotify_uri"])
            
        #create a new playlist
        request_data = json.dumps(uris)
        query = "htps://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
                }
        )
        response_json = response.json()
        return response_json 