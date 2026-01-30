import pandas as pd
import numpy as np

# 1. Carregar o dataset
df = pd.read_csv("Energy_consumption.csv")  # Substituir com o caminho correto se necessário

# 2. Definir colunas para manipulação (excluindo a target 'EnergyConsumption')
colunas_numericas = ['Temperature', 'Humidity', 'RenewableEnergy']
colunas_categoricas = ['HVACUsage', 'LightingUsage']

# 3. Introduzir missing values (5%)
np.random.seed(42)  # Reprodutibilidade
for col in colunas_numericas:
    missing_indices = df.sample(frac=0.05).index
    df.loc[missing_indices, col] = np.nan

for col in colunas_categoricas:
    missing_indices = df.sample(frac=0.05).index
    df.loc[missing_indices, col] = np.nan

# 4. Introduzir outliers (2%)
def adicionar_outliers(df, col, multiplicador=3):
    outlier_indices = df.sample(frac=0.02).index
    media = df[col].mean()
    desvio = df[col].std()
    df.loc[outlier_indices, col] = media + multiplicador * desvio

for col in colunas_numericas:
    adicionar_outliers(df, col)

# 5. Guardar novo dataset
df.to_csv("Energy_consumption_corrompido.csv", index=False)
print("✅ Dataset com missing values e outliers (exceto na variável alvo 'EnergyConsumption').")
