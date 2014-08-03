import os
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
app.secret_key = 'why would I tell you my secret key!?'

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

  return make_response(json.JSONEncoder().encode([client.oauth_token,
                                                  client.oauth_secret]))


@app.route('/ocb', methods=['GET'])
def ocb():

    client = Client(
        consumer_key="0d6f512bc947f1aaa02786d849bccd09c1129340",
        consumer_secret="c10ed411b904bc5969b8535317ed93dcce20a7ad",
        #callback_url="oob"
        callback_url="http://thawing-savannah-5714.herokuapp.com/ocb",
        oauth_token=request.args.get("oauth_token"),
        oauth_secret=request.args.get("oauth_token_secret")
    )

    print "done verifying"
    info = client.get_materials()
    print "Materials = ", info
    fileData = "This data should be read from the request object"

    modelId = 42
    params = {
        "file": fileData,
        "fileName": "bottle.stl",
        "hasRightsToModel": True,
        "acceptTermsAndConditions": True,
    }

    info = client.add_model(params)
    #return make_response()
    return make_response(json.JSONEncoder().encode(info))


# @app.route("/addmodel", methods=['GET'])
# def addmodel():
#     if 'oauth_verifier' not in session:
#         print 'Calling auth'
#         auth()
#         return make_response(json.JSONEncoder().encode([]))

#     client.verify(session['oauth_token'], session['oauth_verifier'])
#     modelId = 42
#     params = {
#         "file": "test",
#         "fileName": "test.stl",
#         "hasRightsToModel": True,
#         "acceptTermsAndConditions": True,
#     }

#     print "done verifying"
#     info = client.get_materials()
#     print "Info = ", info
#     #return make_response()
#     return make_response(json.JSONEncoder().encode(info))

if __name__ == '__main__':
    app.run()
