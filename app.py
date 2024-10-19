from flask import Flask, render_template, jsonify
import requests
import json
import pandas as pd
import os

app = Flask(__name__)

# Salva em um arquivo binário o json de resposta da API
def salva_dict(api_response, esporte):

    data = json.loads(api_response)
    pd.to_pickle(data, rf'C:\workspace\atletas_em_foco\assets\api_response_{esporte}.pkl')

    return

@app.route('/sport/<sport_name>/<int:game_id>')
def index(game_id, sport_name):
    file_path = os.path.join('assets', f'api_response_{sport_name}.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]   # 1200 jogos
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

    salva_dict(response.text, "basquete")

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200


if __name__ == '__main__':
    app.run(debug=True)

    