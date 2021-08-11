from flask import jsonify
from dao.credentials import CredentialsDAO
from dao.users import UserDAO

class CredentialsHandler:

    def build_cred_dict(self, row):
        result = {}
        result['cred_id'] = row[0]
        result['username'] = row[1]
        result['password'] = row[2]
        result['user_id'] = row[3]
        return result

    def build_cred_attributes(self, cred_id, user_id, username, password):
        result = {}
        result['cred_id'] = cred_id
        result['user_id'] = user_id
        result['username'] = username
        result['password'] = password
        return result

    def getCredentialsById(self, cred_id):
        dao = CredentialsDAO()
        row = dao.getCredentialsById(cred_id)
        print(row)
        if not row:
            return jsonify(Error = "Credentials Not Found"), 404
        else:
            cred = self.build_cred_dict(row)
            return jsonify(Credentials = cred)

    def getCredentialsByUserId(self, user_id):
        user_dao = UserDAO()
        if not user_dao.getUserById(user_id):
            return jsonify(Error = "User not found."), 404
        else:
            dao = CredentialsDAO()
            row = dao.getCredentialsByUserId(user_id)
            if not row:
                return jsonify(Error = "Credentials Not Found"), 404
            else:
                login = self.build_cred_dict(row)
                return jsonify(Credentials = login)

    def insertCredentials(self, json):
        user_id = json["user_id"]
        username = json["username"]
        password = json["password"]

        cred_dao = CredentialsDAO()
        user_dao = UserDAO()
        
        if not user_dao.getUserById(user_id):
            return jsonify(Error = "User not found."), 404
        elif cred_dao.getCredentialsByUserId(user_id):
            return jsonify(Error = "Credentials for this user already exists"), 409
        else:        
            if user_id and username and password:
                cred_id = cred_dao.insert(user_id, username, password)
                result = self.build_cred_attributes(cred_id, user_id, username, password)
                return jsonify(Credentials = result), 201
            else:
                return jsonify(Error = "Unexpected attributes in post request"), 400

    def updateCredentials(self, cred_id, json):
        cred_dao = CredentialsDAO()
        if not cred_dao.getCredentialsById(cred_id):
            return jsonify(Error = "Credentials not found."), 404
        else:
            user_id = json["user_id"]
            username = json["username"]
            password = json["password"]

            if user_id and username and password:
                cred_dao = CredentialsDAO()
                cred_id = cred_dao.update(cred_id, username, password, user_id)
                result = self.build_cred_attributes(cred_id, user_id, username, password)
                return jsonify(Credentials = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in post request"), 400

    def deleteUserAndCredentials(self, user_id): ## Check it later
        cred_dao = CredentialsDAO()
        user_dao = UserDAO()
        
        if not cred_dao.getCredentialsById(cred_id):
            return jsonify(Error = "Credentials not found."), 404
        else:
            user_dao.delete(user_id)
            cred_dao.delete(cred_id)
            return jsonify(DeleteStatus = "OK"), 200