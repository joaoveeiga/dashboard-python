from flask import Flask, request
from flask_cors import CORS
from main import generate_bar_plot, generate_gaussian, generate_pie_chart
import json

app = Flask(__name__)
CORS(app)

@app.route('/executar-python', methods=['POST'])
def plot_graph():
    data = request.data
    json_data = json.loads(data.decode('utf-8'))
    startDate = json_data['startDate']
    endDate = json_data['endDate']


    # Chamar a função generate_plot para gerar o gráfico
    plot_data = generate_pie_chart(startDate, endDate)

    # Retornar o gráfico como resposta
    return plot_data, 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True, threaded=True)