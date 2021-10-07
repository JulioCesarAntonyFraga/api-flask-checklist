from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

####METODO PARA PEGAR TODAS AS CHECKLISTS############
def get_all_checklists(user):
    Account_Checklists = user['uid']

    #TODO: comentar esta linha
    Account_Checklists = "UG3weoTY7PW4SeczHtk6ZAYZ2IM2"

    dict_checklists = {}
    list_checklists = []
    list_perguntas = []
    
    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################
    conta = db.collection('accounts').document(Account_Checklists).get()
    equipeId = conta.get('id_equipe_atual')

    Checklists = db.collection('accounts').document(Account_Checklists).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('checklists').get()
 
    try:
        for c in Checklists:

            dict_checklists = {
                'uid': c.id, 
                'deleted_categoria': c.get('deleted_categoria'), 
                'assunto': c.get('assunto'),  
                'numero': c.get('numero'),  
                'revisao': c.get('revisao'), 
                'title': c.get('title'), 
                'type_checklist': c.get('type_checklist'),
                'perguntas': list_perguntas,}

            list_checklists.append(dict_checklists)
            list_perguntas = []

        response = jsonify(list_checklists)
        return response, 200
    except Exception as e:
        response = jsonify({'erro': 'Erro. Não foi possível acessar as checklists dessa conta.'})
        return response, 500

####METODO PARA PEGAR UMA CHECKLIST############
def get_checklist(user):
    Account_Checklist = str(request.args['id'])
    User_id = user['uid']

    #TODO: comentar esta linha
    User_id = "UG3weoTY7PW4SeczHtk6ZAYZ2IM2"

    checklist = Account_Checklist

    #####ESTRUTURANDO OS DADOS DA CHECKLIST####################]
    conta = db.collection('accounts').document(User_id).get()
    equipeId = conta.get('id_equipe_atual')

    Checklist_Firebase = db.collection('accounts').document(User_id).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('checklists').document(checklist).get()
    perguntas_Checklists = db.collection('accounts').document(User_id).collection('equipe').document('equipes_criadas').collection('all_data').document(equipeId).collection('checklists').document(checklist).collection('perguntas').get()

    list_perguntas = []

    try:
        for p in perguntas_Checklists:
            list_perguntas.append(
            {
                'uid': p.id,
                'pergunta': p.get('pergunta'),
                'images': p.get('images'),
            })
        dict_checklists = {
            'uid': Checklist_Firebase.id, 
            'deleted_categoria': Checklist_Firebase.get('deleted_categoria'), 
            'assunto': Checklist_Firebase.get('assunto'),  
            'numero': Checklist_Firebase.get('numero'),  
            'descricao': Checklist_Firebase.get('descricao'),  
            'revisao': Checklist_Firebase.get('revisao'), 
            'title': Checklist_Firebase.get('title'), 
            'itens': len(list_perguntas),
            'type_checklist': Checklist_Firebase.get('type_checklist'),
            'perguntas' : list_perguntas,
        }
        
        response = jsonify(dict_checklists)
        return response, 200
    except Exception as e:
        response = jsonify({'erro': 'Erro. Não foi possível acessar a checklist dessa conta.'})
        return response, 500
