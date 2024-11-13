import pandas as pd

def remove_tracks_without_duration(file_path):
    # Carregar o arquivo Excel
    df = pd.read_excel(file_path)

    # Remover músicas sem duração (Duration (s) == NaN)
    df = df.dropna(subset=['Duration (s)'])

    # Salvar o DataFrame filtrado no mesmo arquivo ou em um novo, se preferir
    df.to_excel(file_path, index=False)
    print(f"Músicas sem duração foram removidas. Arquivo atualizado salvo em: {file_path}")

# Caminho do arquivo Excel
correlation_output_file_path = '/Users/marcelomazzonetto/Desktop/Mineracao de dados/correlacao_duracao_visualizacoes.xlsx'

# Chamar a função para remover as músicas sem duração
remove_tracks_without_duration(correlation_output_file_path)
