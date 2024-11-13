import pandas as pd


file_path = '/Users/marcelomazzonetto/Desktop/Mineracao de dados/Most Streamed Spotify Songs 2024.csv'


df = pd.read_csv(file_path, encoding='latin1')


cols_to_convert = ['Spotify Streams', 'YouTube Views', 'TikTok Views', 
                   'Apple Music Playlist Count', 'Pandora Streams', 'Soundcloud Streams']


for col in cols_to_convert:
    df[col] = df[col].astype(str).str.replace(',', '').astype(float)


print("Valores NaN por coluna antes da limpeza:")
print(df[cols_to_convert].isna().sum())


df[cols_to_convert] = df[cols_to_convert].fillna(0)


df['Total Streams'] = (df['Spotify Streams'] + df['YouTube Views'] + df['TikTok Views'] +
                       df['Apple Music Playlist Count'] + df['Pandora Streams'] +
                       df['Soundcloud Streams'])


df_sorted = df.sort_values(by='Total Streams', ascending=False)


print("Primeiras linhas do DataFrame ordenado:")
print(df_sorted.head())


output_file_path = '/Users/marcelomazzonetto/Desktop/Mineracao de dados/planilha_organizada.xlsx'


df_sorted.to_excel(output_file_path, index=False)

print(f"Arquivo Excel salvo em: {output_file_path}") 