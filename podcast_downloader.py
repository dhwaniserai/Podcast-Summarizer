import spotipy
import requests
import urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyPodcast:
    def __init__(self, client_id, client_secret):
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))
        

    def download_episode(self, podcast_url):
        # Parse the podcast ID from the URL
        parsed_url = urllib.parse.urlparse(podcast_url)
        podcast_id = parsed_url.path.split("/")[-1]
        print(f'Podcast ID: {podcast_id}')
        
        episode = self.sp.episode(podcast_id, market="US")

        # Save the audio file
        audio_url = episode["audio_preview_url"]
        response = requests.get(audio_url)
        filename = f"{podcast_id}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Episode downloaded: {filename}")
        
        return filename

if __name__=="__main__":
    sp = SpotifyPodcast("CLIENT_ID", "CLIENT_SECRET")
    audio_filename = sp.download_episode("https://open.spotify.com/episode/6oUTyFPLPvJE1jB50hm37l")