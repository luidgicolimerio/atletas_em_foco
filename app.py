from flask import Flask, render_template, jsonify, request
import requests
import json
import pandas as pd
import os

os.environ['GROQ_API_KEY'] = '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'

from langchain_groq import ChatGroq

llm=ChatGroq(model="llama-3.1-70b-versatile")

app = Flask(__name__)

# Salva em um arquivo binário o json de resposta da API
def salva_dict(api_response, esporte):

    data = json.loads(api_response)
    pd.to_pickle(data, rf'C:\workspace\atletas_em_foco\assets\api_response_{esporte}.pkl')

    return

######################### Rotas de Páginas #########################################

@app.route('/')
def index():
    # return render_template('index.html')
    return "Hello World"

#Basquete
@app.route('/basquete/<int:game_id>')
def basquete(game_id):
    file_path = os.path.join('assets', 'api_response_basquete.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]
    dados = {
        'date':      response['date'],
        'home_team': response["teams"]["home"]["name"],
        'home_logo': response["teams"]["home"]["logo"],
        'away_team': response["teams"]["away"]["name"],
        'away_logo': response["teams"]["away"]["logo"],
        'home_score':response["scores"]["home"]["total"],
        'away_score':response["scores"]["away"]["total"],
    }
    # # Criação da notícia
    # url = 'http://127.0.0.1:5000/gera_noticia'
    # response = requests.post(url, json=dados)
    # print(response.json())

    return render_template('index.html', data=dados)

#Volei
@app.route('/volei/<int:game_id>')
def volei(game_id):
    file_path = os.path.join('assets', 'api_response_volei.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]
    dados = {
        'date':      response['date'],
        'home_team': response["teams"]["home"]["name"],
        'home_logo': response["teams"]["home"]["logo"],
        'away_team': response["teams"]["away"]["name"],
        'away_logo': response["teams"]["away"]["logo"],
        'home_score':response["scores"]["home"],
        'away_score':response["scores"]["away"],
    }
    return render_template('index.html', data=dados)

#Rugby
@app.route('/rugby/<int:game_id>')
def rugby(game_id):
    file_path = os.path.join('assets', 'api_response_rugby.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]
    dados = {
        'date':      response['date'],
        'home_team': response["teams"]["home"]["name"],
        'home_logo': response["teams"]["home"]["logo"],
        'away_team': response["teams"]["away"]["name"],
        'away_logo': response["teams"]["away"]["logo"],
        'home_score':response["scores"]["home"],
        'away_score':response["scores"]["away"],
    }
    return render_template('index.html', data=dados)

#Handball
@app.route('/handball/<int:game_id>')
def handball(game_id):
    file_path = os.path.join('assets', 'api_response_handball.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]
    dados = {
        'date':      response['date'],
        'home_team': response["teams"]["home"]["name"],
        'home_logo': response["teams"]["home"]["logo"],
        'away_team': response["teams"]["away"]["name"],
        'away_logo': response["teams"]["away"]["logo"],
        'home_score':response["scores"]["home"],
        'away_score':response["scores"]["away"],
    }
    return render_template('index.html', data=dados)

#Football
@app.route('/football/<int:game_id>')
def football(game_id):
    file_path = os.path.join('assets', 'api_response_handball.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]
    dados = {
        'date':      response["fixture"]["date"],
        'home_team': response["teams"]["home"]["name"],
        'home_logo': response["teams"]["home"]["logo"],
        'away_team': response["teams"]["away"]["name"],
        'away_logo': response["teams"]["away"]["logo"],
        'home_score':response["goals"]["home"],
        'away_score':response["goals"]["away"],
    }
    return render_template('index.html', data=dados)

######################### Rotas de Dados #########################################

# # Retorna um json lido do pkl salvo
# @app.route('/data_basquete')
# def data_basquete():
#     data = pd.read_pickle(r'C:\workspace\atletas_em_foco\assets\api_response.pkl')
#     return jsonify(data)

# Retorna dados dos jogos da NBA
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

@app.route('/volei_game', methods=['GET'])
def volei_game():
    url = "https://v1.volleyball.api-sports.io/games?league=24&season=2024"

    payload={}
    headers = {
    'x-rapidapi-key': '28d4d30590983b427633258b52a9684f',
    'x-rapidapi-host': 'v1.volleyball.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    salva_dict(response.text, "volei")

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200
    
@app.route('/rugby_game', methods=['GET'])
def rugby_game():
    url = "https://v1.rugby.api-sports.io/games?league=44&season=2024"

    payload={}
    headers = {
    'x-rapidapi-key': '28d4d30590983b427633258b52a9684f',
    'x-rapidapi-host': 'v1.rugby.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    salva_dict(response.text, "rugby")

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200

@app.route('/handball_game', methods=['GET'])
def handball_game():
    url = "https://v1.handball.api-sports.io/games?league=168&season=2023"

    payload={}
    headers = {
    'x-rapidapi-key': '28d4d30590983b427633258b52a9684f',
    'x-rapidapi-host': 'v1.handball.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    salva_dict(response.text, "handball")

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200

# Retorna os jogso do dia anterior
@app.route('/football_game', methods=['GET'])
def football_game():
    url = "https://v3.football.api-sports.io/fixtures?date=2024-10-22"

    payload={}
    headers = {
    'x-rapidapi-key': '28d4d30590983b427633258b52a9684f',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)


    salva_dict(response.text, "football")

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200

# # Gera notícia a partir de dados passados
@app.route('/gera_noticia/basquete/<int:game_id>', methods=['POST'])
def gera_noticia():
    file_path = os.path.join('assets', 'api_response_basquete.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][10]
    dados = {
        'date':      response['date'],
        'home_team': response["teams"]["home"]["name"],
        'home_logo': response["teams"]["home"]["logo"],
        'away_team': response["teams"]["away"]["name"],
        'away_logo': response["teams"]["away"]["logo"],
        'home_score':response["scores"]["home"]["total"],
        'away_score':response["scores"]["away"]["total"],
    }
    messages = [
        (
            "system",
            """Você é um assistente que possui acesso a dados de partidas de esporte.
               Você deve a partir desses dados gerar uma notícia.
               Exemplo: Time A ganhou de lavada do Time B por 26x10, tiveram muitos atores
               importantes nessa vitória, como o atleta fulano de tal e siclano de tal.
               Gere notícias curtas, porém que deem destaque para as estatiscas recebidas por você
               O prompt conterá tais estátiscicas.
               """,
        ),
        ("human", f"{dados}"), 
    ]
    ai_msg = llm.invoke(messages)
    print(ai_msg.content) 
    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":ai_msg.content}), 200

# futebol  - Diferente +/-
# MMA - Diferente - Stand By

# handball - Igual Check
# basquete - Diferente Check
# volei - Igual Check
# rugby - Igual Check

if __name__ == '__main__':
    app.run(debug=True)

    