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
    callback_url="oob"
    #callback_url="http://thawing-savannah-5714.herokuapp.com/ocb"
)


app = Flask(__name__)
app.debug = True

oauth_token='f5ae6c8dd25d67a983b3aa87686a30cbaeb94326'
oauth_verifier='b35006'

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
    print r
    return redirect(r)
    #return redirect('http://localhost:5000/?oauth_token=393ddd84b2b38d7e367a76a648633b47d45e091d&oauth_verifier=15daba

    #return make_response(r)
    #return make_response(json.JSONEncoder().encode([]))

@app.route('/ocb', methods=['GET'])
def ocb():
    #print request.args
    #print request.args.get('oauth_token'), request.args.get('oauth_verifier')
    client.verify(request.args.get('oauth_token'), request.args.get('oauth_verifier'))
    # oauth_token='a1fb6f511c6a2186eb466b3699e12b5a1b715494'
    # oauth_verifier='d6e30d'
    # print oauth_token , oauth_verifier
    # client.verify(oauth_token, oauth_verifier)

    print "done verifying"
    info = client.get_materials()
    print "Info = ", info
    #return make_response()
    return make_response(json.JSONEncoder().encode(info))

# if __name__ == '__main__':
#     app.run()
