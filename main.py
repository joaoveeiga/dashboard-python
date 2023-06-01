import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')


def create_df(startDate = '2022-01-01', endDate = '2023-05-31'):
    API_KEY = '9sHoGBddX4leupSZcm809zBCw88Nd5EpyPgFB04h'
    response = requests.get(f"https://api.nasa.gov/DONKI/FLR?startDate={startDate}&endDate={endDate}&api_key={API_KEY}")

    data = response.json()
    dataFrame = pd.DataFrame(data)

    df = dataFrame.drop(['link', 'linkedEvents', 'flrID', 'instruments'], axis=1)

    df = df.loc[pd.to_datetime(df['beginTime'], errors='coerce').notna()]
    df = df.loc[pd.to_datetime(df['peakTime'], errors='coerce').notna()]
    df = df.loc[pd.to_datetime(df['endTime'], errors='coerce').notna()]

    df['beginToPeakTime'] = (pd.to_datetime(df['peakTime']) - pd.to_datetime(df['beginTime'])).dt.total_seconds()
    df['peakToEndTime'] = (pd.to_datetime(df['endTime']) - pd.to_datetime(df['peakTime'])).dt.total_seconds()

    index_negatives = df[df['beginToPeakTime'] < 0].index
    df = df.drop(index_negatives)
    index_negatives = df[df['peakToEndTime'] < 0].index
    df = df.drop(index_negatives)

    df['beginTime'] = pd.to_datetime(df['beginTime'])
    df['peakTime'] = pd.to_datetime(df['peakTime'])
    df['endTime'] = pd.to_datetime(df['endTime'])

    df['sameDay'] = (df['beginTime'].dt.date == df['peakTime'].dt.date) & (df['beginTime'].dt.date == df['endTime'].dt.date)
    return df

def calculateMode(startDate = '2023-01-01', endDate = '2023-05-20'):
    # df = create_df(startDate, endDate)

    same_day_counts = df['sameDay'].value_counts()
    df = df.loc[df['sameDay'] == True]
    print(same_day_counts)
    
def calculatePeakTimes(startDate = '2023-01-01', endDate = '2023-05-20'):
    # df = create_df(startDate, endDate)

    beginToPeakTimeInMinutes = df['beginToPeakTime'].mean()/60
    peakToEndTimeInMinutes = df['peakToEndTime'].mean()/60

    print(beginToPeakTimeInMinutes, peakToEndTimeInMinutes)
    
def generate_bar_plot(startDate = '2023-01-01', endDate = '2023-05-20'):
    df = create_df(startDate, endDate)

    df['date'] = df['beginTime'].dt.date
    flr_counts = df['date'].value_counts().sort_index()
    plt.bar(flr_counts.index, flr_counts.values)
    plt.title('FLR Counts by Day')
    plt.xlabel('Date')
    plt.ylabel('FLR Count')
    plt.xticks(rotation=45)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()

    return buffer.getvalue()

def generate_pie_chart(startDate = '2023-01-01', endDate = '2023-05-20'):
    df = create_df(startDate, endDate)
    class_counts = df['classType'].value_counts()

    class_percentages = class_counts / len(df) * 100
    small_classes = class_percentages[class_percentages < 2]
    class_counts['Outros'] = small_classes.sum()
    class_counts = class_counts.drop(small_classes.index)
    colors = ['lightblue', 'lightgreen', 'orange', 'pink']
    explode = [0.1] * len(class_counts)  
    labels = class_counts.index
    plt.pie(class_counts, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Distribution of Class Types')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()
    
    return buffer.getvalue()

def generate_gaussian(startDate = '2023-01-01', endDate = '2023-05-20'):
    df2 = create_df(startDate, endDate)
    begin_to_peak_times = df2['beginToPeakTime'] / 60
    mean = begin_to_peak_times.mean()
    std = begin_to_peak_times.std()
    
    plt.hist(begin_to_peak_times, bins=30, alpha=0.5, density=True, label='Real Data')
    plt.xlabel('Begin to Peak Time (minutes)')
    plt.ylabel('Density')
    plt.title('Real Data')
    plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()

    return buffer.getvalue()