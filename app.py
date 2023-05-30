from flask import Flask
from flask_cors import CORS
from main import generate_plot

app = Flask(__name__)
CORS(app)

@app.route('/executar-python', methods=['POST'])
def plot_graph():
    # Chamar a função generate_plot para gerar o gráfico
    plot_data = generate_plot()
    print('plotted')

    # Retornar o gráfico como resposta
    return plot_data, 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run()