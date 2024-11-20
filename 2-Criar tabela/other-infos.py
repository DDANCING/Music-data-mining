import requests
import pandas as pd
import os
import base64
from dotenv import load_dotenv
import time

# Carregar variáveis de ambiente
load_dotenv()

# Obter client_id e client_secret do Spotify e a chave da YouTube API
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
genius_access_token = os.getenv("GENIUS_ACCESS_TOKEN")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

# Função para obter token de acesso do Spotify
def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    auth_response = requests.post(auth_url, headers=headers, data=data)
    if auth_response.status_code != 200:
        print("Erro na autenticação com a API do Spotify.")
        return None
    return auth_response.json().get("access_token")

# Função para obter a URL da letra da música da Genius API
def get_lyrics(track_name, artist_name):
    base_url = "https://api.genius.com"
    search_url = f"{base_url}/search"
    headers = {"Authorization": f"Bearer {genius_access_token}"}
    params = {"q": f"{track_name} {artist_name}"}

    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['response']['hits']:
            song_info = data['response']['hits'][0]['result']
            lyrics_path = song_info['path']
            lyrics_url = f"{base_url}{lyrics_path}"
            return lyrics_url  # Retorna a URL da letra
    return None

# Função para obter informações do Spotify
def get_track_info_spotify(track_name, artist_name, token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": f"track:{track_name} artist:{artist_name}" if artist_name else f"track:{track_name}",
        "type": "track",
        "limit": 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['tracks']['items']:
            track = data['tracks']['items'][0]
            genre = None
            if 'album' in track and 'genres' in track['album'] and track['album']['genres']:
                genre = track['album']['genres'][0]
            return {
                "genre": genre,
                "popularity": track['popularity'],
                "track_id": track['id']
            }
    return None

# Função para obter visualizações do YouTube
def get_youtube_views(track_name, artist_name):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{track_name} {artist_name}",
        "type": "video",
        "key": youtube_api_key,
        "maxResults": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        search_results = response.json().get("items")
        if search_results:
            video_id = search_results[0]["id"]["videoId"]
            video_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={youtube_api_key}"
            video_response = requests.get(video_url)
            if video_response.status_code == 200:
                video_data = video_response.json()
                if "items" in video_data and video_data["items"]:
                    view_count = video_data["items"][0]["statistics"]["viewCount"]
                    return int(view_count)
    return None

# Caminho do arquivo da planilha existente
input_file_path = '/Users/marcelomazzonetto/Desktop/Mineracao de dados/top_10000_musicas.xlsx'
df_tracks = pd.read_excel(input_file_path)

# Lista para armazenar as novas informações
tracks_data = []

# Obter token do Spotify
token = get_spotify_token(client_id, client_secret)

# Total de faixas para cálculo da porcentagem de conclusão
total_tracks = len(df_tracks)

# Loop pelas faixas da planilha
for index, row in df_tracks.iterrows():
    track_name = row['name']
    artist_name = row['artist']

    # Obter letra
    lyrics_url = get_lyrics(track_name, artist_name)

    # Obter informações do Spotify
    track_info = get_track_info_spotify(track_name, artist_name, token)

    # Obter visualizações do YouTube
    youtube_views = get_youtube_views(track_name, artist_name)

    # Calcular a porcentagem de conclusão
    completion_percentage = (index + 1) / total_tracks * 100

    # Exibir progresso
    print(f"Processando {track_name} - {artist_name} ({index + 1}/{total_tracks}) - {completion_percentage:.2f}% concluído")

    # Adicionar dados à lista
    tracks_data.append({
        "name": track_name,
        "artist": artist_name,
        "lyrics_url": lyrics_url,
        "genre": track_info['genre'] if track_info else None,
        "popularity": track_info['popularity'] if track_info else None,
        "youtube_views": youtube_views,
        "completion_percentage": f"{completion_percentage:.2f}%",
    })

# Criar DataFrame com as novas informações
df_tracks_info = pd.DataFrame(tracks_data)

# Salvar as informações em um novo arquivo Excel
output_file_path = '/Users/marcelomazzonetto/Desktop/Mineracao de dados/top_10000_musicas_info.xlsx'
df_tracks_info.to_excel(output_file_path, index=False)

print(f"Arquivo Excel salvo em: {output_file_path}")
