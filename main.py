from fastapi import FastAPI
from typing import Tuple
import pandas as pd
import pickle

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Cargar los datos desde los archivos
with open('games.pkl', 'rb') as games_file, open('playtime.pkl', 'rb') as playtime_file, open('reviews.pkl', 'rb') as reviews_file:
    games_data = pickle.load(games_file)
    playtime_data = pickle.load(playtime_file)
    df_reviews = pickle.load(reviews_file)

# Definir la función para contar las reseñas entre dos fechas
def count_reviews_between_dates(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_reviews = df[(df['posted'] >= start_date) & (df['posted'] <= end_date)]
    total_users = len(filtered_reviews['user_id'].unique())
    recommend_percentage = (filtered_reviews['recommend'].astype(int).sum() / len(filtered_reviews)) * 100

    return total_users, recommend_percentage

# Endpoint para contar reseñas
@app.get("/count_reviews")
async def count_reviews_endpoint(start_date: str, end_date: str) -> Tuple[int, float]:
    total_users, recommend_percentage = count_reviews_between_dates(df_reviews, start_date, end_date)
    return total_users, round(recommend_percentage, 2)


