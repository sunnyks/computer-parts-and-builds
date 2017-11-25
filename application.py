from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy import sessionmaker
from database_setup import Base, User, Part, Motherboard, CPU, CPU_Cooler, Memory, Storage, GPU, PowerSupply, SoundCard, Wishlist, Build

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import jsonify
from flask import make_response
import requests



engine = create_engine('sqlite:///computerpartsandbuilds.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/login')
def showLogin():




@app.route('/gconnect', methods=['POST'])
def gconnect():




@app.route('/gdisconnect')
def gdisconnect():



@app.route('/')
def showHome():
    # list categories and show recently added parts & builds




@app.route('/part/')
def showAllParts():




@app.route('/part/<int:part_id>/')
def showPart(part_id):




@app.route('/part/new/', methods = ['GET', 'POST'])
def createPart():





@app.route('/part/<int:part_id>/edit', methods = ['GET', 'POST'])
def editPart(part_id):




@app.route('/part/<int:part_id>/delete', methods = ['GET', 'POST'])
def deletePart(part_id):




@app.route('/compare/<int:part_id1>/<int:part_id2>/')
def compareParts(part_id1, part_id2):






@app.route('/part/cpu/')
def showAllCPUs():




@app.route('/part/cpucooler/')
def showAllCPUCoolers():




@app.route('/part/motherboard/')
def showAllMotherboards():




@app.route('/part/memory/')
def showAllMemory():




@app.route('/part/storage/')
def showAllStorage():




@app.route('/part/GPU/')
def showAllGPUs




@app.route('/part/powersupply/')
def showAllPowerSupplies():




@app.route('/part/soundcard')
def showAllSoundcards():




@app.route('/build/')
def showAllBuilds():




@app.route('/build/<string:build_name>')
def showBuild(build_name):




@app.route('/build/new', methods = ['GET', 'POST'])
def createBuild():





@app.route('/build/<string:build_name>/edit', methods = ['GET', 'POST'])
def editBuild(build_name):





@app.route('/build/<string:build_name>/delete', methods = ['GET', 'POST'])
def deleteBuild(build_name):





    
@app.route('/wishlist/')
def showUserWishlist():






##############################################################################
# JSON METHODS & Stuff idk
