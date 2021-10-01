# To run flask
# $ export FLASK_APP=main.py
# $ export FLASK_ENV=development
# $ flask run

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')
def hello_world():
    return 'Hello, World!'

# @app.route('/users')
# def get_users():
#     return users

# @app.route('/users')
# def get_users():
#    search_username = request.args.get('name') #accessing the value of parameter 'name'
#    if search_username :
#       subdict = {'users_list' : []}
#       for user in users['users_list']:
#          if user['name'] == search_username:
#             subdict['users_list'].append(user)
#       return subdict
#    return users

@app.route('/users', methods=['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      #print(search_username,search_job)
      if search_username and search_job:
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username or user['job'] == search_job:
               subdict['users_list'].append(user)
         return subdict
      elif search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd['id'] = uuid.uuid4()
      users['users_list'].append(userToAdd)
      print(users)
      resp = jsonify(userToAdd)
      resp.status_code = 201
      #resp.status_code = 200 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp

@app.route('/users/<id>', methods=['DELETE'])
def get_user(id):
   if request.method == 'DELETE':
      if id :
         for user in users['users_list']:
            if user['id'] == id:
               users['users_list'].remove(user)
               #return users
               resp = jsonify(success=True)
               #resp.status_code = 200 #optionally, you can always set a response code. 
               # 200 is the default code for a normal response
               return resp
   elif request.method == 'GET':
      if id :
         for user in users['users_list']:
            if user['id'] == id:
               return user
            return ({})
   return users