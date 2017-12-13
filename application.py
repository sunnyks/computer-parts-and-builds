from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Part
#from database_setup import Motherboard, CPU, CPU_Cooler, Memory, Storage, GPU, PowerSupply, SoundCard, Wishlist, Build

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)



# CLIENT JSON
CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']


engine = create_engine('sqlite:///computerpartsandbuilds.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(64))
    login_session['state'] = state
    return render_template('login.html', STATE = state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    # get authorization code
    code = request.data
    try:
        # Upgrade authorization code into credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-type'] = 'application/json'
        return response

    # Check that access token in credentials object is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + str(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # abort in case of error in accessing of token info
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-type'] = 'application/json'
        return response
    # verify that the access token is used for intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("token's user ID doesn't match given user ID."), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    # verify that access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-type'] = 'application/json'
        return response
    # check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    #login_session['provider'] = 'google'
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "http://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token' : credentials.access_token, 'alt' : 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = '<h1>hey sup</h1>'
    return output


def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None



@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    print 'in gdisconnect access token is' + str(access_token)
    print 'username is: '
    print login_session['username']
    url = 'https://www.accounts.google.com/o/oauth2/revoke?token=' + str(login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token'), 400)
        response.headers['Content-type'] = 'application/json'
        return response


@app.route('/')
@app.route('/home/')
def showHome():
    # list types of pc part
    types = session.query(Part.type.distinct().label("type"))
    distinct_types = [row.type for row in types.all()]
    return render_template('home.html', types = distinct_types)




@app.route('/part/')
def showAllParts():
    parts = session.query(Part).all()
    if 'username' in login_session:
        return render_template('allparts.html', parts = parts)
    else:
        return render_template('publicallparts.html', parts = parts)



@app.route('/part/<int:part_id>/')
def showPart(part_id):
    part = session.query(Part).filter_by(id = part_id).one()
    if 'username' in login_session:
        return render_template('partinfo.html', part = part)
    else:
        return render_template('publicpartinfo.html', part = part)



@app.route('/part/new/', methods = ['GET', 'POST'])
def newPart():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newPart = Part(type = request.form['type'], name = request.form['name'], price = request.form['price'], manufacturer = request.form['manufacturer'], model_number = request.form['model_number'])
        session.add(newPart)
        session.commit()
        flash('New item' + newPart.name + 'successfully added')
        return redirect(url_for('showPart', part_id = newPart.id))
    else:
        return render_template('newPart.html')




@app.route('/part/<int:part_id>/edit', methods = ['GET', 'POST'])
def editPart(part_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedPart = session.query(Part).filter_by(id = part_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedPart.name = request.form['name']
        if request.form['type']:
            editedPart.type = request.form['type']
        if request.form['price']:
            editedPart.price = request.form['price']
        if request.form['manufacturer']:
            editedPart.manufacturer = request.form['manufacturer']
        if request.form['model_number']:
            editedPart.model_number = request.form['model_number']
        session.add(editedPart)
        session.commit()
        flash('Part successfully edited')
        return redirect(url_for('showPart', part_id = editedPart.id))
    else:
        return render_template('editpart.html', part = editedPart)




@app.route('/part/<int:part_id>/delete', methods = ['GET', 'POST'])
def deletePart(part_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletePart = session.query(Part).filter_by(id = part_id).one()
    if request.method == 'POST':
        session.delete(deletePart)
        session.commit()
        flash('Part Successfully Deleted')
        return redirect(url_for('showHome'))
    else:
        return render_template('deletepart.html', part = deletePart)




@app.route('/part/<string:part_type>/')
def showAllPartsOfType(part_type):
    parts = session.query(Part).filter_by(type = part_type).all()
    if 'username' in login_session:
        return render_template('partsoftype.html', parts = parts, type = part_type)
    else:
        return render_template('publicpartsoftype.html', parts = parts, type = part_type)





############ JSON

@app.route('/part/<int:part_id>/JSON')
def partInfoJSON(part_id):
    part = session.query(Part).filter_by(id = part_id).one()
    return jsonify(part.serialize)


# show parts from manufacturer


# @app.route('/compare/<int:part_id1>/<int:part_id2>/')
# def compareParts(part_id1, part_id2):




############################################################################
#
#                           BUILD METHODS
#
##########################################################################

# @app.route('/build/')
# def showAllBuilds():
#
#
#
#
# @app.route('/build/<string:build_name>')
# def showBuild(build_name):
#
#
#
#
# @app.route('/build/new', methods = ['GET', 'POST'])
# def createBuild():
#
#
#
#
#
# @app.route('/build/<string:build_name>/edit', methods = ['GET', 'POST'])
# def editBuild(build_name):
#
#
#
#
#
# @app.route('/build/<string:build_name>/delete', methods = ['GET', 'POST'])
# def deleteBuild(build_name):
#
#
#
#
#
#
# @app.route('/wishlist/')
# def showUserWishlist():

##############################################################################


if __name__ == '__main__':
    app.secret_key = 'asdfq'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
