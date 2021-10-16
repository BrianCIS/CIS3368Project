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
    return "<h1> WELCOME! </h1>"

@app.route('/api/rests/all', methods=['GET']) 
def api_all_rests():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    sql = "SELECT * FROM restaurants"
    guests = execute_read_query(conn, sql)
    users = []
    for body in guests:
            users.append(body)
    return jsonify(users)



@app.route('/api/users', methods=['GET']) #API to get a user from the db table in AWS by id as a JSON response: http://127.0.0.1:5000/api/profiles?id=1
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

@app.route('/api/adduser', methods=['POST']) #endppoint to add user to profiles table
def add_user(): 
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.get_json()
    newfname = request_data['firstname']
    newlname = request_data['lastname']
    sql = "INSERT INTO users (firstname, lastname) values('{}','{}')".format(newfname, newlname)
    execute_query(conn, sql)
    return 'POST REQUEST WORKED'


@app.route('/api/addrestaurant', methods=['POST']) #endppoint to add user to profiles table
def add_restaurant(): 
    if 'user_id' in request.args: #only if an id is provided as an argument, proceed
        user_id = int(request.args['user_id'])
    else:
        return 'ERROR: No ID provided!'

    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax","cis3368fall21")
    request_data = request.get_json()
    

    for i in request_data:
        sql = "INSERT INTO restaurants (restaurant, user_id) values('{}', '{}')".format(i['restaurant'], user_id)
        #print (i)
        execute_query(conn, sql)

    return 'POST REQUEST WORKED'
 

@app.route('/api/deleteuser', methods=['DELETE'])
def del_entry():
     request_data = request.get_json()
     del_id = request_data['user_id']
    
     conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
     sql = "DELETE FROM users WHERE user_id = %s" % (del_id)
     execute_query(conn, sql) 

     return "<p>DELETE REQUEST WORKED</p>"
     

@app.route('/api/updateuser', methods=['PUT'])
def update_user():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.json
    user_id = request_data['user_id']
    new_fname = request_data['firstname']
    new_lname = request_data['lastname']
    sql = """UPDATE users 
    SET firstname = "%s", lastname = "%s"
    WHERE user_id = %s """ % (new_lname, new_fname, user_id,)
    execute_query(conn, sql)
    return "PUT REQUEST WORKS"

@app.route('/api/updaterest', methods=['PUT'])
def update_rest():
    conn = create_connection("cis3368.cpnrvwg2unom.us-east-1.rds.amazonaws.com", "myadmin", "qakgu6-wovcaf-subXax", "cis3368fall21")
    request_data = request.json
    rest_id = request_data['id']
    rest_new = request_data['restaurant']
    sql = """UPDATE restaurants 
    SET restaurant = "%s" WHERE id = %s """ % (rest_new,rest_id)
    execute_query(conn, sql)
    return "PUT REQUEST WORKS"


app.run()
