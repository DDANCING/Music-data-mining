import pandas as pd

def calcular_popularidade_duas_planilhas():
    # Caminhos das planilhas
    caminho_rank = r"3-rankear dados\analise_top_1000_popularidade.xlsx"
    caminho_musica = r"3-rankear dados\top_10000_musicas_com_generos_e_letras.xlsx"
    
    # Ler a planilha de ranking
    df_rank = pd.read_excel(caminho_rank)
    # Ler a planilha de músicas
    df_musica = pd.read_excel(caminho_musica)
    
    # Verificar se a coluna 'popularity' existe em ambas as planilhas
    if 'popularity' not in df_rank.columns or 'popularity' not in df_musica.columns:
        raise ValueError("A coluna 'popularity' não foi encontrada em uma ou ambas as planilhas.")
    
    # Calcular a popularidade máxima na planilha de ranking
    max_popularity = df_rank['popularity'].max()

    # Calcular a porcentagem de popularidade para a planilha de músicas
    df_musica['percentual_popularidade'] = (df_musica['popularity'] / max_popularity) * 100

    # Salvar a nova planilha com a porcentagem calculada
    novo_caminho = r"3-rankear dados\top_10000_musicas_com_percentual.xlsx"
    df_musica.to_excel(novo_caminho, index=False)
    print(f"Planilha salva com sucesso em {novo_caminho}")

if __name__ == "__main__":
    calcular_popularidade_duas_planilhas()
