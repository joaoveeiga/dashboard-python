# Importação das bibliotecas
import requests
import json
import pandas as pd
import plotly.express as px
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def create_df(startDate = '2023-01-01', endDate = '2023-05-20'):
    # Integração da API
    API_KEY = '9sHoGBddX4leupSZcm809zBCw88Nd5EpyPgFB04h'
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
    return df

def calculateMode(startDate = '2023-01-01', endDate = '2023-05-20'):
    df = create_df(startDate, endDate)
    # Calcular o dia que mais se repete(moda) 
    same_day_counts = df['sameDay'].value_counts()
    df = df.loc[df['sameDay'] == True]
    print(same_day_counts)
    
def calculatePeakTimes(startDate = '2023-01-01', endDate = '2023-05-20'):
    df = create_df(startDate, endDate)
    # Calculo para ver em minutos o tempo que foi levado
    beginToPeakTimeInMinutes = df['beginToPeakTime'].mean()/60
    peakToEndTimeInMinutes = df['peakToEndTime'].mean()/60

    print(beginToPeakTimeInMinutes, peakToEndTimeInMinutes)
    
def generate_bar_plot(startDate = '2023-01-01', endDate = '2023-05-20'):
    df = create_df(startDate, endDate)

    df['date'] = df['beginTime'].dt.date
    flr_counts = df['date'].value_counts().sort_index()

    # Criar o gráfico de barras
    plt.bar(flr_counts.index, flr_counts.values)

    # Configurar o título e os rótulos dos eixos
    plt.title('FLR Counts by Day')
    plt.xlabel('Date')
    plt.ylabel('FLR Count')

    # Girar os rótulos do eixo x em 45 graus
    plt.xticks(rotation=45)

    # Converter o gráfico em objeto bytes
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer.getvalue()

def generate_gaussian(startDate = '2023-01-01', endDate = '2023-05-20'):
    df = create_df(startDate, endDate)
    # Dados dos tempos de início ao pico
    begin_to_peak_times = df['beginToPeakTime'] / 60

    # Calcula a média e o desvio padrão dos tempos de início ao pico
    mean = begin_to_peak_times.mean()
    std = begin_to_peak_times.std()

    # Plota o histograma dos dados reais
    plt.hist(begin_to_peak_times, bins=30, alpha=0.5, density=True, label='Real Data')

    plt.xlabel('Begin to Peak Time (minutes)')
    plt.ylabel('Density')
    plt.title('Real Data')
    plt.legend()

    # Salva o gráfico em um buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer.getvalue()

def generate_pie_chart(startDate = '2023-01-01', endDate = '2023-05-20'):
    df = create_df(startDate, endDate)
    class_counts = df['classType'].value_counts()

    # Calcula a porcentagem de cada classe em relação ao total
    class_percentages = class_counts / len(df) * 100

    # Seleciona as classes que representam menos de 1%
    small_classes = class_percentages[class_percentages < 1.5]

    # Agrupa as classes menores em uma única classe chamada "Outros"
    class_counts['Outros'] = small_classes.sum()

    # Remove as classes menores
    class_counts = class_counts.drop(small_classes.index)

    class_percentages2 = class_counts / len(df) * 100

    # Configurações do gráfico de pizza
    colors = ['lightblue', 'lightgreen', 'orange', 'pink']
    explode = [0.1] * len(class_counts)  # Separa todos os pedaços da pizza igualmente
    labels = class_counts.index

    # Cria o gráfico de pizza
    plt.pie(class_counts, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Adiciona um círculo branco no centro para transformar em um donut chart (opcional)
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Adiciona um título
    plt.title('Distribution of Class Types')

    # Configura a figura para ser salva em um buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Retorna o buffer contendo a imagem
    return buffer.getvalue()
