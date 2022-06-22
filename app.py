from flask import Flask
from flask_jwt_extended import JWTManager 
from flask_restful import Api
from config import Config
from resources.user import UserRegisterResourse 
from resources.user import UseLoginResource , UserLogoutResource ,jwt_blacklist
from resources.memo import MemoListResource
from resources.memo_info import MemoResource
from resources.memo_publish import MemoPublishResource
from resources.follow import FollowResource ,FollowListResource

app  = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

# 로그아웃 된 토큰이 들어있는 set을, jwt 에 알려준다.
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api  = Api(app)

# 경로와 리소스를 연결 
api.add_resource(UserRegisterResourse,'/users/register')
api.add_resource(UseLoginResource,'/users/login')
api.add_resource(UserLogoutResource,'/users/logout')
api.add_resource(MemoResource,'/memos/<int:memo_id>')
api.add_resource(MemoListResource,'/memos')
api.add_resource(MemoPublishResource, '/memos/<int:memo_id>/publish')
api.add_resource(FollowResource, '/follow/<int:follow_id>')
api.add_resource(FollowListResource, '/follow')

if __name__ == '__main__':
    app.run()