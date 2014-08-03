import os
from flask import Flask
from flask import request
from flask import make_response
import json
import yaml
from flask import redirect, url_for

from shapeways.client import Client

client = Client(
    consumer_key="0d6f512bc947f1aaa02786d849bccd09c1129340",
    consumer_secret="c10ed411b904bc5969b8535317ed93dcce20a7ad",
    callback_url="http://thawing-savannah-5714.herokuapp.com/ocb"
)


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/addmodel', methods=['GET'])
def add_model():
    modelId = 42
    params = {
        "file": "test",
        "fileName": "test.stl",
        "hasRightsToModel": True,
        "acceptTermsAndConditions": True,
    }

    r = client.connect()

    #r = client.add_model_file(modelId, params)
    #print r
    return redirect(r)
    #return redirect('http://localhost:5000/?oauth_token=393ddd84b2b38d7e367a76a648633b47d45e091d&oauth_verifier=15daba

    #return make_response(r)
    #return make_response(json.JSONEncoder().encode([]))

@app.route('/ocb', methods=['GET'])
def ocb():
    client.verify(request.args)
    info = client.get_api_info()
    return make_response(info)
    #return make_response(json.JSONEncoder().encode(["calledback"]))

# if __name__ == '__main__':
#     app.run()
