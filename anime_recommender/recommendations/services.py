import requests
import pandas as pd
import sqlite3

def fetch_animes_by_genre(genre):
    url = f"https://api.jikan.moe/v4/anime?q={genre}&genre={genre}"
    response = requests.get(url)
    
    if response.status_code!= 200:
        print(f"Erro na requisição: Status Code {response.status_code}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
    
    data = response.json()
    
    # Verifica se a chave 'results' existe antes de tentar acessá-la
    if 'results' in data:
        df = pd.DataFrame(data['results'])
        df['genre'] = genre  # Adiciona a coluna de gênero
        return df
    else:
        print("Dados da API não retornaram resultados.")
        return pd.DataFrame()  # Retorna um DataFrame vazio se 'results' não existir

# Exemplo de uso
df_animes = fetch_animes_by_genre("Action")
print(df_animes.head())



def save_to_database(df, db_name):
    if df.empty:
        print("DataFrame is empty. Not saving to database.")
        return
    conn = sqlite3.connect(db_name)
    df.to_sql('animes', conn, if_exists='replace', index=False)
    conn.close()

# Only save to database if df_animes is not empty
if not df_animes.empty:
    save_to_database(df_animes, 'anime_data.db')

def display_animes_from_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='animes'")
    if cursor.fetchone() is None:
        print("No such table: animes")
        return

    cursor.execute("SELECT * FROM animes")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
