# Importação das bibliotecas
import requests
import json
import pandas as pd
import plotly.express as px

# Integração da API
API_KEY = '9sHoGBddX4leupSZcm809zBCw88Nd5EpyPgFB04h'
startDate = '2023-01-01'
endDate = '2023-05-20'
response = requests.get(f"https://api.nasa.gov/DONKI/FLR?startDate={startDate}&endDate={endDate}&api_key={API_KEY}")

data = response.json()
dataFrame = pd.DataFrame(data)

# Excluir colunas que da API que não usaremos
df = dataFrame.drop(['link', 'linkedEvents', 'flrID', 'instruments'], axis=1)

# Verificação para excluir dados com erro(Nesse caso dados que não são número para representar o tempo)
df = df.loc[pd.to_datetime(df['beginTime'], errors='coerce').notna()]
df = df.loc[pd.to_datetime(df['peakTime'], errors='coerce').notna()]
df = df.loc[pd.to_datetime(df['endTime'], errors='coerce').notna()]

# Calculo para ver o tempo do inicio ao pico e do pico ao fim
df['beginToPeakTime'] = (pd.to_datetime(df['peakTime']) - pd.to_datetime(df['beginTime'])).dt.total_seconds()
df['peakToEndTime'] = (pd.to_datetime(df['endTime']) - pd.to_datetime(df['peakTime'])).dt.total_seconds()

# Verificação para excluir dados com erro(Nesse caso que o tempo levado seja inferior a 0)
index_negatives = df[df['beginToPeakTime'] < 0].index
df = df.drop(index_negatives)
index_negatives = df[df['peakToEndTime'] < 0].index
df = df.drop(index_negatives)

# Mostrar na tela em formato de tabelas os dados
df['beginTime'] = pd.to_datetime(df['beginTime'])
df['peakTime'] = pd.to_datetime(df['peakTime'])
df['endTime'] = pd.to_datetime(df['endTime'])

df['sameDay'] = (df['beginTime'].dt.date == df['peakTime'].dt.date) & (df['beginTime'].dt.date == df['endTime'].dt.date)

# Calcular o dia que mais se repete(moda) 
same_day_counts = df['sameDay'].value_counts()
df = df.loc[df['sameDay'] == True]
print(same_day_counts)

# Calculo para ver em minutos o tempo que foi levado
beginToPeakTimeInMinutes = df['beginToPeakTime'].mean()/60
peakToEndTimeInMinutes = df['peakToEndTime'].mean()/60

print(beginToPeakTimeInMinutes, peakToEndTimeInMinutes)
df



