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


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate_sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    # return "Hola!"

# Obtener todas las tareas
@app.route('/task', methods=['GET'])
def get_task():

    tasks = Task.query.all()
    all_tasks = list(map(lambda task: task.serialize(), tasks))
    return jsonify(all_tasks), 201

# Crear una Tarea
@app.route('/task', methods=['POST'])
def create_task():
   
    body = request.get_json()
    task = Task(text=body["text"], done= False, user_id=body["user_id"])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.serialize()),201

# Actualizar una Tarea
@app.route('/task/<int:task_id>', methods=['PUT'])
def refresh_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        raise APIException("Tarea no encontrada", 404)
    body = request.get_json()
    if not ("done" in body):
        raise APIException("keyError: done", 404)
    task.done = body["done"]
    db.session.commit()
    return jsonify(task.serialize())

# Obtener una única Tarea
@app.route('/task/<int:task_id>', methods=['GET'])
def get_refresh_task(task_id):

    task = Task.query.get(task_id)
    if task is None:
        raise APIException("Tarea no encontrada", 404)
    return jsonify(task.serialize())

# Borrar Tarea
@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        raise APIException("Tarea no encontrada", 404)
    db.session.delete(task)
    db.session.commit()
    return jsonify(task.serialize())

# Obtener todos los usuarios
@app.route('/user', methods=['GET'])
def get_all_users():
    
    users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), users))
    return jsonify(all_users), 200

# Obtener un único usuario
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.get(user_id)
    if user is None:
        raise APIException("Usuario no encontrado", 404)
    return jsonify(user.serialize()), 200

# Crear usuario
@app.route('/user/register', methods=['POST'])
def create_user():
   
    body = request.get_json()
    print(body)
    user = User(email=body["email"], is_active=True, password=body["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify("Usuario añadido")

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
