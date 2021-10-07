from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

secret_key = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

def get_all_plano_de_acao(user):
    Account_Planos_de_acao = user['uid']

    #TODO: comentar esta linha
    Account_Planos_de_acao = "UG3weoTY7PW4SeczHtk6ZAYZ2IM2"

    list_planos_de_acao = []
    list_perguntas = []

    try:
        conta = db.collection('accounts').document(Account_Planos_de_acao).get()
        equipeId = conta.get('id_equipe_atual')

        planos_de_acao = db.collection('accounts').document(Account_Planos_de_acao).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('planos_de_acao').get()
        
        for plano in planos_de_acao:
            perguntas = db.collection('accounts').document(Account_Planos_de_acao).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('planos_de_acao').document(plano.id).collection('perguntas_plano_de_acao').get()

            for pergunta in perguntas:
                list_perguntas.append({
                    'perguntas_plano_de_acao' : pergunta.get('perguntas_plano_de_acao'),
                })

            list_planos_de_acao.append({
                'uid': plano.id, 
                'descricao': plano.get('descricao'), 
                'title': plano.get('title'), 
                'perguntas': list_perguntas,
            })

        response = jsonify(list_planos_de_acao)
        return response, 200
    except Exception as e:
        response = jsonify({'erro': 'Erro. Não foi possível acessar os planos ed ação dessa conta.' + str(e)})
        return response, 500

def get_plano_de_acao(user):
    PlanoDeAcaoId = str(request.args['id'])

    Account_Planos_de_acao = user['uid']

    #TODO: comentar esta linha
    Account_Planos_de_acao = "UG3weoTY7PW4SeczHtk6ZAYZ2IM2"

    list_planos_de_acao = []
    list_perguntas = []

    try:
        conta = db.collection('accounts').document(Account_Planos_de_acao).get()
        equipeId = conta.get('id_equipe_atual')

        plano = db.collection('accounts').document(Account_Planos_de_acao).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('planos_de_acao').document(PlanoDeAcaoId).get()
    
        perguntas = db.collection('accounts').document(Account_Planos_de_acao).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('planos_de_acao').document(plano.id).collection('perguntas_plano_de_acao').get()

        for pergunta in perguntas:
            list_perguntas.append({
                'uid': pergunta.id,
                'pergunta_plano_de_acao' : pergunta.get('perguntas_plano_de_acao'),
            })

        plano_de_acao_dict = {
            'uid': plano.id, 
            'descricao': plano.get('descricao'), 
            'title': plano.get('title'), 
            'perguntas': list_perguntas,
        }

        response = jsonify(plano_de_acao_dict)
        return response, 200
    except Exception as e:
        response = jsonify({'erro': 'Erro. Não foi possível acessar o plano de ação dessa conta.' + str(e)})
        return response, 500
