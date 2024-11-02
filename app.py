from flask import Flask, render_template, jsonify, request
import requests
import json
import pandas as pd
import os
from datetime import datetime

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
    return render_template('index.html')

@app.route('/esporte/<esporte_name>')
def esporte(esporte_name):
    return render_template('esporte.html', esporte=esporte_name)

#Esportes
@app.route('/sport/<sport_name>/<int:game_id>')
def sport(game_id, sport_name):
    file_path = os.path.join('assets', f'api_response_{sport_name}.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]
    if sport_name == "basquete":
        dados = {
            'date':      response['date'],
            'home_team': response["teams"]["home"]["name"],
            'home_logo': response["teams"]["home"]["logo"],
            'away_team': response["teams"]["away"]["name"],
            'away_logo': response["teams"]["away"]["logo"],
            'home_score':response["scores"]["home"]["total"],
            'away_score':response["scores"]["away"]["total"],
        }
    elif sport_name == "football":
        dados = {
            'date':      response["fixture"]["date"],
            'home_team': response["teams"]["home"]["name"],
            'home_logo': response["teams"]["home"]["logo"],
            'away_team': response["teams"]["away"]["name"],
            'away_logo': response["teams"]["away"]["logo"],
            'home_score':response["goals"]["home"],
            'away_score':response["goals"]["away"],
        }
    elif sport_name == "mma":
        dados = {
            'date':      response['date'],
            'category':  response['category'],
            'home_team': response["fighters"]["first"]["name"],
            'home_logo': response["fighters"]["first"]["logo"],
            'home_score':response["fighters"]["first"]["winner"],
            'away_team': response["fighters"]["second"]["name"],
            'away_logo': response["fighters"]["second"]["logo"],
            'away_score':response["fighters"]["second"]["winner"],
        }
    else:
        dados = {
            'date':      response['date'],
            'home_team': response["teams"]["home"]["name"],
            'home_logo': response["teams"]["home"]["logo"],
            'away_team': response["teams"]["away"]["name"],
            'away_logo': response["teams"]["away"]["logo"],
            'home_score':response["scores"]["home"],
            'away_score':response["scores"]["away"],
        }
    # Criação da notícia
    url = f'http://127.0.0.1:5000/gera_noticia/sport/{sport_name}/{game_id}'
    response = requests.post(url, json=dados)
    noticia = response.json()
    
    return render_template('noticia.html', data=dados, noticia=noticia)


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

@app.route('/football_game', methods=['GET'])
def football_game():
    data_atual = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={data_atual}"

    payload={}
    headers = {
    'x-rapidapi-key': '28d4d30590983b427633258b52a9684f',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)


    salva_dict(response.text, "football")

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200


@app.route('/mma_game', methods=['GET'])
def mma_game():
    data_atual = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v1.mma.api-sports.io/fights?date=2023-08-26"

    payload={}
    headers = {
    'x-rapidapi-key': '28d4d30590983b427633258b52a9684f',
    'x-rapidapi-host': 'v1.mma.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)


    salva_dict(response.text, "mma")

    return jsonify({"message": "Requisição realizada com sucesso", "Jogos":response.text}), 200

# # Gera notícia a partir de dados passados
@app.route('/gera_noticia/sport/<sport_name>/<int:game_id>', methods=['POST'])
def gera_noticia(sport_name, game_id):
    file_path = os.path.join('assets', f'api_response_{sport_name}.pkl')
    data = pd.read_pickle(file_path)
    response = data["response"][game_id]
    if sport_name == "basquete":
            dados = {
            'date':      response['date'],
            'home_team': response["teams"]["home"]["name"],
            'home_logo': response["teams"]["home"]["logo"],
            'away_team': response["teams"]["away"]["name"],
            'away_logo': response["teams"]["away"]["logo"],
            'home_score':response["scores"]["home"]["total"],
            'away_score':response["scores"]["away"]["total"],
        }
    elif sport_name == "football":
        dados = {
            'date':      response["fixture"]["date"],
            'home_team': response["teams"]["home"]["name"],
            'home_logo': response["teams"]["home"]["logo"],
            'away_team': response["teams"]["away"]["name"],
            'away_logo': response["teams"]["away"]["logo"],
            'home_score':response["goals"]["home"],
            'away_score':response["goals"]["away"],
        }
    elif sport_name == "mma":
        dados = {
            'date':      response['date'],
            'category':  response['category'],
            'home_team': response["fighters"]["first"]["name"],
            'home_logo': response["fighters"]["first"]["logo"],
            'home_score':response["fighters"]["first"]["winner"],
            'away_team': response["fighters"]["second"]["name"],
            'away_logo': response["fighters"]["second"]["logo"],
            'away_score':response["fighters"]["second"]["winner"],
        }
    else:
        dados = {
            'date':      response['date'],
            'home_team': response["teams"]["home"]["name"],
            'home_logo': response["teams"]["home"]["logo"],
            'away_team': response["teams"]["away"]["name"],
            'away_logo': response["teams"]["away"]["logo"],
            'home_score':response["scores"]["home"],
            'away_score':response["scores"]["away"],
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

if __name__ == '__main__':
    app.run(debug=True)

    