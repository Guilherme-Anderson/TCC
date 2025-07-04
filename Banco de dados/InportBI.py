import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# Caminho para a chave JSON
cred = credentials.Certificate("C:/Users/guilh/OneDrive/Documentos/GitHub/TCC/Banco de dados/credencial.json")

# Inicialize o app (somente uma vez)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://tcc-2025-1b2ee-default-rtdb.firebaseio.com/'  # Altere aqui
    })

# Referência ao nó desejado no Realtime Database
ref = db.reference('/dados')  # Altere o caminho conforme seu nó

# Pegue os dados e converta para DataFrame
data = ref.get()
df = pd.DataFrame.from_dict(data, orient='index')  # orient='index' para quando os dados forem armazenados por push()

# Exibir para o Power BI
df
