#!/usr/bin/env python
# coding: utf-8
import requests
import base64
import datetime
from urllib.parse import urlencode


class SpotifyAPI():
    access_token = None
    expires = datetime.datetime.now()
    expired = True
    client_id = None
    client_secret = None
    redirect_uri = 'http://localhost:8888/notebooks/Autho.ipynb'
    token_url = 'https://accounts.spotify.com/api/token'
    
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def __getTokenData(self):
        return {
            'grant_type': 'client_credentials'
        }
    def __getTokenHeaders(self):
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
        self.expired = expires < now
        return True
        

