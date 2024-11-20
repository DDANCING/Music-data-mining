import requests
import pandas as pd
import os
import base64
from dotenv import load_dotenv
import time

# Carregar variáveis de ambiente
load_dotenv()

# Obter client_id e client_secret do Spotify
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

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

# Função para obter os gêneros do artista
def get_artist_genres(artist_id, token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("genres", [])
    else:
        print(f"Erro ao buscar gêneros para o artista {artist_id}.")
        return []

# Função para obter as faixas da playlist
def get_playlist_tracks(playlist_id, token):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'limit': 100  # Limite máximo por requisição
    }
    all_tracks = []
    total_tracks = 0  # Variável para armazenar o total de faixas da playlist
    
    # Primeira requisição para saber o número total de faixas
    initial_response = requests.get(url, headers=headers, params=params)
    if initial_response.status_code == 200:
        data = initial_response.json()
        total_tracks = data['total']
    else:
        print("Erro ao obter informações da playlist.")
        return []

    # Loop para pegar todas as faixas da playlist
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 401:
            print("Token expirado. Gerando um novo token...")
            token = get_spotify_token(client_id, client_secret)
            headers['Authorization'] = f'Bearer {token}'  # Atualizando o cabeçalho com o novo token
            continue

        if response.status_code != 200:
            print(f"Erro ao buscar faixas da playlist: {response.status_code}")
            break

        data = response.json()
        if 'items' not in data:
            print("Erro ao obter as faixas da playlist.")
            break

        for idx, item in enumerate(data['items']):
            track = item['track']
            if track:  # Verifica se a track não é None
                # Buscar gêneros do artista principal
                artist_id = track['artists'][0]['id']
                genres = get_artist_genres(artist_id, token)

                all_tracks.append({
                    "name": track['name'],
                    "artist": track['artists'][0]['name'],
                    "album": track['album']['name'],
                    "release_date": track['album']['release_date'],
                    "duration_s": track['duration_ms'] / 1000,
                    "popularity": track['popularity'],
                    "genres": ", ".join(genres) if genres else "Unknown"
                })
            
            # Exibir porcentagem de conclusão
            progress = (len(all_tracks) / total_tracks) * 100
            print(f"Progresso: {progress:.2f}% - {len(all_tracks)} de {total_tracks} músicas processadas.")

        # Verificar se há mais páginas de dados
        if data['next']:
            url = data['next']
        else:
            break
        # Para evitar sobrecarga na API
        time.sleep(0.1)

    return all_tracks

# ID da playlist
playlist_id = '1G8IpkZKobrIlXcVPoSIuf'

# Obtendo o token de acesso
token = get_spotify_token(client_id, client_secret)

if token:
    # Obtendo todas as faixas da playlist
    tracks_data = get_playlist_tracks(playlist_id, token)

    # Criar DataFrame e salvar em um arquivo Excel
    if tracks_data:
        df_tracks = pd.DataFrame(tracks_data)
        output_file_path = './top_10000_musicas_com_generos.xlsx'
        df_tracks.to_excel(output_file_path, index=False)
        print(f"Arquivo Excel salvo em: {output_file_path}")
    else:
        print("Nenhuma faixa foi processada.")
else:
    print("Erro ao autenticar na API do Spotify.")
