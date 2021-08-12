from flask import jsonify
from dao.leader import LeaderDAO
from dao.users import UserDAO
from dao.faction import FactionsDAO

class LeaderHandler:

    def build_leader_attributes(self, user_id, leader_id, leader_firstname, leader_lastname, leader_date_birth, leader_email, leader_phone_id, leader_phone):
        result = {}
        result['user_id'] = user_id
        result['leader_id'] = leader_id 
        result['leader_firstname'] = leader_firstname
        result['leader_lastname'] = leader_lastname
        result['leader_date_birth'] = leader_date_birth
        result['leader_email'] = leader_email
        result['leader_phone_id'] = leader_phone_id
        result['leader_phone'] = leader_phone
        return result

    def build_leader_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['leader_id'] = row[1]
        result['leader_firstname'] = row[2]
        result['leader_lastname'] = row[3]
        result['leader_date_birth'] = row[4]
        result['leader_email'] = row[5]
        result['leader_phone_id'] = row[6]
        result['leader_phone'] = row[7]
        return result 

    def build_resource_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['leader_id'] = row[1]
        result['category_id'] = row[2]
        result['resource_name'] = row[3]
        result['resource_brand'] = row[4]
        result['resource_quantity'] = row[5]
        result['resource_price'] = row[6]
        return result

    def getAllleaders(self):
        dao = leaderDAO()
        result = dao.getAllleaders()
        result_list = []
        for row in result:
            result = self.build_leader_dict(row)
            result_list.append(result)
        return jsonify(leaders = result_list)

    def getleaderById(self, leader_id):
        dao = leaderDAO()
        row = dao.getleaderById(leader_id)
        if not row:
            return jsonify(Error = "leader Not Found"), 404
        else:
            leader = self.build_leader_dict(row)
            return jsonify(leader = leader)
    
    def getleadersByCompanyId(self, company_id):
        company_dao = CompanyDAO()
        if not company_dao.getCompanyById(company_id):
            return jsonify(Error = "Company Not Found"), 404
        else:
            leader_dao = leaderDAO()
            result_list = []
            leader_list = leader_dao.getleadersByCompanyId(company_id)
            for row in leader_list:
                result = self.build_leader_dict(row)
                result_list.append(result)
            return jsonify(leaders = result_list)

    def getAllleaderResources(self, leader_id):
        dao = leaderDAO()
        result = dao.getAllleaderResources(leader_id)
        result_list = []
        for row in result:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resources = result_list)

    def searchleaders(self, args):
        leader_firstname = args.get('leader_firstname')
        leader_lastname = args.get("leader_lastname")
        leader_email = args.get('leader_email')
        leader_phone = args.get('leader_phone')
        suppplier_date_birth = args.get('leader_date_birth')
        dao = leaderDAO()
        leader_list = []
        if (len(args) == 2) and leader_firstname and leader_lastname:
            leader_list = dao.getleadersByFirstnameAndLastname(leader_firstname , leader_lastname)
        elif (len(args) == 1) and leader_firstname:
            leader_list = dao.getleadersByFirstname(leader_firstname)
        elif (len(args) == 1) and leader_lastname:
            leader_list = dao.getleadersByLastname(leader_lastname)
        elif(len(args) == 1) and leader_email:
            leader_list = dao.getleaderByEmail(leader_email)
        elif(len(args) == 1) and leader_phone:
            leader_list = dao.getleaderByPhone(leader_phone)
        elif(len(args) == 1) and suppplier_date_birth:
            leader_list = dao.getleadersByDateOfBirth(suppplier_date_birth)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in leader_list:
            result = self.build_leader_dict(row)
            result_list.append(result)
        return jsonify(leaders = result_list)

    def insertleader(self, json):
        leader_firstname = json['leader_firstname']
        leader_lastname = json['leader_lastname']
        leader_date_birth = json['leader_date_birth']
        leader_email = json['leader_email']
        leader_phone = json['leader_phone']

        if leader_firstname and leader_lastname and leader_date_birth and leader_email and leader_phone:
            dao_user = UserDAO()
            user_id = dao_user.insert(leader_firstname, leader_lastname, leader_date_birth, leader_email)
            dao_phone = UserPhoneDAO()
            leader_phone_id = dao_phone.insert(user_id, leader_phone)
            dao_leader = leaderDAO()
            leader_id = dao_leader.insert(user_id)
            result = self.build_leader_attributes(user_id, leader_id, leader_firstname, leader_lastname, leader_date_birth, leader_email, leader_phone_id, leader_phone)
            return jsonify(leader = result), 201
        else:
            return jsonify(Error = "Unexpected attributes in post request"), 400

    def deleteleader(self, leader_id):
        leader_dao = leaderDAO()
    
        if not leader_dao.getleaderById(leader_id):
            return jsonify(Error = "leader not found."), 404
        else:
            user_id = leader_dao.delete(leader_id)
            dao_phone = UserPhoneDAO()
            dao_phone.delete(user_id)
            user_dao = UserDAO()
            user_dao.delete(user_id)
            return jsonify(DeleteStatus = "OK"), 200

    def updateleader(self, leader_id, json):
        dao_leader = leaderDAO()
        dao_user = UserDAO()
        if not dao_leader.getleaderById(leader_id):
            return jsonify(Error = "leader not found."), 404
        else:
            leader_firstname = json['leader_firstname']
            leader_lastname = json['leader_lastname']
            leader_date_birth = json['leader_date_birth']
            leader_email = json['leader_email']
            leader_phone = json['leader_phone']
            leader_phone_id = json["leader_phone_id"]

            if leader_firstname and leader_lastname and leader_date_birth and leader_email and leader_phone and leader_phone_id:
                user_id = dao_leader.update(leader_id)
                dao_user.update(user_id, leader_firstname, leader_lastname, leader_date_birth, leader_email)
                dao_phone = UserPhoneDAO()
                dao_phone.update(user_id, leader_phone) 
                result = self.build_leader_attributes(user_id, leader_id, leader_firstname, leader_lastname, leader_date_birth, leader_email, leader_phone_id, leader_phone)
                return jsonify(leader = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in update request"), 400