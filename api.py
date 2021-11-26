#!/usr/bin/python3
import json
import time
import string
import pyseto

from random import choice
from pyseto import Key, Paseto
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from functools import wraps
from flask import abort

from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required,
                                get_jwt_identity, verify_jwt_in_request, get_jwt)


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' not in request.headers:
            abort(401)

        try:
            result = verify_jwt_in_request()
            claims = get_jwt()
            print(result, claims)
            user = claims["sub"]
            print(user)
        except Exception as e:
            print(e)
            abort(401)

        return f(*args, **kws)
    return decorated_function


app = Flask(__name__)

api = Api(app)

jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 360
app.config['JWT_SECRET_KEY'] = "A" * 128

cors = CORS(app)


counter = 0
STORE = {
    "username": "password",
}



parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'username', 
    type=str, 
    help='username is required', 
    required=True,)

parser.add_argument(
    'password', 
    type=str, 
    help='password is required', 
    required=True,)


class Login(Resource):
    def put(self):
        request.get_json(force=True)
        args = parser.parse_args()
        username = args["username"]
        password = args["password"]

        if username in STORE.keys():
            if password == STORE[username]:

                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                return {
                    'status': f'Logged in as {username}',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            else:
                return {"status": "login failure"}, 401
        else:
            return {"status": "login failure"}, 401


class Counter(Resource):

    @authorize
    def put(self):
        global counter
        time.sleep(2)
        counter += 1
        return {"counter": counter}

    def get(self):
        return {"counter": counter}


api.add_resource(Counter, "/counter")
api.add_resource(Login, "/login")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
