from Client import SpotifyAPI

CLIENT_ID = '4e75cab0012d409da502214e828ade40'
CLIENT_SECRET = '3a5f1a1c83f442f991b1321a4e78edac'

def main():
    client = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    res = client.recommendByTrack("Glimpse of us", 'dorothea')

if __name__ == "__main__":
    main()