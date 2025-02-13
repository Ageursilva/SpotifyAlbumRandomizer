from flask import Flask, render_template, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import random

app = Flask(__name__)
app.secret_key = '' 

client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:5000/callback' 
scope = 'user-library-read'

def criar_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )

@app.route('/')
def index():
    if 'token_info' not in session:
        return render_template('index.html', logged_in=False)
    
    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    resultados = sp.search(q='year:2020-2023', type='album', limit=50)
    albuns = resultados['albums']['items']
    album_aleatorio = random.choice(albuns) if albuns else None
    
    return render_template('index.html', logged_in=True, album=album_aleatorio)

@app.route('/login')
def login():
    sp_oauth = criar_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = criar_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('token_info', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)