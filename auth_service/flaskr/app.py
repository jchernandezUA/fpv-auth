from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from modelos import db, Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@db:5432'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()


class VistaLogIn(Resource):
    def post(self):
        username = request.json["username"]
        password = request.json["password"]
        
        user = Usuario.query.filter_by(username=username, password = password).all()
        if user:
            token_de_acceso = create_access_token(identity=request.json['username'])
            return {'message':'Usuario creado exitosamente', 'token_de_acceso': token_de_acceso}
        else:
            return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn(Resource):
    
    def post(self):
        username = request.json["username"]
        password =request.json["password1"]
        password_confirm =request.json["password2"]

        if password != password_confirm:
            return {'message': 'Bad request'}, 400
        
        new_user = Usuario(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message':'Usuario creado exitosamente'}

cors=CORS(app)

api = Api(app)
jwt = JWTManager(app)

api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
    
    