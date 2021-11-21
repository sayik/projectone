#!/usr/bin/python3
import threading, time, random
from flask import Flask, Response
from flask_restful import Api, Resource
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
counter = 0

cors = CORS(app)


class increment(Resource):
    def put(self):
        global counter
        time.sleep(2)
        counter += 1

        return {"counter": counter}


class read(Resource, threading.Thread):
    def get(self):
        # time.sleep(random.randint(10,40))
        return {"counter": counter}


api.add_resource(read, "/counter/read")
api.add_resource(increment, "/counter/increment")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
