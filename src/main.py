"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

todos = [
    { "text": "My first task", "done": False }
]

# generate_sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    # return "Hola!"


@app.route('/todos', methods=['GET'])
def get_task():
    json_text = jsonify(todos)
    return json_text

@app.route('/todos', methods=['POST'])
def create_task():
    # request_body = request.data que significa?
# We already used request.json for that, since we know that the request will be in format application/json. If that is not known, you may want to use request.get_json(force=True) to ignore the content type and treat it like json.
    body = request.get_json()
    print(body)
    task = Task(text=body["text"], done= False )
    return 'Response for the POST todo'

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
