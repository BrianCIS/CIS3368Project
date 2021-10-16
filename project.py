import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_query
from sql import execute_read_query

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

@app.route('/', methods=['GET']) # default url without any routing as GET request
def home():
    return "<h1> WELCOME TO OUR FIRST API! </h1>"

@app.route('/api/profiles/all', methods=['GET']) #endpoint to get all the cars # http://127.0.0.1:5000/api/profiles/all
def api_all():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    sql = "SELECT * FROM profiles"
    profiles = execute_read_query(conn, sql)
    users = []
    for body in profiles:
            users.append(body)
    return jsonify(users)

@app.route('/api/cars', methods=['GET']) #endppoint to get a single car by id
def api_id():
    if 'id' in request.args: #only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    
    results = [] #resulting car(s) to return
    for car in cars: 
        if car['id'] == id:
            results.append(car)
    return jsonify(results)

@app.route('/api/profiles', methods=['GET']) #API to get a user from the db table in AWS by id as a JSON response: http://127.0.0.1:5000/api/profiles?id=1
def api_users_id():
    if 'id' in request.args: #only if an id is provided as an argument, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    sql = "SELECT * FROM profiles"
    users = execute_read_query(conn, sql)
    results = []

    for user in users:
        if user['id'] == id:
            results.append(user)
    return jsonify(results)


@app.route('/api/adduserprofile', methods=['POST']) #endppoint to add user to profiles table
def add_profile(): 
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.get_json()
    newid = int(request_data['id'])
    newfname = request_data['firstname']
    newlname = request_data['lastname']

    sql = "INSERT INTO profiles (firstname, lastname) values('{}','{}')".format(newfname, newlname)

    execute_query(conn, sql)

    return 'POST REQUEST WORKED'


@app.route('/api/addrestaurant', methods=['POST']) #endppoint to add user to profiles table
def add_restaurant(): 
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.get_json()
    newid = int(request_data['id'])
    newrestaurant = request_data['restaurant']
    user_id = request_data['user_id']
    sql = "INSERT INTO restaurants (restaurant, user_id) values('{}', '{}')".format(newrestaurant, user_id)

    execute_query(conn, sql)

    return 'POST REQUEST WORKED' 
app.run()
