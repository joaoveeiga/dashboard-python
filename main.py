# # Importação das bibliotecas
# import requests
# import json
# import pandas as pd
# import plotly.express as px

# # Integração da API
# API_KEY = '9sHoGBddX4leupSZcm809zBCw88Nd5EpyPgFB04h'
# startDate = '2023-01-01'
# endDate = '2023-05-20'
# response = requests.get(f"https://api.nasa.gov/DONKI/FLR?startDate={startDate}&endDate={endDate}&api_key={API_KEY}")

# data = response.json()
# dataFrame = pd.DataFrame(data)

# # Excluir colunas que da API que não usaremos
# df = dataFrame.drop(['link', 'linkedEvents', 'flrID', 'instruments'], axis=1)

# # Verificação para excluir dados com erro(Nesse caso dados que não são número para representar o tempo)
# df = df.loc[pd.to_datetime(df['beginTime'], errors='coerce').notna()]
# df = df.loc[pd.to_datetime(df['peakTime'], errors='coerce').notna()]
# df = df.loc[pd.to_datetime(df['endTime'], errors='coerce').notna()]

# # Calculo para ver o tempo do inicio ao pico e do pico ao fim
# df['beginToPeakTime'] = (pd.to_datetime(df['peakTime']) - pd.to_datetime(df['beginTime'])).dt.total_seconds()
# df['peakToEndTime'] = (pd.to_datetime(df['endTime']) - pd.to_datetime(df['peakTime'])).dt.total_seconds()

# # Verificação para excluir dados com erro(Nesse caso que o tempo levado seja inferior a 0)
# index_negatives = df[df['beginToPeakTime'] < 0].index
# df = df.drop(index_negatives)
# index_negatives = df[df['peakToEndTime'] < 0].index
# df = df.drop(index_negatives)

# # Mostrar na tela em formato de tabelas os dados
# df['beginTime'] = pd.to_datetime(df['beginTime'])
# df['peakTime'] = pd.to_datetime(df['peakTime'])
# df['endTime'] = pd.to_datetime(df['endTime'])

# df['sameDay'] = (df['beginTime'].dt.date == df['peakTime'].dt.date) & (df['beginTime'].dt.date == df['endTime'].dt.date)

# # Calcular o dia que mais se repete(moda) 
# same_day_counts = df['sameDay'].value_counts()
# df = df.loc[df['sameDay'] == True]
# print(same_day_counts)

# # Calculo para ver em minutos o tempo que foi levado
# beginToPeakTimeInMinutes = df['beginToPeakTime'].mean()/60
# peakToEndTimeInMinutes = df['peakToEndTime'].mean()/60

# print(beginToPeakTimeInMinutes, peakToEndTimeInMinutes)
# df

# import matplotlib.pyplot as plt

# df['date'] = df['beginTime'].dt.date
# flr_counts = df['date'].value_counts().sort_index()

# plt.figure(figsize=(12, 6))
# plt.bar(flr_counts.index, flr_counts.values)
# plt.xlabel('Date')
# plt.ylabel('FLR Count')
# plt.title('FLR Counts by Day')
# plt.xticks(rotation=45)
# # plt.show()

# import plotly.graph_objects as go
# import os
# def generate_flr_counts_chart():
#     df['date'] = df['beginTime'].dt.date
#     flr_counts = df['date'].value_counts().sort_index()

#     fig = go.Figure(data=[go.Bar(x=flr_counts.index, y=flr_counts.values)])

#     fig.update_layout(
#         title='FLR Counts by Day',
#         xaxis=dict(title='Date'),
#         yaxis=dict(title='FLR Count'),
#         xaxis_tickangle=-45
#     )

#     # Gerar o caminho do arquivo
#     file_path = os.path.join(os.getcwd(), 'flr_counts.html')

#     # Salvar o gráfico como arquivo HTML
#     fig.write_html(file_path)

#     # Retornar o caminho do arquivo
#     return file_path

# generate_flr_counts_chart()

import io
import matplotlib.pyplot as plt

def generate_plot():
    # Dados para o gráfico
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    # Criar o gráfico
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Gráfico de exemplo')

    # Converter o gráfico em objeto bytes
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer.getvalue()