import pandas as pd

# Carregar o arquivo Excel já processado
file_path = '/Users/marcelomazzonetto/Desktop/Mineracao de dados/planilha_organizada.xlsx'
df = pd.read_excel(file_path)

# Colunas de visualizações
view_cols = ['Spotify Streams', 'YouTube Views', 'TikTok Views', 
             'Apple Music Playlist Count', 'Pandora Streams', 'Soundcloud Streams']

# Converter as colunas para float, lidando com erros
for col in view_cols:
    # Remover espaços em branco e converter para numérico
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.strip(), errors='coerce')

# Exibir tipos de dados das colunas para verificar se a conversão foi bem-sucedida
print(df[view_cols].dtypes)

# Calcular a soma total de visualizações
df['Total Views'] = df[view_cols].sum(axis=1, skipna=True)  # Ignora NaN ao somar

# Converter 'Duration (s)' para numérico, lidando com erros
df['Duration (s)'] = pd.to_numeric(df['Duration (s)'], errors='coerce')

# Criar um DataFrame com a duração e total de visualizações
correlation_df = df[['Track', 'Duration (s)', 'Total Views']]


correlation = correlation_df[['Duration (s)', 'Total Views']].corr().iloc[0, 1]
print(f"A correlação entre a duração da música e o total de visualizações é: {correlation}")


correlation_output_file_path = '/Users/marcelomazzonetto/Desktop/Mineracao de dados/correlacao_duracao_visualizacoes.xlsx'
correlation_df.to_excel(correlation_output_file_path, index=False)

print(f"Arquivo de correlação salvo em: {correlation_output_file_path}")
