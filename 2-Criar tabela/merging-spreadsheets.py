import pandas as pd
import requests
import time

# Função para buscar URL da letra de uma música (usando Genius como exemplo)
def get_lyrics_url(track_name, artist_name, genius_token):
    base_url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {genius_token}"}
    params = {"q": f"{track_name} {artist_name}"}
    
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        hits = data.get("response", {}).get("hits", [])
        if hits:
            # Retorna o URL do primeiro resultado
            return hits[0]["result"]["url"]
    else:
        print(f"Erro ao buscar letra para {track_name} - {artist_name}: {response.status_code}")
    return None

# Caminho para o arquivo Excel
file_path = "./top_10000_musicas_infos.xlsx"

# Token de acesso para a API do Genius (substitua pelo seu)
genius_token = "SUA_GENIUS_API_TOKEN"

# Ler o arquivo Excel existente
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Arquivo {file_path} não encontrado.")
    exit()

# Verificar se as colunas necessárias existem
if "name" not in df.columns or "lyrics_url" not in df.columns:
    print("As colunas 'name' e 'lyrics_url' são necessárias na planilha.")
    exit()

# Iterar sobre as músicas sem URL de letra
for idx, row in df[df["lyrics_url"].isnull()].iterrows():
    track_name = row["name"]
    artist_name = row["artist"]  # Supondo que existe uma coluna "artist"
    
    # Buscar URL da letra
    lyrics_url = get_lyrics_url(track_name, artist_name, genius_token)
    if lyrics_url:
        df.at[idx, "lyrics_url"] = lyrics_url
        print(f"Lyrics URL encontrado para '{track_name}' - '{artist_name}': {lyrics_url}")
    else:
        print(f"Lyrics URL não encontrado para '{track_name}' - '{artist_name}'.")

    # Aguardar para evitar excesso de requisições na API
    time.sleep(1)

# Salvar progresso no arquivo Excel
df.to_excel(file_path, index=False)
print(f"Letras adicionadas e salvas em: {file_path}")
