from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import  request
import datetime
import jwt
from api_firebase import *

secret_key = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

####METODO PARA LOGAR UM USUARIO DO FIREBASE############
def Login():
    json_data = request.json
    try:
        user= auth_pyrebase.sign_in_with_email_and_password(json_data['email'], json_data['senha'])
        userToken = auth_pyrebase.get_account_info(user['idToken'])
        userId = userToken['users'][0]['localId']
        account = db.collection('accounts').document(userId).get()
        token = jwt.encode(
            {
                'uid': userId, 
                'userName': account.get('name'), 
                'email': json_data['email'],
                'isRefreshToken': False,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },secret_key)
        refreshToken = jwt.encode(
            {
                'uid': userId, 
                'userName': account.get('name'), 
                'email': json_data['email'],
                'isRefreshToken': True,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=40)
            },secret_key)
        return jsonify(
            {
                'user': 
                    {
                        'uid': userId, 
                        'userName': account.get('name'), 
                        'email': json_data['email']
                    }, 
                'token': token,
                'refreshToken': refreshToken
            })
    except Exception as e:
        response = jsonify({'erro': 'Usuário ou senha incorretos' + str(e)})
        return response, 401
