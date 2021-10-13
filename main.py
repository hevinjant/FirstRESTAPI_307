# To run flask
# $ export FLASK_APP=main.py
# $ export FLASK_ENV=development
# $ flask run

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import uuid

from model_mongodb import Model, User

app = Flask(__name__)
CORS(app)

users = {
   'users_list': []
}

# users = {
#    'users_list' :
#    [
#       {
#          'id' : 'xyz789',
#          'name' : 'Charlie',
#          'job': 'Janitor',
#       },
#       {
#          'id' : 'abc123',
#          'name': 'Mac',
#          'job': 'Bouncer',
#       },
#       {
#          'id' : 'ppp222',
#          'name': 'Mac',
#          'job': 'Professor',
#       },
#       {
#          'id' : 'yat999',
#          'name': 'Dee',
#          'job': 'Aspring actress',
#       },
#       {
#          'id' : 'zap555',
#          'name': 'Dennis',
#          'job': 'Bartender',
#       }
#    ]
# }

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username and search_job:
         users = User().find_by_name_job(search_username, search_job)
      elif search_username :
         users = User().find_by_name(search_username)
      elif search_job:
         users = User().find_by_job(search_job)
      else:
         users = User().find_all()
      print(users)
      return {'users_list': users}
   elif request.method == 'POST':
      userToAdd = request.get_json()
      # userToAdd['id'] = str(uuid.uuid4())
      # users['users_list'].append(userToAdd)
      new_user = User(userToAdd)
      new_user.save()
      resp = jsonify(new_user)
      resp.status_code = 201
      #resp.status_code = 200 #optionally, you can always set a response code.
      # 200 is the default code for a normal response
      return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
   if request.method == 'DELETE':
      userToDelete = User({"_id":id})
      status = userToDelete.remove()
      if status:
         resp = jsonify(success=True)
         resp.status_code = 204
         #resp.status_code = 200 #optionally, you can always set a response code.
         # 200 is the default code for a normal response
         return resp
      else:
         resp = jsonify(success=False)
         resp.status_code = 404
         return resp
   elif request.method == 'GET':
      user = User({"_id":id})
      if user.reload():
         return user
      else:
         return jsonify({"error":"User not found"}), 404
   return users
