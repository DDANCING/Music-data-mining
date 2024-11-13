import os
import requests
import base64
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    
    # Codifica o client_id e client_secret em base64
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    
    # Faz a requisição
    auth_response = requests.post(auth_url, headers=headers, data=data)
    
    # Verifique o status da resposta
    if auth_response.status_code != 200:
        print("Erro na autenticação com a API do Spotify.")
        print(f"Status Code: {auth_response.status_code}")
        print(f"Resposta: {auth_response.text}")
        return None
    
    # Tenta converter para JSON
    try:
        auth_response_data = auth_response.json()
    except requests.exceptions.JSONDecodeError as e:
        print("Erro ao decodificar a resposta como JSON:", e)
        print("Conteúdo da resposta:", auth_response.text)
        return None
    
    # Retorna o token de acesso
    return auth_response_data.get("access_token")

# Chamada da função
token = get_spotify_token(client_id, client_secret)
if token:
    print("Token obtido com sucesso:", token)
else:
    print("Falha ao obter o token.")
