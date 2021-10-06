from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

secret_key = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

#####METODO PARA PEGAR TODAS AS VERIFICACOES############
def get_all_verificacoes(user):
    Account_Verificacoes = user['uid']

    #TODO: comentar esta linha
    Account_Verificacoes = "UG3weoTY7PW4SeczHtk6ZAYZ2IM2"

    list_verificacoes = []
    list_itens = []

    #####ESTRUTURANDO TODAS AS VERIFICACOES DOS OS USUARIOS####################
    try:
        conta = db.collection('accounts').document(Account_Verificacoes).get()
        equipeId = conta.get('id_equipe_atual')

        verificacoes_total = db.collection('accounts').document(Account_Verificacoes).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('verificacoes').get()
        
        for v in verificacoes_total:
            list_verificacoes.append({
                'uid': v.id, 
                'aplicado_por': v.get('aplicado_por'), 
                'uid_account': v.get('uid_account'), 
                'cargo': v.get('cargo'),
                'obraDP': v.get('obraDP'),
                'nome_auditor': v.get('nome_auditor'),
                'empresa': v.get('empresa'),
                'assinatura': v.get('assinatura'),
                'assunto': v.get('assunto'),
                'localInspencao': v.get('localInspencao'),
                'referencia': v.get('referencia'),
                'data_checklist': v.get('data_checklist'),
                'name_checklist': v.get('name_checklist'), 
                'total_c': v.get('total_c'),
                'total_nc': v.get('total_nc'), 
                'total_na': v.get('total_na'),
                'uid_checklist': v.get('uid_checklist'),
                # 'itens': list_itens,
                'pdf': v.get('pdf'),
            })

        response = jsonify(list_verificacoes)
        return response, 200
        
    except Exception as e:
        response = jsonify({'erro': 'Erro. Não foi possível acessar as verificações dessa conta.' + str(e)})
        return response, 500

####METODO PARA PEGAR UMA VERIFICACAO############
def get_verificacao(user):
    Account_Verificacoes = str(request.args['id'])
    User_id = user['uid']

    #TODO: comentar esta linha
    User_id = "UG3weoTY7PW4SeczHtk6ZAYZ2IM2"

    verificacaoId = Account_Verificacoes
    list_itens = []

    #####ESTRUTURANDO TODAS AS VERIFICACOES DOS OS USUARIOS####################
    try:
        conta = db.collection('accounts').document(User_id).get()
        equipeId = conta.get('id_equipe_atual')

        verificacao = db.collection('accounts').document(User_id).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('verificacoes').document(verificacaoId).get()  

        itens = db.collection('accounts').document(User_id).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('verificacoes').document(verificacao.id).collection('todos_itens').get()


        for item in itens:
            list_itens.append({
                'comentario' : item.get('comentario'),
                'images' : item.get('images'),
                'pergunta' : item.get('pergunta'),
                'situacao' : item.get('situacao'),
            })

        verificacao_dict = {
            'uid': verificacao.id, 
            'aplicado_por': verificacao.get('aplicado_por'), 
            'uid_account': verificacao.get('uid_account'), 
            'cargo': verificacao.get('cargo'),
            'obraDP': verificacao.get('obraDP'),
            'nome_auditor': verificacao.get('nome_auditor'),
            'empresa': verificacao.get('empresa'),
            'assinatura': verificacao.get('assinatura'),
            'assunto': verificacao.get('assunto'),
            'localInspencao': verificacao.get('localInspencao'),
            'referencia': verificacao.get('referencia'),
            'data_checklist': verificacao.get('data_checklist'),
            'name_checklist': verificacao.get('name_checklist'), 
            'total_c': verificacao.get('total_c'),
            'total_nc': verificacao.get('total_nc'), 
            'total_na': verificacao.get('total_na'),
            'uid_checklist': verificacao.get('uid_checklist'),
            'itens': list_itens,
            'pdf': verificacao.get('pdf'),
        }

        response = jsonify(verificacao_dict)
        return response, 200

    except Exception as e:
        response = jsonify({'erro': 'Erro. Não foi possível acessar a verificação dessa conta.' + str(e)})
        return response, 500
