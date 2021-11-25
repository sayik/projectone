#!/usr/bin/python3
import json
import time
import string
import pyseto

from random import choice
from pyseto import Key
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from functools import wraps
from flask import abort


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'Authorization' not in request.headers:
            abort(401)

        user = None
        data = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(data), 'Bearer ', '')
        decoded = pyseto.decode(paseto_key, token, deserializer=json)
        try:
            print(decoded)
        except:
            abort(401)

        return f(*args, **kws)
    return decorated_function


def secret_token(length=32):
    return "".join(
        [choice(string.digits + string.ascii_letters) 
            for _ in range(length)]
    ).encode()


def create_paseto(key, username):
    token = pyseto.encode(
        key,
        {"username": username},
        serializer=json,
        exp=3600,
    )
    return token.decode()


app = Flask(__name__)
api = Api(app)
counter = 0

cors = CORS(app)

STORE = {
    "username": "password",
}

paseto_key = Key.new(version=4, purpose="local", key=secret_token())


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
                return {"status": "login", "token": create_paseto(paseto_key, username)}, 200
            else:
                return {"status": "login failure"}, 404
        else:
            return {"status": "login failure"}, 404




class Counter(Resource):
    decorators = [authorize]

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
