import requests
import pandas as pd
import os
import base64
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter client_id e client_secret do Spotify
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Função para obter token de acesso do Spotify
def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}
    data = {"grant_type": "client_credentials"}
    auth_response = requests.post(auth_url, headers=headers, data=data)
    if auth_response.status_code != 200:
        print("Erro na autenticação com a API do Spotify.")
        return None
    return auth_response.json().get("access_token")

# Função para buscar o ID do artista pelo nome
def get_artist_id(artist_name, token):
    search_url = "https://api.spotify.com/v1/search"
    params = {"q": artist_name, "type": "artist", "limit": 1}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        artists = data.get("artists", {}).get("items", [])
        if artists:
            return artists[0]["id"]  # Retorna o ID do primeiro resultado
    print(f"Erro ao buscar ID para o artista '{artist_name}'.")
    return None

# Função para obter os gêneros do artista
def get_artist_genres(artist_id, token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("genres", [])
    elif response.status_code == 429:  # Rate limit
        retry_after = int(response.headers.get("Retry-After", 1))
        print(f"Rate limit atingido. Aguardando {retry_after} segundos.")
        time.sleep(retry_after)
        return get_artist_genres(artist_id, token)
    else:
        print(f"Erro na API do Spotify para artista {artist_id}: {response.status_code}")
        return []

# Função para processar músicas com gêneros desconhecidos
def update_unknown_genres(file_path, token):
    try:
        # Carregar o arquivo Excel existente
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao carregar o arquivo Excel: {e}")
        return

    # Filtrar músicas com gênero "Unknown"
    unknown_tracks = df[df['genres'] == "Unknown"]
    if unknown_tracks.empty:
        print("Nenhuma música com gênero 'Unknown' encontrada.")
        return

    print(f"{len(unknown_tracks)} músicas com gênero 'Unknown' serão processadas.")

    for idx, row in unknown_tracks.iterrows():
        track_artist_id = row.get('artist_id')  # Assumindo que a coluna `artist_id` existe

        # Buscar ID do artista caso não esteja disponível
        if pd.isna(track_artist_id) or not isinstance(track_artist_id, str):
            track_artist_id = get_artist_id(row['artist'], token)
            if not track_artist_id:
                print(f"Não foi possível encontrar o ID para o artista '{row['artist']}'.")
                continue

        # Obter os gêneros do artista
        genres = get_artist_genres(track_artist_id, token)

        # Atualizar o gênero no DataFrame
        if genres:
            df.at[idx, 'genres'] = ", ".join(genres)
        else:
            print(f"Gêneros para {row['name']} ({row['artist']}) ainda não encontrados.")
            df.at[idx, 'genres'] = "Desconhecido"

        # Exibir progresso
        progress = ((idx + 1) / len(unknown_tracks)) * 100
        print(f"Progresso: {progress:.2f}%")

        # Aguardar para evitar excesso de requisições
        time.sleep(0.1)

    # Salvar progresso atualizado no arquivo Excel
    try:
        df.to_excel(file_path, index=False)
        print(f"Gêneros atualizados salvos em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo Excel: {e}")

# Caminho para o arquivo Excel existente
file_path = './top_10000_musicas_com_generos.xlsx'

# Obter token de acesso
token = get_spotify_token(client_id, client_secret)

if token:
    update_unknown_genres(file_path, token)
else:
    print("Erro ao autenticar na API do Spotify.")
