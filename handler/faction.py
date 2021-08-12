from flask import jsonify
from dao.faction import FactionsDAO 
from dao.leader import LeaderDAO

class FactionHandler:

    # leader_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory
    def build_faction_dict(self, row):
        print(row)
        result = {}
        result['faction_id'] = row[0]
        result['faction_name'] = row[1]
        result['faction_population'] = row[2] 
        result['faction_rating'] = row[3]
        result['faction_wealth'] = row[4] 
        result['faction_territory'] = row[5]
        return result

    def build_faction_attributes(self, faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory):
        result = {}
        result['faction_id'] = faction_id
        result['faction_name'] = faction_name
        result['faction_population'] = faction_population 
        result['faction_rating'] = faction_rating
        result['faction_wealth'] = faction_wealth 
        result['faction_territory'] = faction_territory
        return result

    def getAllFactions(self):
        dao = FactionsDAO()
        result = dao.getAllFactions()
        result_list = []
        for row in result:
            result = self.build_faction_dict(row)
            result_list.append(result)
        return jsonify(Factions = result_list)

    def getFactionById(self, faction_id):
        dao = FactionsDAO()
        row = dao.getFactionById(faction_id)
        if not row:
            return jsonify(Error = "faction Not Found"), 404
        else:
            order = self.build_faction_dict(row)
            return jsonify(faction = order)

    def getFactionByLeaderId(self, leader_id):
        leader_dao = LeaderDAO()
        if not leader_dao.getLeaderById(leader_id):
            return jsonify(Error = "Leader Not Found"), 404
        else:
            faction_dao = FactionsDAO()
            faction = faction_dao.getFactionByLeaderId(leader_id)
            result = self.build_faction_dict(faction)
            print(result)
            return jsonify(faction = result)

    def searchFaction(self, args):
        faction_name = args.get('faction_name')
        faction_address = args.get('faction_address')
        faction_phone = args.get('faction_phone')
        dao = FactionsDAO()
        companies_list = []
        if (len(args) == 1) and faction_name:
            companies_list = dao.getFactionByName(faction_name)
        elif (len(args) == 1) and faction_address:
            companies_list = dao.getFactionByAddress(faction_address)
        elif (len(args) == 1) and faction_phone:
            companies_list = dao.getFactionByPhone(faction_phone)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in companies_list:
            result = self.build_faction_dict(row)
            result_list.append(result)
        return jsonify(faction = result_list)

    def insertFaction(self, json):
        leader_id = json['leader_id']
        faction_name = json['faction_name']
        faction_population = json['faction_population']
        faction_rating = json['faction_rating']
        faction_wealth = json['faction_wealth']
        faction_territory = json['faction_territory']

        if leader_id and faction_name and faction_population and faction_rating and faction_wealth and faction_territory:
            dao = FactionsDAO()
            faction_id = dao.insert(leader_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory)
            json = self.build_faction_attributes(faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory)
            return jsonify(faction = json), 201
        else:
            return jsonify(Error = "Unexpected attributes in post request"), 400

    def deleteFaction(self, faction_id):
        dao = FactionsDAO()
        if not dao.getFactionById(faction_id):
            return jsonify(Error = "faction not found."), 404
        else:
            dao.delete(faction_id)
            return jsonify(DeleteStatus = "OK"), 200

    def updateFaction(self, faction_id, json):
        dao = FactionsDAO()
        if not dao.getFactionById(faction_id):
            return jsonify(Error = "faction not found."), 404
        else:
            faction_id = json['faction_id']
            faction_name = json['faction_name']
            faction_address = json['faction_address']
            faction_phone = json['faction_phone']

            if faction_id and faction_name and faction_address and faction_phone:
                dao.update(faction_id, faction_name, faction_address, faction_phone)
                result = self.build_faction_attributes(faction_id, faction_name, faction_address, faction_phone)
                return jsonify(faction = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in update request"), 400