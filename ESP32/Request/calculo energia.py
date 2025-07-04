import os
import pandas as pd

# Caminho onde estão os arquivos Excel
pasta = "Request"

# Lista apenas arquivos .xlsx da pasta
arquivos = [f for f in os.listdir(pasta) if f.endswith(".xlsx")]

# Exibe os arquivos disponíveis
print("Arquivos disponíveis:")
for i, arquivo in enumerate(arquivos):
    print(f"{i + 1}: {arquivo}")

# Pede ao usuário para escolher o arquivo
indice = int(input("\nDigite o número do arquivo que deseja usar: ")) - 1
arquivo_escolhido = arquivos[indice]
caminho_arquivo = os.path.join(pasta, arquivo_escolhido)

# Carrega o Excel
df = pd.read_excel(caminho_arquivo)

# Converte colunas para numérico (caso estejam como texto com vírgula)
df["valorAmp"] = df["valorAmp"].astype(str).str.replace(",", ".").astype(float)
df["valorVol"] = df["valorVol"].astype(str).str.replace(",", ".").astype(float)

# Junta data e hora para criar coluna datetime
df["datetime"] = pd.to_datetime(df["data"].astype(str) + " " + df["hora"].astype(str))

# Calcula potência instantânea
df["potencia_W"] = df["valorAmp"] * df["valorVol"]

# Calcula tempo entre medições em segundos e depois converte para horas
df["delta_s"] = df["datetime"].diff().dt.total_seconds().fillna(0)
df["delta_h"] = df["delta_s"] / 3600

# Calcula energia gerada em cada intervalo (Wh)
df["energia_Wh"] = df["potencia_W"] * df["delta_h"]

# Soma total
energia_total = df["energia_Wh"].sum()

print(f"\nEnergia total gerada no dia ({arquivo_escolhido}): {energia_total:.2f} Wh")
