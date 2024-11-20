import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def calcular_metricas():
    # Caminho da planilha gerada
    caminho_planilha = r"4-script de popularidade\top_10000_musicas_com_percentual.xlsx"

    # Ler a planilha
    df = pd.read_excel(caminho_planilha)

    # Verificar se as colunas necessárias existem
    if 'popularity' not in df.columns or 'percentual_popularidade' not in df.columns:
        raise ValueError("A planilha deve conter as colunas 'popularity' e 'percentual_popularidade'.")

    # Criar rótulos binários para valores reais e previstos
    y_true = (df['popularity'] >= 50).astype(int)  # 1 se for relevante, 0 caso contrário
    y_pred = (df['percentual_popularidade'] >= 50).astype(int)  # 1 se for relevante, 0 caso contrário

    # Calcular Precisão, Recall e F1 Score
    precisao = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    # Exibir os resultados no console
    print("Métricas calculadas:")
    print(f"Precisão: {precisao:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")

if __name__ == "__main__":
    calcular_metricas()
