import requests

user_id = 'panda6722'
artistURL = f'https://api.spotify.com/v1/me/top/artists'
trackURL = 'https://api.spotify.com/v1/me/top/tracks'
playlistURL = f'https://api.spotify.com/v1/users/{user_id}/playlists'

# ACCESS_TOKEN = 'BQBR5ebpliJa9AfzRqgNnOBXFg5rikoyMHWIHLflXWhu0kAZYAofE27m73HQOyG_8XWPwNL1AND4c6NcPNUf0-Awz8faxJd9kDA8RCge6yNHqEKWGmk7Y57MCJGbzYx1Nv23-rtQuRNDQ0Q1lxE-5eU2j_gXgI0aBsd_Xw37u4Fs3N8r9_Ivcg'
ACCESS_TOKEN = 'BQDXECS0CVxPl4aUhY404tHbsyIylnItYIiDG0htC1hFcetRRrh1f43UjMINckLVBoc2Lwb07vY0l8fVHcvvptK_jme6u1M-QtCh0DDnk7E7qehqKWCRYUONpsCsBsc2l0XLIYO4Dhl5YzOBObG_8qoLXAAHvSXWxvxm2ZG00zuvXyjgsDGW7oKozFWubjsBS07cgjnxcXk2Ciyf7P1BLLU4rjlBB-6vmWa--P71xRo'

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