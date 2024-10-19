from flask import Flask, render_template, jsonify
import requests
import json
import pandas as pd

app = Flask(__name__)

# Salva em um arquivo binário o json de resposta da API
def salva_dict(api_response):

    data = json.loads(api_response)
    pd.to_pickle(data, r'C:\workspace\atletas_em_foco\assets\api_response.pkl')

    return

@app.route('/')
def index():
    data = pd.read_pickle(r'C:\workspace\atletas_em_foco\assets\api_response.pkl')
    response = data["response"][1]   # 1200 jogos
    dados = {
        'date':      response['date'],
        'home_team': response["teams"]["home"]["name"],
        'home_logo': response["teams"]["home"]["logo"],
        'away_logo': response["teams"]["away"]["name"],
        'home_score':response["scores"]["home"]["total"],
        'away_score':response["scores"]["away"]["total"],
    }
    return render_template('index.html', data=dados)

# Retorna um json lido do pkl salvo
@app.route('/data_basquete')
def data_basquete():
    data = pd.read_pickle(r'C:\workspace\atletas_em_foco\assets\api_response.pkl')
    return jsonify(data)

@app.route('/basquete_game', methods=['GET'])
def basquete_game():     # League ID( NBA = 12 ), Season ( 2024-2025 ), data ( YYYY-MM-DD )
    url = "https://v1.basketball.api-sports.io/games?league=12&season=2024-2025"

    payload={}
    headers = {
    'x-rapidapi-key': '28d4d30590983b427633258b52a9684f',
    'x-rapidapi-host': 'v1.basketball.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    salva_dict(response.text)

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200


if __name__ == '__main__':
    app.run(debug=True)

    