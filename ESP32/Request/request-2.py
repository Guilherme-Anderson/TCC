import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# Configuração do Firebase
cred = credentials.Certificate('Request/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tcc-2025-1b2ee-default-rtdb.firebaseio.com/'
})

# Referência para a raiz
ref = db.reference('/150625-teste')
dados_por_data = ref.get()

# Verifica se há dados
if not dados_por_data:
    print("Nenhum dado encontrado no Firebase.")
    exit()

# Lista de datas disponíveis
datas_disponiveis = list(dados_por_data.keys())
print("Datas disponíveis no banco:")
for d in datas_disponiveis:
    print(f"- {d}")

# Pergunta ao usuário
escolha = input("\nDigite a data desejada (YYYY-MM-DD) ou 'todas' para exportar tudo: ").strip()

# Lista para armazenar as leituras
leituras = []

# Função para extrair os dados
def extrair_leituras(data_str, registros):
    for timestamp, item in registros.items():
        if isinstance(item, dict) and all(k in item for k in ['ID', 'tempo', 'valorAmp', 'valorVol']):
            leituras.append({
                'data': data_str,
                'timestamp': timestamp,
                'hora': item.get('hora', ''),
                'ID': item['ID'],
                'tempo': item['tempo'],
                'valorAmp': item['valorAmp'],
                'valorVol': item['valorVol']
            })
        else:
            print(f"Registro inválido em {data_str}/{timestamp}: {item}")

# Exporta tudo ou só a data escolhida
if escolha.lower() == 'todas':
    for data_str, registros in dados_por_data.items():
        if isinstance(registros, dict):
            extrair_leituras(data_str, registros)
    nome_arquivo = 'Request/leituras_completas.xlsx'
elif escolha in datas_disponiveis:
    registros = dados_por_data[escolha]
    extrair_leituras(escolha, registros)
    nome_arquivo = f"Request/leituras_{escolha}.xlsx"
else:
    print("Data inválida.")
    exit()

# Verifica se há leituras válidas
if not leituras:
    print("Nenhuma leitura válida encontrada.")
    exit()

# DataFrame e exportação
df = pd.DataFrame(leituras)
df = df.sort_values(by=['data', 'hora'])
df.to_excel(nome_arquivo, index=False)
print(f"Dados exportados para '{nome_arquivo}'")
