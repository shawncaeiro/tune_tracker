import urllib
import base64
import json
import requests
from requests.auth import HTTPBasicAuth
from private import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET

def get_spotify_code_url(state):
    try:
        client_id = SPOTIFY_CLIENT_ID
        redirect_uri = "http://127.0.0.1:8000/spotify_return/"
        scope = "user-read-private user-read-email"

        f = { 'client_id' : client_id, 
        'redirect_uri' : redirect_uri,
        'scope' : scope,
        'state' : str(state),
        'response_type' : 'code',
        'show_dialog' : 'true'}

        url = "https://accounts.spotify.com/authorize?"
        url = url + urllib.parse.urlencode(f)
    except:
        return None, False
    return url, True

def get_auth_token(code, state, redirect):
    try:
        url = "https://accounts.spotify.com/api/token"
        c_id = SPOTIFY_CLIENT_ID
        c_se = SPOTIFY_SECRET
        params = {'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : "http://127.0.0.1:8000/spotify_return/",
        'state' : state}
        auth = HTTPBasicAuth(c_id,c_se)
        r = requests.post(url, auth=auth, data=params)
        d = json.loads(r.text)
        at = d["access_token"]
    except:
        return None, False
    return at, True

def get_spotify_user_id(token):
    try:
        params = {'Authorization' : 'Bearer {0}'.format(token)}
        url = 'https://api.spotify.com/v1/me'
        r = requests.get(url, headers= params)
        d = json.loads(r.text)
        s_id = d['id']
    except:
        return None, False
    return s_id, True

def get_spotify_user_playlists(token, s_id):
    try:
        params = {'Authorization' : 'Bearer {0}'.format(token)}
        url = 'https://api.spotify.com/v1/users/{0}/playlists'.format(s_id)
        r = requests.get(url, headers= params)
        d = json.loads(r.text)
        playlists = [p['name'] for p in d['items']]
    except:
        return None, False
    return playlists, True