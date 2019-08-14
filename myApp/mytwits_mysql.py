from flask import Flask, request
from flask import render_template
from flask import redirect, url_for, send_from_directory, send_file
from flask import session, flash, abort
from flask import request
from flask import jsonify
from vs_url_for import vs_url_for
from dbhelper import DBHelper
from forms import addTwitForm, editTwitForm, loginForm, RegistrationForm, UploadForm, editImageForm
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from flask_login import current_user
from user import User
import hashlib
import sqlite3
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from base64 import b64encode
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from models import db,Users,Twits, Images
from passwordhelper import PasswordHelper
from werkzeug.utils import secure_filename

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mytwits_user:mytwits_password@localhost/mytwits'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#initialise flask-login
login_manager.init_app(app)
login_manager.login_message = u"You need to log in to access this page"

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
    'created_at': fields.DateTime(dt_format='rfc822'),

    'image_id': fields.Integer,
    'image': fields.String,
    'name': fields.String,
    'created_at': fields.DateTime(dt_format='rfc822')
}

#---parse and verify the api inputs
parser = reqparse.RequestParser()
parser.add_argument('twit', type=str, help='the text of the twit; must be a string')
parser.add_argument('twit_id', type=int, help='the id of the twit; must be an integer')
parser.add_argument('user_id', type=int, help='the id of the twit; must be an integer')

parser2 = reqparse.RequestParser()
parser2.add_argument('image', type=str, help='the src of the image; must be a url')
parser2.add_argument('image_id', type=int, help='the id of the image; must be an integer')
parser2.add_argument('user_id', type=int, help='the id of the image; must be an integer')
parser2.add_argument('name', type=str, help='the name of the image; must be a String')
parser2.add_argument('description', type=str, help='the description of the image; must be a String')


#---- flask-restful api for twits
class TwitsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return  Twits.query.order_by(Twits.created_at.desc()).all()

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        twit = args['twit']
        user_id = args['user_id']
        new_twit =Twits(user_id=user_id, twit=twit)
        db.session.commit()
        return  Twits.query.order_by(Twits.created_ac.desc()).all()

class TwitsIdApi(Resource):

    @marshal_with(resource_fields)
    def get(self, twit_id):
        return Twits.query.filter_by(twit_id=twit_id).first()

    @marshal_with(resource_fields)
    def put(self,twit_id):
        args = parser.parse_args()
        twit = args['twit']
        twt = Twits.query.filter_by(twit_id=twit_id).first()
        twt.twit = twit
        db.session.commit()
        return  Twits.query.filter_by(twit_id=twit_id).first()

    @marshal_with(resource_fields)
    def delete(self, twit_id):
        twt = Twits.query.filter_by(twit_id=twit_id).first()
        db.delete(twt)
        db.session.commit()
        return  Twits.query.order_by(Twits.created_at.desc()).all()

#------Api for images

class ImagesApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Images.query.order_by(Images.created_at.desc()).all()

    @marshal_with(resource_fields)
    def post(self):
        args= parser2.parse_args()
        name = args['name']
        user_id = args['user_id']
        image = args['image']
        new_image = Images.query.filter_by(image_id=image_id).first()        
        new_image.name = name
        new_image.description = description
        new_image.user_id = user_id
        new_image.image = image
        new_image.username = Users.query.filter_by(user_id=user_id).first().username
        db.session.commit()
        return Images.query.order_by(Images.created_at.desc()).all()
   
class ImagesIdApi(Resource):
    @marshal_with(resource_fields)
    def get(self, image_id):
         return Images.query.order_by(Images.created_at.desc()).all()
    
    @marshal_with(resource_fields)
    def put(self,image_id):
        args = parser.parse_args()
        image = args['image']
        name = args['name']
        description = args['description']
        img = Images.query.order_by(image_id=image_id).first()
        img.name = name
        img.description = description
        img.image = image    
        db.session.commit()
        return Images.query.filter_by(image_id=image_id).first()
   
    @marshal_with(resource_fields)
    def delete(self, image_id):
        result = Images.query.filter_by(image_id=image_id).first()
        db.delete(result)
        db.session.commit()
        return Images.query.order_by(Images.created_at.desc()).all()

#--- assigning a route for the api
api.add_resource(TwitsApi,'/api')
api.add_resource(TwitsIdApi,'/api/<int:twit_id>')
api.add_resource(ImagesApi,'/image_api')
api.add_resource(ImagesIdApi,'/image_api/<int:image_id>')



#--- the callback function for flask-login
@login_manager.user_loader
def load_user(user_id):
     return Users.query.get(int(user_id))

@app.route('/')
def index():
    twits = Twits.query.order_by(Twits.created_at.desc()).all()
    return render_template("mytwits_mysql.html", twits=twits)

