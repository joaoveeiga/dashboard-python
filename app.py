from flask import Flask, request
from flask_cors import CORS
from main import generate_bar_plot,  generate_pie_chart, create_df, generate_gaussian
import json

app = Flask(__name__)
CORS(app)


@app.route('/plot-pie-chart', methods=['POST'])
def plot_pie_chart():
    data = request.data
    json_data = json.loads(data.decode('utf-8'))
    startDate = json_data['startDate']
    endDate = json_data['endDate']

    # Chamar a função generate_pie_chart para gerar o gráfico de pizza, passando o dataframe df
    plot_data = generate_pie_chart(startDate, endDate)

    # Retornar o gráfico de pizza como resposta
    return plot_data, 200, {'Content-Type': 'image/png'}

@app.route('/plot-gaussian', methods=['POST'])
def plot_gaussian():
    data = request.data
    json_data = json.loads(data.decode('utf-8'))
    startDate = json_data['startDate']
    endDate = json_data['endDate']

    # Chamar a função generate_gaussian para gerar o gráfico gaussiano, passando o dataframe df
    plot_data = generate_gaussian(startDate, endDate)

    # Retornar o gráfico gaussiano como resposta
    return plot_data, 200, {'Content-Type': 'image/png'}

@app.route('/plot-bar-chart', methods=['POST'])
def bar_plot():
    data = request.data
    json_data = json.loads(data.decode('utf-8'))
    startDate = json_data['startDate']
    endDate = json_data['endDate']

    plot_data = generate_bar_plot(startDate, endDate)

    return plot_data, 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
