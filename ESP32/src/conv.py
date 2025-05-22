import json
import pandas as pd

# Carregue o arquivo JSON
with open('dados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extraia os dados da chave "data"
dados = data['data']

# Crie uma lista para armazenar os dados formatados
tabela = []

# Percorra cada item no JSON
for key, item in dados.items():
    tabela.append({
        'timestamp': item['timestamp'],
        'value': item['value']
    })

# Converta a lista em um DataFrame do Pandas
df = pd.DataFrame(tabela)

# Salve o DataFrame como um arquivo CSV
df.to_csv('tabela.csv', index=False, encoding='utf-8')
print('Arquivo CSV salvo como tabela.csv')
