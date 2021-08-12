from flask import jsonify
from dao.survivor import SurvivorDAO
from dao.users import UserDAO


class SurvivorHandler:
    
    def build_survivor_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['survivor_id'] = row[1]
        result['survivor_firstname'] = row[2]
        result['survivor_lastname'] = row[3]
        result['survivor_date_birth'] = row[4]
        return result

    def build_survivor_attributes(self, survivor_id, user_id, survivor_firstname, survivor_lastname, survivor_date_birth):
        result = {}
        result['survivor_id'] = survivor_id
        result['user_id'] = user_id
        result['survivor_firstname'] = survivor_firstname
        result['survivor_lastname'] = survivor_lastname
        result['survivor_date_birth'] = survivor_date_birth
        return result

    def getAllSurvivors(self):
        dao = SurvivorDAO()
        survivors_list = dao.getAllSurvivors()
        result_list = []
        for row in survivors_list:
            result = self.build_survivor_dict(row)
            result_list.append(result)
        return jsonify(survivors = result_list)

    def getSurvivorById(self, survivor_id):
        dao = SurvivorDAO()
        row = dao.getSurvivorById(survivor_id)
        if not row:
            return jsonify(Error = "survivor Not Found"), 404
        else:
            survivor = self.build_survivor_dict(row)
            return jsonify(survivor = survivor)

    def searchsurvivors(self, args):
        survivor_firstname = args.get("survivor_firstname")
        survivor_lastname = args.get("survivor_lastname")
        survivor_email = args.get("survivor_email")
        survivor_phone = args.get("survivor_phone")
        survivor_date_birth = args.get("survivor_date_birth")
        dao = SurvivorDAO()
        survivors_list = []
        if (len(args) == 2) and survivor_firstname and survivor_lastname:
            survivors_list = dao.getsurvivorsByFirstnameAndLastname(survivor_firstname, survivor_lastname)
        elif (len(args) == 1) and survivor_firstname:
            survivors_list = dao.getsurvivorsByFirstname(survivor_firstname)
        elif (len(args) == 1) and survivor_lastname:
            survivors_list = dao.getsurvivorsByLastname(survivor_lastname)
        elif (len(args) == 1) and survivor_email:
            survivors_list = dao.getsurvivorsByEmail(survivor_email)
        elif (len(args) == 1) and survivor_phone:
            survivors_list = dao.getsurvivorsByPhone(survivor_phone)
        elif (len(args) == 1) and survivor_date_birth:
            survivors_list = dao.getsurvivorsByDateOfBirth(survivor_date_birth)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in survivors_list:
            result = self.build_survivor_dict(row)
            result_list.append(result)
        return jsonify(survivors = result_list)

    def insertsurvivor(self, json):
        survivor_firstname = json['survivor_firstname']
        survivor_lastname = json['survivor_lastname']
        survivor_date_birth = json['survivor_date_birth']
        
        if survivor_firstname and survivor_lastname and survivor_date_birth and survivor_email and survivor_phone:
            user_dao = UserDAO()
            user_id = user_dao.insert(survivor_firstname, survivor_lastname, survivor_date_birth, survivor_email)
            dao_phone = UserPhoneDAO()
            survivor_phone_id = dao_phone.insert(user_id, survivor_phone)         
            survivor_dao = SurvivorDAO()
            survivor_id = survivor_dao.insert(user_id)
            result = self.build_survivor_attributes(survivor_id, user_id, survivor_firstname, survivor_lastname, survivor_date_birth, survivor_email, survivor_phone_id, survivor_phone)
            return jsonify(survivor = result), 201
        else:
            return jsonify(Error = "Unexpected attributes in post request"), 400

    def updatesurvivor(self, survivor_id, json):
        survivor_dao = SurvivorDAO()
        if not survivor_dao.getSurvivorById(survivor_id):
            return jsonify(Error = "survivor not found."), 404
        else:
            survivor_firstname = json["survivor_firstname"]
            survivor_lastname = json["survivor_lastname"]
            survivor_date_birth = json["survivor_date_birth"]
            survivor_email = json["survivor_email"]
            survivor_phone = json["survivor_phone"]
            survivor_phone_id = json["survivor_phone_id"]
            
            if survivor_firstname and survivor_lastname and survivor_date_birth and survivor_email and survivor_phone_id and survivor_phone:
                user_id = survivor_dao.update(survivor_id)
                user_dao = UserDAO()
                user_dao.update(user_id, survivor_firstname, survivor_lastname, survivor_date_birth, survivor_email)
                dao_phone = UserPhoneDAO()
                dao_phone.update(user_id, survivor_phone) 
                result = self.build_survivor_attributes(survivor_id, user_id, survivor_firstname, survivor_lastname, survivor_date_birth, survivor_email, survivor_phone_id, survivor_phone)
                return jsonify(survivor = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in update request"), 400

    def deletesurvivor(self, survivor_id):
        survivor_dao = SurvivorDAO()
        if not survivor_dao.getSurvivorById(survivor_id):
            return jsonify(Error = "survivor not found."), 404
        else:
            user_id = survivor_dao.delete(survivor_id)
            dao_phone = UserPhoneDAO()
            dao_phone.delete(user_id)
            user_dao = UserDAO()
            user_dao.delete(user_id)
            return jsonify(DeleteStatus = "OK"), 200