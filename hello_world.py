#Import required packages
from flask import Flask
from flask_restful import Resource, Api

# Initialize app
app = Flask(__name__)
api = Api(app)

#Create a Hello-World Class to handle requests
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello World'}

api.add_resource(HelloWorld, '/','/hello-world')

# Run Server
if __name__ == '__main__':
    app.run(debug=True)