from flask import Flask
from twits_blueprint import twits_blueprint
from images_blueprint import images_blueprint
from register_blueprint import register_blueprint
from login_blueprint import login_blueprint
from flask_login import current_user
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from models import db,Users,Twits, Images
from passwordhelper import PasswordHelper
from user import User
from dbhelper import db
from dbhelper import DBHelper

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mytwits_user:mytwits_password@localhost/mytwits'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(twits_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(images_blueprint)
app.register_blueprint(register_blueprint)

api = Api(app)

#initialise the sqlalchemy database connection
db.init_app(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# instantiate a password helper object
ph = PasswordHelper()

#---resource fields to filter the output for flask-restful
resource_fields = {
    'twit_id': fields.Integer,
    'twit':fields.String,
    'user_id': fields.Integer,
    'created_at': fields.DateTime(dt_format='rfc822')
}

#---parse and verify the api inputs
parser = reqparse.RequestParser()
parser.add_argument('twit', type=str, help='the text of the twit; must be a string')
parser.add_argument('twit_id', type=int, help='the id of the twit; must be an integer')
parser.add_argument('user_id', type=int, help='the id of the twit; must be an integer')

#---instantiating the resource; the main part of the flask-restful api
class TwitsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return  db.get_all_twits()

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        twit = args['twit']
        user_id = args['user_id']
        db.add_twit(twit,user_id)
        return  db.get_all_twits()

class TwitsIdApi(Resource):

    @marshal_with(resource_fields)
    def get(self, twit_id):
        if  db.get_twit(twit_id):
            return db.get_twit(twit_id)
        abort(404)

    @marshal_with(resource_fields)
    def put(self,twit_id):
        args = parser.parse_args()
        twit = args['twit']
        db.update_twit(twit,twit_id)
        return  db.get_all_twits()

    @marshal_with(resource_fields)
    def delete(self, twit_id):
        db.delete_twit(twit_id)
        return  db.get_all_twits()

#--- assigning a route for the api
api.add_resource(TwitsApi,'/api')
api.add_resource(TwitsIdApi,'/api/<int:twit_id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)

