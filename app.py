from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import C_Secret

# Configuración de la API de Spotify
SPOTIPY_CLIENT_ID = '3a4ec34d235d41b3bff556587b7eb0d1'
SPOTIPY_CLIENT_SECRET = C_Secret.CLIENT_SECRET

app = Flask(__name__)

# Autenticación de cliente
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    artista = request.form['artista']
    resultados = sp.search(q=f'artist:{artista}', type='artist', limit=1)

    if resultados['artists']['items']:
        artista_info = resultados['artists']['items'][0]
        nombre = artista_info['name']
        popularidad = artista_info['popularity']
        seguidores = artista_info['followers']['total']
        imagen = artista_info['images'][0]['url'] if artista_info['images'] else None

        return render_template('resultados.html', nombre=nombre, popularidad=popularidad, seguidores=seguidores, imagen=imagen)
    else:
        return render_template('resultados.html', error="Artista no encontrado.")

if __name__ == '__main__':
    app.run(debug=True)
