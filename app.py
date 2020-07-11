from flask import Flask , request,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_restplus import Api, fields , Resource  #pip install flask-restplus
from werkzeug.utils import cached_property #pip install Werkzeug==0.16.1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user_details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
app.config['SECRET_KEY']=True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)


#Table
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password')


model = api.model('demo',{
    'name':fields.String('Enter Name'),
    'email':fields.String('Enter Email'),
    'password':fields.String('Enter Password')
})

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api.route('/user')
class UserDetails(Resource):
    def get(self):
        #get users from the database
        users = User.query.all()
        #return the list of users
        return jsonify(users_schema.dump(users)) 

    @api.expect(model)
    def post(self):
        #Instantiate new user
        new_user = User(name=request.json['name'], email=request.json['email'], password=request.json['password'])
        #add new user
        db.session.add(new_user)
        #commit the change to reflect in database
        db.session.commit()
        #return the response
        return user_schema.jsonify(new_user)

@api.route('/user/<int:id>')
class UserPutDelete(Resource):
    @api.expect(model)
    def put(self,id):
        #get User
        user = User.query.get(id)
        #update user data
        user.name = request.json['name']
        user.email = request.json['email']
        user.password = request.json['password']
        #commit to change in database
        db.session.commit()
        return {'message':'data updated'}

    def delete(self,id):
        #get user
        user = User.query.get(id)
        #delete the user
        db.session.delete(user)
        #commit to reflect in database
        db.session.commit()
        return {'message':'data deleted successfully'}

# Run Server
if __name__ == '__main__':
    app.run(debug=True)