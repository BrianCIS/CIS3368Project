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

# http://127.0.0.1:5000/api/adduserprofile

@app.route('/api/adduserprofile', methods=['POST']) #endppoint to add user to profiles table
def add_profile(): 
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.get_json()
    newfname = request_data['firstname']
    newlname = request_data['lastname']

    sql = "INSERT INTO profiles (firstname, lastname) values('{}','{}')".format(newfname, newlname)

    execute_query(conn, sql)

    return 'POST REQUEST WORKED'


@app.route('/api/addrestaurant', methods=['POST']) #endppoint to add user to profiles table
def add_restaurant(): 
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.get_json()
    newrestaurant = request_data['restaurant']
    user_id = request_data['user_id']
    sql = "INSERT INTO restaurants (restaurant, user_id) values('{}', '{}')".format(newrestaurant, user_id)

    execute_query(conn, sql)

    return 'POST REQUEST WORKED'

@app.route('/api/deleterestaurant', methods=['POST'])
def del_entry():
     request_data = request.get_json()
     #user input
     del_id = request_data['id']
     conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
     sql = "DELETE FROM ``.`celestial_object` WHERE id = %s" % (del_id)
     execute_query(conn, sql) 
     return "<p>POST REQUEST WORK</p>"
     

@app.route('/api/updateuser', methods=['PUT'])
def update_guest():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.json
    user_id = request_data['user_id']
    new_fname = request_data['first name']
    new_lname = request_data['last name']
    sql = """UPDATE guests 
    SET firstname = "%s", lastname = %s
    WHERE id = %s """ % (new_lname,new_fname,user_id,)
    execute_query(conn, sql)

    return "PUT REQUEST WORKS"
@app.route('/api/updaterest', methods=['PUT'])
def update_rest():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.json
    rest_id = request_data['id']
    sql = """UPDATE restaurant 
    SET restaurant = "%s" WHERE id = %s """ % (rest_id,rest_id)
    execute_query(conn, sql)

    return "PUT REQUEST WORKS"


@app.route('/api/updaterest', methods=['PUT'])
def print_name():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.json
    rest_name = request_data['rest name']
    sql = ("SELECT * FROM restaurants WHERE restaurant = %s " % (rest_name)

    
app.run()
