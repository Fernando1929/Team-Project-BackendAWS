## Dependencies
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

## Handlers
from handler.credentials import CredentialsHandler
from handler.survivor import SurvivorHandler
from handler.faction import FactionHandler
from handler.location import LocationHandler
from handler.leader import LeaderDAO


app = Flask(__name__)

# mysql = MySQL()
# mysql.init_app(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

CORS(app)

@app.route('/')
def greeting():
    return 'Amazon Prime Z'

## translate to handler and dao
# Register function 
@app.route("/register", methods = ['POST'])
def register():

    # Connect database
    conn = mysql.connect()
    cursor = conn.cursor()

    # Read data from GUI
    data = request.get_json()["newUser"]
    
    # Saving values
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    status = "new"

    # Check if the username is taken 
    query = "SELECT * from users where username = %s"
    cursor.execute(query,(username))
    result = cursor.fetchone()

    print(result)

    if(result == None):
        # Save the user in the database
        query="INSERT INTO users (username, password, status) VALUES(%s, %s, %s)"
        cursor.execute(query,(username, password, status))

        conn.commit()

        return jsonify({'status': 'Registered'}), 200

    else:
        return jsonify({'msg': '*The username already exist.'}), 400


# # Login function
# @app.route("/login", methods = ['POST'])
# def login():

#     # Connect database
#     conn = mysql.connect()
#     cursor = conn.cursor()

#     # Read data from GUI
#     data = request.get_json()["user"]
    
#     # Saving values
#     username = data['username']
#     password = data['password']

#     # Get user from database 
#     cursor.execute("SELECT * FROM users where username = '" + str(username) + "'")
#     data = cursor.fetchone()

#     if data != None and bcrypt.check_password_hash(data[2], password):

#         access_token = create_access_token(identity = {
#             'id': data[0],
#             'username': data[1],
#             'status': data[3]
#         })

#         return access_token, 200

#     else:
#         return jsonify({"msg" : "Invalid username or password."}), 400


##########################################################################

################################## Credentials routes ##################################

@app.route("/login", methods=['POST'])
def addlogin():
    return CredentialsHandler().insertLogin(request.json)

@app.route("/login/<int:cred_id>", methods=['GET', 'PUT'])
def getLoginById(cred_id):
    if request.method == 'GET':
        return CredentialsHandler().getCredentialsById(cred_id)
    elif request.method == 'PUT':
        return CredentialsHandler().updateCredentials(cred_id, request.json)
    elif request.method == 'DELETE':## Left on standby
        return CredentialsHandler().deleteCredentials(cred_id)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/user/<int:user_id>/login", methods=['GET'])
def getLoginByUserId(user_id):
    return CredentialsHandler().getCredentialsByUserId(user_id)


################################## Credentials routes ##################################

################################## Location routes ##################################
@app.route("/user/location", methods=['GET', 'POST'])
def getAllAddresses():
    if request.method == 'POST':
        return Location_Handler().insertAddress(request.json)
    else:
        if not request.args:
            return Location_Handler().getAllAddresses()
        else:
            return Location_Handler().searchAddresses(request.args)

@app.route("/user/location/<int:location_id>", methods=['GET', 'PUT', 'DELETE'])
def getAddressById(location_id):
    if request.method == 'GET':
        return Location_Handler().getAddressById(location_id)
    elif request.method == 'PUT':
        return Location_Handler().updateAddress(location_id, request.json)
    elif request.method == 'DELETE':
        return Location_Handler().deleteAddress(location_id)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/user/<int:user_id>/location", methods=['GET'])
def getAddressesByUserId(user_id):
    return Location_Handler().getAddressesByUserId(user_id)

################################## Location routes ##################################

################################## Survivor routes ##################################

@app.route("/register/survivor", methods=['POST'])
def registerSurvivor():
    return SurvivorHandler().insertSurvivor(request.json)

@app.route("/survivor", methods=['GET'])
def getAllSurvivors():
    if not request.args:
        return SurvivorHandler().getAllSurvivors()
    else:
        return SurvivorHandler().searchSurvivors(request.args)

@app.route('/survivor/<int:survivor_id>', methods=['GET', 'PUT', 'DELETE'])
def getSurvivorById(survivor_id):
    if request.method == 'GET':
        return SurvivorHandler().getSurvivorById(survivor_id)
    elif request.method == 'PUT':
        return SurvivorHandler().updateSurvivor(survivor_id, request.json)
    elif request.method == 'DELETE':
        return SurvivorHandler().deleteSurvivor(survivor_id)
    else:
        return jsonify(Error="Method not allowed."), 405

################################## Survivor routes ##################################

################################## Faction routes ##################################

@app.route('/factions', methods = ['GET','POST'])
def getAllFactions():
    if request.method == 'POST':
        return FactionHandler().insertFaction(request.json)
    else :
        if not request.args:
            return FactionHandler().getAllFactions()
        else:
            return FactionHandler().searchFaction(request.args)

@app.route('/faction/<int:faction_id>', methods = ['GET','PUT','DELETE'])
def getFactionById(faction_id):
    if request.method == 'GET':
        return FactionHandler().getFactionById(faction_id)
    elif request.method == 'PUT':
        return FactionHandler().updateFaction(faction_id, request.json)
    elif request.method == 'DELETE':
        return FactionHandler().deleteFaction(faction_id)
    else:
        return jsonify(Error = "Method not allowed"), 405

@app.route('/faction_leader/<int:faction_leader_id>/faction', methods = ['GET'])
def getFactionBySupplierId(faction_leader_id):
    return FactionHandler().getFactionByLeaderId(faction_leader_id)

################################## Faction routes ##################################

if __name__ == '__main__':
    app.run(debug=True)