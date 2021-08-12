from flask import jsonify
from dao.leader import LeaderDAO
from dao.users import UserDAO
from dao.faction import FactionsDAO

class LeaderHandler:

    # leader_id, leader_firstname, leader_lastname, leader_date_birth, leader_status
    def build_leader_attributes(self, user_id, leader_id, leader_firstname, leader_lastname, leader_date_birth, leader_status):
        result = {}
        result['user_id'] = user_id
        result['leader_id'] = leader_id 
        result['leader_firstname'] = leader_firstname
        result['leader_lastname'] = leader_lastname
        result['leader_date_birth'] = leader_date_birth
        result['leader_status'] = leader_status
        return result

    def build_leader_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['leader_id'] = row[1]
        result['leader_firstname'] = row[2]
        result['leader_lastname'] = row[3]
        result['leader_date_birth'] = row[4]
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

    def getAllLeader(self):
        dao = LeaderDAO()
        result = dao.getAllLeaders()
        result_list = []
        for row in result:
            result = self.build_leader_dict(row)
            result_list.append(result)
        return jsonify(leaders = result_list)

    def getLeaderById(self, leader_id):
        dao = LeaderDAO()
        row = dao.getLeaderById(leader_id)
        if not row:
            return jsonify(Error = "leader Not Found"), 404
        else:
            leader = self.build_leader_dict(row)
            return jsonify(leader = leader)
    
    def getleadersByFactionId(self, company_id):
        faction_dao = FactionDAO()
        if not faction_dao.getFactionById(company_id):
            return jsonify(Error = "Faction Not Found"), 404
        else:
            leader_dao = LeaderDAO()
            result_list = []
            leader_list = Leader_dao.getleadersByFactionId(company_id)
            for row in leader_list:
                result = self.build_leader_dict(row)
                result_list.append(result)
            return jsonify(leaders = result_list)

    def getAllLeaderResources(self, leader_id):
        dao = LeaderDAO()
        result = dao.getAllleaderResources(leader_id)
        result_list = []
        for row in result:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resources = result_list)

    def searchLeaders(self, args):
        leader_firstname = args.get('leader_firstname')
        leader_lastname = args.get("leader_lastname")
        leader_email = args.get('leader_email')
        leader_phone = args.get('leader_phone')
        leader_date_birth = args.get('leader_date_birth')
        dao = LeaderDAO()
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

    def insertLeader(self, json):
        leader_firstname = json['leader_firstname']
        leader_lastname = json['leader_lastname']
        leader_date_birth = json['leader_date_birth']
        leader_status = json['leader_status']

        if leader_firstname and leader_lastname and leader_date_birth and leader_status:
            dao_user = UserDAO()
            user_id = dao_user.insert(leader_firstname, leader_lastname, leader_date_birth, leader_status)
            dao_leader = LeaderDAO()
            leader_id = dao_leader.insert(user_id)
            result = self.build_leader_attributes(user_id, leader_id, leader_firstname, leader_lastname, leader_date_birth, leader_status)
            return jsonify(leader = result), 201
        else:
            return jsonify(Error = "Unexpected attributes in post request"), 400

    def deleteLeader(self, leader_id):
        leader_dao = LeaderDAO()
    
        if not leader_dao.getleaderById(leader_id):
            return jsonify(Error = "leader not found."), 404
        else:
            user_id = leader_dao.delete(leader_id)
            dao_phone = UserPhoneDAO()
            dao_phone.delete(user_id)
            user_dao = UserDAO()
            user_dao.delete(user_id)
            return jsonify(DeleteStatus = "OK"), 200

    def updateLeader(self, leader_id, json):
        dao_leader = LeaderDAO()
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
                user_id = dao_Leader.update(leader_id)
                dao_user.update(user_id, leader_firstname, leader_lastname, leader_date_birth, leader_status)
                result = self.build_leader_attributes(user_id, leader_id, leader_firstname, leader_lastname, leader_date_birth, leader_email, leader_phone_id, leader_phone)
                return jsonify(leader = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in update request"), 400