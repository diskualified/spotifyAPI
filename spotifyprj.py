import requests
import base64

CLIENT_ID = '4e75cab0012d409da502214e828ade40'
CLIENT_SECRET = '3a5f1a1c83f442f991b1321a4e78edac'
client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_creds_b64 = base64.b64encode(client_creds.encode())

user_id = 'panda6722'
artistURL = f'https://api.spotify.com/v1/me/top/artists'
trackURL = 'https://api.spotify.com/v1/me/top/tracks'
playlistURL = f'https://api.spotify.com/v1/users/{user_id}/playlists'

auth_url = 'https://accounts.spotify.com/authorize'
auth_code = requests.get(auth_url, {
    'client_id': CLIENT_ID,
    'response_type': 'code',
    'redirect_uri': 'http://localhost:8888/notebooks/Autho.ipynb',
})
token_url = 'https://accounts.spotify.com/api/token'
token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'authorization': f"Basic {client_creds_b64.decode()}" # <base64 encoded client_id:client_secret>
}
auth_data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': 'http://localhost:8888/notebooks/Autho.ipynb',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
}
auth_r = requests.post(token_url, data = auth_data, headers = token_headers)
print(auth_r.json())
ACCESS_TOKEN = auth_r.json()["access_token"]

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}", 
    'Content-Type': 'application/json',
    "Accept": "application/json"
}

def createPlaylist():
    response = requests.get(playlistURL, headers=headers, json={'name':'Test'})
    myjson = response.json()
    print(myjson)

def getTopArtists():
    response = requests.get(artistURL, headers=headers, 
                            json={"limit":10, 'time_range': 'short_term'})

    myjson = response.json()
    print(myjson)
    return myjson

def getTopTracks():
    response = requests.post(trackURL, headers=headers, 
                            json={"limit":10, 'time_range': 'short_term'})

    myjson = response.json()
    return myjson

def main():
    # artists = getTopArtists()
    # tracks = getTopTracks()
    # print(artists)
    # print(tracks)
    createPlaylist()

if __name__ == "__main__":
    main()