@app.route('/<username>')
def timeline(username):
    twits = Twits.query.filter_by(username=username).first().twits
    return render_template('timeline.html',twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
@login_required
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        user_id = current_user.user_id
        new_twit = Twits(twit=twit, user_id=user_id)
        db.session.add(new_twit)
        db.session.commit()
        return redirect(vs_url_for('index'))
    return render_template('add_twit_mysql.html',form=form)

@app.route('/edit_twit', methods = ['GET', 'POST'])
@login_required
def edit_twit():
    user_id = current_user.user_id 
    form = editTwitForm()
    if request.args.get('id'):
          twit_id = request.args.get('id')
          twit = Twits.query.filter_by(twit_id = twit_id).first() 
          form.twit.data = twit.twit
          form.twit_id.data = twit_id
          print(form.twit.data)
          print(form.twit_id.data)
          return render_template('edit_twit_mysql.html',form=form)
    if form.validate_on_submit():  
          twit_id = form.twit_id.data
          # load the twit
          twit = Twits.query.filter_by(twit_id = twit_id).first()
          usr = twit.user_id
          if(user_id != usr):
              abort(401)
          else:
              #twit = Twits.query.filter_by(twit_id = twit_id).first()
              # change the twit text to the text submitted in the form
              twit.twit = form.twit.data
              print(twit.twit)
              db.session.commit()
              return redirect(vs_url_for('index'))
    return render_template('edit_twit_mysql.html',form=form)

@app.route('/delete_twit', methods = ['GET', 'POST'])
@login_required
def delete_twit():
    user_id = current_user.user_id
    twit_id = request.args.get('id')
    usr = Twits.query.filter_by(twit_id=twit_id).first().user_id
    if (user_id != usr):
         abort(401)
    else:
        if request.args.get('id'):
            twit_for_deletion = Twits.query.filter_by(twit_id = twit_id).first()
            db.session.delete(twit_for_deletion)
            db.session.commit()
    return redirect(vs_url_for('index'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        user = Users.query.filter_by(username=username).first()
        if ph.validate_password(password,user.salt,user.hashed):
            login_user(user)
            return redirect(vs_url_for('index'))
        else:
            flash('Login failed. Please try again')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(vs_url_for('index'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = Users(hashed=None, salt=None, username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        user = Users.query.filter_by(username=username).first()
        salt= ph.get_salt().decode()
        hashed = hashlib.sha512(str(salt+user.password).encode('utf-8')).hexdigest()
        user.salt = salt
        user.hashed = hashed
        db.session.commit()
        flash('Thanks for registering')
        return redirect(vs_url_for('login'))
    return render_template('register.html', form=form)

#----CRUD for images

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    images = Images.query.order_by(Images.created_at.desc()).all()
    return render_template("gallery.html", images=images)

#---Create image 
@app.route("/w")
@login_required
def w():
    return render_template("upload.html")

# phase for letting user upload image
@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
     #---make static file if not exists
     target = os.path.join(APP_ROOT, 'static/')
     print(target)
     if not os.path.isdir(target):
            os.mkdir(target)
     else:
        print("Couldn't create upload directory {}".format(target))
    
     #---get image
     print(request.files.getlist("file"))
     for upload in request.files.getlist("file"):
         print(upload)
         print("{} is the filename".format(upload.filename))
         name = upload.filename
         destination = "/".join([target, name])
         print("Accept incoming file:", name)
         print("Save it to:",destination)
         upload.save(destination)

     #---and store..
         user_id = current_user.user_id 
         name = upload.filename
         username = Users.query.filter_by(user_id=user_id).first().username         
         image = str('www.doc.gold.uk/usr/340/static/'+str(name))
         new_image = Images(user_id=user_id, username=username, image = image, name=name)
         db.session.add(new_image)
         db.session.commit()
         
         #result = Images.query.filter_by(name=name).first()
         return redirect(vs_url_for('add_image'))
     return render_template('complete.html',name=name)

@app.route('/add_image',methods=['GET','POST'])
@login_required
def add_image():
     form = UploadForm()
     if form.validate_on_submit():
        user_id = current_user.user_id
        result = Images.query.order_by(Images.image_id.desc()).first()
        result.description = form.description.data
        db.session.commit()
        return redirect(vs_url_for('gallery'))
     return render_template('add_image.html',form=form)

#---edit image
@app.route('/edit_image', methods=['GET','POST'])
@login_required
def edit_image():
     form = editImageForm() 
     user_id = current_user.user_id
     if request.args.get('id'):
          image_id = request.args.get('id')
          image = Images.query.filter_by(image_id = image_id).first()
          form.description.data = image.description
          form.image_id.data = image_id 
          print(form.description.data)
          print(form.image_id.data)
          return render_template('edit_image.html', form=form) 
     if form.validate_on_submit():
          image_id = form.image_id.data
          new_description = form.description.data
          #load the image
          result = Images.query.order_by(Images.image_id.desc()).first()
          image = Images.query.filter_by(image_id = image_id).first()
          usr = result.user_id
          if(user_id != usr):
              abort(401)
          else:
              #change the description & image data
              image.description = form.description.data
              image.image = result.image
              image.name = result.name
              db.session.commit()
              #delete the latest image cause we aim to replace image
              if (image != result):
                  db.session.delete(result)
                  db.session.commit()
              return redirect(vs_url_for('gallery'))
     return render_template('edit_image.html', form=form) 
    
#---delete image
@app.route('/delete_image', methods=['GET', 'POST'])
@login_required
def delete_image():
     user_id = current_user.user_id
     image_id = request.args.get('id')
     usr = Images.query.filter_by(image_id=image_id).first().user_id
     if (user_id != usr):
         abort(401)
     else:
         if request.args.get('id'):
              image_for_deletion = Images.query.filter_by(image_id=image_id).first() 
              db.session.delete(image_for_deletion)
              db.session.commit()
     return redirect(vs_url_for('gallery'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)



