# Brian Rivera
# Jai Kapoor

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
    return "<h1> WELCOME TO OUR RESTAURANT! </h1>"

@app.route('/api/rests/all', methods=['GET']) # endpoint to print restaurant table in json format
def api_all_rests():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    sql = "SELECT * FROM restaurants"
    guests = execute_read_query(conn, sql)
    users = []
    for body in guests:
            users.append(body)
    return jsonify(users)

@app.route('/api/users/all', methods=['GET']) # endpoint to output users table in json format 
def api_all_users():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    # selects all user info from users table
    sql = "SELECT * FROM users"
    users = execute_read_query(conn, sql)
    results = []
    # populates results list with user info from user table
    for user in users:
            results.append(user)
    return jsonify(results)


@app.route('/api/adduser', methods=['POST']) #endppoint to add user to users table
def add_user(): 
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.get_json()
    newfname = request_data['firstname']
    newlname = request_data['lastname']
    # inserts new user into users table 
    sql = "INSERT INTO users (firstname, lastname) values('{}','{}')".format(newfname, newlname)
    execute_query(conn, sql)
    return 'POST REQUEST WORKED'


@app.route('/api/addrestaurant', methods=['POST']) #endppoint to add restaurant to restaurants table
def add_restaurant(): 
    if 'user_id' in request.args: 
        # proceeds only if an id is provided as an argument, pulls user_id from  url http://127.0.0.1:5000/api/users?id=1 
        # for user_id column of restaurants table
        user_id = int(request.args['user_id'])
    else:
        return 'ERROR: No ID provided!'

    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax","cis3368fall21")
    request_data = request.get_json()
    

    for i in request_data: # for each request data restaurant information is added to restaurant table for specific user
        sql = "INSERT INTO restaurants (restaurant, user_id) values('{}', '{}')".format(i['restaurant'], user_id)
        execute_query(conn, sql)

    return 'POST REQUEST WORKED'

@app.route('/api/deleteuser', methods=['DELETE']) # endpoint to delete user from users table 
def del_user():
     request_data = request.get_json()
     del_id = request_data['user_id']
    
     conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
     sql = "DELETE FROM users WHERE user_id = %s" % (del_id)
     execute_query(conn, sql) 

     return "<p>DELETE REQUEST WORKED</p>"
     # attempted to delete user, however due to foreign key constraint errors, deleting users with restaurants already posted prevented. Users without restaurants do delete.

@app.route('/api/deleterestaurant', methods=['DELETE']) # endpoint to delete restaurant from restaurant table 
def del_rest():
     request_data = request.get_json()
     del_id = request_data['id']
     conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
     sql = "DELETE FROM restaurants WHERE id = %s" % (del_id)
     execute_query(conn, sql) 
     return "<p>POST REQUEST WORKED</p>"

@app.route('/api/updateuser', methods=['PUT']) # endpoint to update user information for any given user on users table
def update_user():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.json
    user_id = request_data['user_id']
    new_fname = request_data['firstname']
    new_lname = request_data['lastname']
    # user updated via id. Where id equals given user id, corresponding user info is updated
    sql = """UPDATE users 
    SET firstname = "%s", lastname = "%s"
    WHERE user_id = %s """ % (new_lname, new_fname, user_id,)
    execute_query(conn, sql)
    return "PUT REQUEST WORKS"

@app.route('/api/updaterest', methods=['PUT']) # endpoint to update restaurant information for any given restaurant on restaurant table
def update_rest():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.json
    rest_id = request_data['id']
    rest_new = request_data['restaurant']
    # restaurant updated via id. Where id equals given restaurant id, corresponding restaurant info is updated
    sql = """UPDATE restaurants 
    SET restaurant = "%s" WHERE id = %s """ % (rest_new,rest_id)
    execute_query(conn, sql)
    return "PUT REQUEST WORKS"

@app.route('/api/selectusers', methods=['POST'])
def select_users():
    request_data = request.get_json()
    return jsonify(request_data)
# api to select users that are going to dinner from json input that contain name and availability 
# we were not able to figure out how to save the users given by the json input to a list of available users
# the list would need to be accessed in random api (below) to randomly select a restaurant from the choices of available users
 
@app.route('/api/random', methods=['GET'])
def random_rest():
    users=[]
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    # coded with intent to provided a random restaurant from given user ids that were given in selectuser api, if code ran as intended, 
    # unable to implement our logic into code appropriately 
    sql= "SELECT * FROM restaurants WHERE user_id IN (%s) ORDER BY RAND() LIMIT 1;" % (users)
    execute_query(conn, sql)
    return jsonify(sql)

app.run()
