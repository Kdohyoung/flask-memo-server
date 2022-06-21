from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from recoources.user import UserRegisterResourse


app  = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)
api  = Api(app)

# 경로와 리소스를 연결 
api.add_resource(UserRegisterResourse,'/users/register')




if __name__ == '__main__':
    app.run()