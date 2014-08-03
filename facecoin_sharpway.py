import os
import base64
from flask import Flask
from flask import request
from flask import make_response
import json
import yaml
from flask import redirect, url_for, session

from shapeways.client import Client

client = Client(
    consumer_key="0d6f512bc947f1aaa02786d849bccd09c1129340",
    consumer_secret="c10ed411b904bc5969b8535317ed93dcce20a7ad",
    #callback_url="oob"
    callback_url="http://thawing-savannah-5714.herokuapp.com/signin"
)

app = Flask(__name__)
app.debug = True
app.secret_key = 'why would I tell you my secret key!'

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/auth', methods=['GET'])
def auth():
    print 'In auth....'
    r = client.connect()
    print r
    return redirect(r)

@app.route('/signin')
def signin():
  client.verify(request.args.get('oauth_token'),
                      request.args.get('oauth_verifier'))
  session['oauth_token'] = client.oauth_token
  session['oauth_token_secret'] = client.oauth_secret

  print "Session variables:signin", session

  return make_response(json.JSONEncoder().encode([client.oauth_token,
                                                  client.oauth_secret]))

@app.route('/addmodel', methods=['GET'])
def addmodel():

    client = setUpOAuthClient()
    fileData = getFileData()
    #fileData = "This works?"
    #fileData = base64.b64encode(fileData)

    params = {
        "file": fileData,
        "fileName": "bottlev1.stl",
        "hasRightsToModel": True,
        "acceptTermsAndConditions": True,
    }

    info = client.add_model(params)

    #return make_response()
    return make_response(json.JSONEncoder().encode(info))

def getFileData():
    data = []
    with open('bottle.stl') as f:
        for l in f:
            data.append(l)

    return base64.b64encode("".join(data))

def setUpOAuthClient():
    # if "oauth_token_secret" not in session:
    #     oauth_token = 'cc04e87c44d2ecc92a66633621e94251595eb8d9'
    #     oauth_secret_token = '2e68adf666e130a94573cce038b2c2d9bf6f0abc'
    # else:
    print "Session variables", session
    oauth_token = session['oauth_token']
    oauth_secret_token = session['oauth_token_secret']
        # oauth_token=request.args.get("oauth_token"),
        # oauth_secret_token=request.args.get("oauth_token_secret")

    client = Client(
        consumer_key="0d6f512bc947f1aaa02786d849bccd09c1129340",
        consumer_secret="c10ed411b904bc5969b8535317ed93dcce20a7ad",
        #callback_url="oob"
        callback_url="http://thawing-savannah-5714.herokuapp.com/ocb",
        oauth_token=oauth_token,
        oauth_secret=oauth_secret_token
    )

    return client

@app.route('/addtocart', methods=['GET'])
def add_to_cart():

    client = setUpOAuthClient()
    modelId = request.args.get("modelId")

    params = { "modelId" : modelId }
    info = client.add_to_cart(params)
    #return make_response()
    return make_response(json.JSONEncoder().encode(info))

@app.route("/showcart", methods=['GET'])
def showcart():
    client = setUpOAuthClient()
    modelId = request.args.get("modelId")

    return redirect('https://www.shapeways.com/cart/')

if __name__ == '__main__':
    app.run()
