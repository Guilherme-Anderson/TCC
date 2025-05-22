import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# Configuração do Firebase
cred = credentials.Certificate('Request/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tcc-2025-1b2ee-default-rtdb.firebaseio.com/'
})

# Acessa os dados no Firebase
ref = db.reference('/teste')
dados = ref.get()

# Verifica se os dados foram carregados corretamente
if not dados:
    print("Nenhum dado encontrado no Firebase.")
    exit()

# Processa os dados
leituras = []
for key, item in dados.items():
    # Verifica se todas as chaves necessárias estão presentes
    if isinstance(item, dict) and 'ID' in item and 'tempo' in item and 'valor' in item:
        leituras.append({
            'ID': item['ID'],
            'tempo': item['tempo'],
            'valor': item['valor']
        })
    else:
        print(f"Dados incompletos ou inválidos no nó {key}: {item}")

# Verifica se há leituras válidas
if not leituras:
    print("Nenhuma leitura válida encontrada.")
    exit()

# Ordena as leituras pelo ID
leituras.sort(key=lambda x: x['ID'])

# Converte para um DataFrame do Pandas
df = pd.DataFrame(leituras)

# Exporta para Excel
df.to_excel('Request/leituras_com_ID.xlsx', index=False)
print("Dados exportados para leituras_com_ID.xlsx")