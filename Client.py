import requests
import base64
import datetime
from urllib.parse import urlencode
from IPython.display import Image, display



# search, recommendByTrack, getAudioFeatures, getRelatedArtists
class SpotifyAPI():
    access_token = None
    expires = datetime.datetime.now()
    client_id = None
    client_secret = None
    redirect_uri = 'http://localhost:8888/notebooks/Autho.ipynb'
    token_url = 'https://accounts.spotify.com/api/token'
    headers = None
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def getTokenData(self):
        return {
            'grant_type': 'client_credentials'
        }
    def getTokenHeaders(self):
        client_creds = f"{self.client_id}:{self. client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return {
            'authorization': f"Basic {client_creds_b64.decode()}" # <base64 encoded client_id:client_secret>
        }
    
    def performAuth(self):
        r = requests.post(self.token_url, data=self.getTokenData(), headers = self.getTokenHeaders())
        if r.status_code not in range(200, 299):
            return False
        response = r.json()
        now = datetime.datetime.now()
        self.access_token = response['access_token']
        expires_in = response['expires_in']
        self.expires = now + datetime.timedelta(seconds=expires_in)
        return True

    def getToken(self):
        if self.expires < datetime.datetime.now():
            self.performAuth()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    def displaySearch(self, result, searchtype, getID):
        if searchtype == 'track':
            # 0 index meaning first result
            title = result['tracks']['items'][0]['name']
            artist = result['tracks']['items'][0]['artists'][0]['name']
            artist_id = result['tracks']['items'][0]['artists'][0]['id']
            song_id = result['tracks']['items'][0]['id']
            if getID:
                return song_id, artist_id
            link = f"https://open.spotify.com/track/{song_id}"
            artist_page = f"https://open.spotify.com/artist/{artist_id}"
            img = result['tracks']['items'][0]['album']['images'][1]['url']
            release_date = result['tracks']['items'][0]['album']['release_date']
            display(Image(url=img))
            print(f"Title: {title}\nArtist: {artist}\nRelease Date: {release_date}\nLink: {link}\nArtist Profile: {artist_page}")
        elif searchtype == 'artist':
            if getID:
                return result['artists']['items'][0]['id']
            artist = result['artists']['items'][0]['name']
            link = result['artists']['items'][0]['external_urls']['spotify']
            followers = result['artists']['items'][0]['followers']['total']
            img = result['artists']['items'][0]['images'][1]['url']
            display(Image(url=img))
            print(f"Name: {artist}\nFollower Count: {followers}\nProfile: {link}")
        elif searchtype == 'album':
            img = result['albums']['items'][0]['images'][1]['url']
            display(Image(url=img))
            # TODO: Display Album Info
            
        else:
            print("Choose type: track, artist, or album")
        return result
    
    
    # User Functions Below
    
    # search track, artist, album
    def search(self, name, searchtype, getID = False):
        self.getToken()
        data = {'q': name, 'type': searchtype.lower()}
        dataurl = urlencode(data)
        url = f"https://api.spotify.com/v1/search?{dataurl}"
        r = requests.get(url, headers=self.headers)
        result = r.json()
        
        return self.displaySearch(result, searchtype, getID)
    
    # input one or two songs
    def recommendByTrack(self, song1, song2=''):
        self.getToken()
        song1_id, artist1_id = self.search(song1, 'track', getID=True)
        data = {'seed_artists': artist1_id, 'seed_tracks': song1_id}
        if song2 != '':
            song2_id, artist2_id = self.search(song2, 'track', getID=True)
            if artist2_id != artist1_id:
                data['seed_artists'] += f',{artist2_id}'
            data['seed_tracks'] += f',{song2_id}'
            
        dataurl = urlencode(data)
        url = f"https://api.spotify.com/v1/recommendations?{dataurl}"
        r = requests.get(url, headers=self.headers)
        response = r.json()
        
        for i in range(10):
            name = response['tracks'][i]['album']['artists'][0]['name']
            album = response['tracks'][i]['album']['name']
            link = response['tracks'][i]['album']['external_urls']['spotify']
            img = response['tracks'][i]['album']['images'][1]['url']
            display(Image(url=img))
            print(f"{i+1}. Artist: {name}\nAlbum: {album}\nSpotify Link: {link}\n")
        return response
    
    # search by artist or track using isArtist bool
    def getRelatedArtists(self, name, isArtist):
        if isArtist:
            _id = self.search(name, 'artist', getID=True)
        else:
            _id = self.search(name, 'track', getID=True)[1]
        url = f'https://api.spotify.com/v1/artists/{_id}/related-artists'
        r = requests.get(url, headers = self.headers)
        response = r.json()
        print("Similar Artists:")
        for i in range(20):
            print(i+1, response['artists'][i]['name'])
        return response
    
    def getAudioFeatures(self, track):
        _id = self.search(track, 'track', getID=True)[0]
        url = f'https://api.spotify.com/v1/audio-features/{_id}'
        r = requests.get(url, headers=self.headers)
        # TODO: Parse / visualize audio features (e.g. danceability, energy)
        
        return r.json()
    