from flask import Flask
from flask import request
from flask import make_response
import json
import yaml

from shapeways.client import Client

client = Client(
    consumer_key="0d6f512bc947f1aaa02786d849bccd09c1129340",
    consumer_secret="c10ed411b904bc5969b8535317ed93dcce20a7ad",
    callback_url="http://thawing-savannah-5714.herokuapp.com/oauth-callback"
)


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/service-request', methods=['GET'])
def get_service():
    if not request.args['s']:
        return make_response('')

    wts = get_weights(request.args['s'])
    r = make_response(wts)
    return r

@app.route('/addmodel', methods=['GET'])
def add_model():
    modelId = 42
    params = {
        "file": "test",
        "fileName": "test.stl",
        "hasRightsToModel": True,
        "acceptTermsAndConditions": True,
    }

    client.connect()

    r = client.add_model_file(modelId, params)
    print r

    #return make_response(r)
    return make_response(json.JSONEncoder().encode([]))

@app.route('/oauth-callback', methods=['GET'])
def oauth_cb():
    return make_response(json.JSONEncoder().encode(["calledback"])

# if __name__ == '__main__':
#     app.run()