import pandas as pd
import requests
from collections import Counter
from tqdm import tqdm
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

# Carregar a tabela
file_path = "top_10000_musicas_com_generos_e_letras.xlsx"
df = pd.read_excel(file_path)

# Filtrar as 1000 músicas mais populares
top_1000_populares = df.nlargest(1000, "popularity")

# Função para contar palavras em uma coluna
def contar_palavras(df, coluna):
    palavras = Counter()
    df[coluna] = df[coluna].fillna("").astype(str)
    for conteudo in df[coluna]:
        palavras.update(conteudo.split())
    return palavras.most_common(1000)

# Contar palavras em diferentes setores
top_1000_titulos = contar_palavras(top_1000_populares, "name")
top_1000_artistas = contar_palavras(top_1000_populares, "artist")
top_1000_albuns = contar_palavras(top_1000_populares, "album")
top_1000_generos = contar_palavras(top_1000_populares, "genres")

# Função para buscar letras via API Genius
# Função para buscar letras via API Genius
def buscar_letra(api_url):
    if not isinstance(api_url, str) or api_url.strip() == "" or pd.isna(api_url):
        return ""  # Retorna vazio se a URL for inválida
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            letra = response.json().get("response", {}).get("lyrics", {}).get("lyrics_body", "")
            return letra
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {api_url}: {e}")
    return ""  # Retorna vazio em caso de falha

# Baixar letras apenas das 1000 músicas mais populares
letras = []
for _, row in tqdm(top_1000_populares.iterrows(), total=len(top_1000_populares), desc="Baixando letras"):
    letras.append(buscar_letra(row["letra"]))

# Adicionar as letras baixadas à tabela
top_1000_populares["letra_completa"] = letras

# Contar palavras nas letras das músicas
top_1000_palavras_letras = contar_palavras(top_1000_populares, "letra_completa")

# Criar um novo arquivo Excel com análises separadas
with pd.ExcelWriter("analise_top_1000_popularidade.xlsx") as writer:
    top_1000_populares.to_excel(writer, index=False, sheet_name="Top 1000 Populares")
    pd.DataFrame(top_1000_titulos, columns=["Palavra", "Frequência"]).to_excel(writer, index=False, sheet_name="Top 1000 Títulos")
    pd.DataFrame(top_1000_artistas, columns=["Palavra", "Frequência"]).to_excel(writer, index=False, sheet_name="Top 1000 Artistas")
    pd.DataFrame(top_1000_albuns, columns=["Palavra", "Frequência"]).to_excel(writer, index=False, sheet_name="Top 1000 Álbuns")
    pd.DataFrame(top_1000_generos, columns=["Palavra", "Frequência"]).to_excel(writer, index=False, sheet_name="Top 1000 Gêneros")
    pd.DataFrame(top_1000_palavras_letras, columns=["Palavra", "Frequência"]).to_excel(writer, index=False, sheet_name="Top 1000 Letras")
