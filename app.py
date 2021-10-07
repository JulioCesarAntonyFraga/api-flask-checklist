from flask.json import jsonify
from firebase_admin import credentials, firestore, initialize_app
from functools import wraps
import pyrebase
from flask import Flask, request
import datetime
import jwt
from api_auth import *
from verificacoes import *
from api_firebase import *
from checklists import *
from planos_de_acao import *
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
#credenciais aplicação
app.config['SECRET_KEY'] = 'JDFH8HU8hf78dhn348fhpwuiyf8dfisdhy8fh34fhdfnf34h3lguihohr8efg3lhg8fbrlgb3o5blui5g975gh9elfkgi5ngby9jgepuilgh54bouigheor7ibutg5huhgevo89'

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Auto Checklist"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

##################AUTH FIREBASE E TOKEN###################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers['authorization']
        except:
            return jsonify({'erro': 'Nenhum token recebido !!'}), 401

        # return 401 if token is not passed
        if not token:
            return jsonify({'erro': 'Nenhum token recebido !!'}), 401
        
        # jwt is passed in the request header
        if 'Bearer' in request.headers['authorization']:
            token = token.replace('Bearer ', '')

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = {
                "email": data['email'],
                "uid": data['uid'],
                "userName": data['userName'],
            }
        except Exception as e:
            return jsonify({
                'erro': 'Algum erro ocorreu: ' + str(e)
            }), 401
        # returns the current logged in users contex to the routes
        return f(user, *args, **kwargs)
    return decorated


#####METODO PARA PEGAR TODAS AS VERIFICACOES############
@app.route('/pawaresoftwares/api/auth/refresh-token/', methods=['POST'])
def Route_refresh_token():
    try:
        token = str(request.args['refreshToken'])
    except:
        return jsonify({'erro': 'Nenhum token recebido !!'}), 401

    # return 401 if token is not passed
    if not token:
        return jsonify({'erro': 'Nenhum token recebido !!'}), 401
    
    # jwt is passed in the request header
    if 'Bearer' in token:
        token = token.replace('Bearer ', '')

    try:
        # decoding the payload to fetch the stored details
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])  

    except Exception as e:
        return jsonify({
            'erro': 'Algum erro ocorreu: ' + str(e)
        }), 401

    if data['isRefreshToken'] != True:
        return jsonify({
            'erro': 'Algum erro ocorreu: Este não é um refresh token.'
        }), 401  

    user = {
        "uid": data['uid'],
        "email": data['email'],
        "userName": data['userName'],
    }

    newToken = jwt.encode(
            {
                'uid': user['uid'], 
                'userName': user['userName'], 
                'email': user['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },secret_key)

    newRefreshToken = jwt.encode(
        {
            'uid': user['uid'], 
            'userName': user['userName'], 
            'email': user['email'],
            'isRefreshToken': True,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=40)
        },secret_key)
        
    return jsonify(
        {
            'user': 
                {
                    'uid': user['uid'], 
                    'userName': user['userName'], 
                    'email': user['email'],
                }, 
            'token': newToken,
            'refreshToken': newRefreshToken
        })

#####METODO PARA PEGAR TODAS AS VERIFICACOES############
@app.route('/pawaresoftwares/api/verificacoes/obter-todos/', methods=['GET'])
@token_required
def Route_get_all_verificacoes(user):
    return get_all_verificacoes(user)

####METODO PARA PEGAR UMA VERIFICACAO############
@app.route('/pawaresoftwares/api/verificacoes/obter-por-id/', methods=['GET'])
@token_required
def Route_get_verificacao(user):
   return get_verificacao(user)

####METODO PARA PEGAR TODAS AS CHECKLISTS############
@app.route('/pawaresoftwares/api/checklists/obter-todos/', methods=['GET'])
@token_required
def Route_get_all_checklists(user):
    return get_all_checklists(user)

####METODO PARA PEGAR UMA CHECKLIST############
@app.route('/pawaresoftwares/api/checklists/obter-por-id/', methods=['GET'])
@token_required
def Route_get_checklist(user):
    return get_checklist(user)

####METODO PARA PEGAR TODOS OS PLANOS DE AÇÃO############
@app.route('/pawaresoftwares/api/planos-de-acao/obter-todos/', methods=['GET'])
@token_required
def Route_get_all_planos_de_acao(user):
    return get_all_plano_de_acao(user)

####METODO PARA PEGAR UM PLANO DE AÇÃO############
@app.route('/pawaresoftwares/api/planos-de-acao/obter-por-id/', methods=['GET'])
@token_required
def Route_get_plano_de_acao(user):
    return get_plano_de_acao(user)

####METODO PARA LOGAR UM USUARIO DO FIREBASE############
@app.route('/pawaresoftwares/api/auth/login/',  methods=['POST'])
def Route_Login():
    return Login()


if __name__ == '__main__':
    # app.config['ENV'] = 'development'
    app.config['DEBUG'] = False
    app.run(debug=False)
