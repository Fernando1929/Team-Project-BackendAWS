from flask import jsonify
from dao.water import WaterDAO



class Water:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['water_quantity'] = row[1]
        result['water_container'] = row[2]
        result['water_type'] = row[3]
        return result

    def createWater(self, json):
        resource_id = json['resource_id']
        water_container = json['water_container']
        water_quantity = json['water_quantity']
        water_name = json['water_type']
        dao = WaterDAO()
        fid = dao.insert_water(resource_id, water_quantity, water_container, water_type)
        if fid:
            return jsonify("Added water", {"water_id": fid}), 200
        return jsonify("ERROR"), 404

    def getWater(self, fid):
        dao = WaterDAO()
        water = dao.get_water_by_id(fid)
        if water:
            result = self.build_map_dict(water)
            return jsonify(result), 200
        return jsonify("NOT FOUND"), 404

    def getAllWater(self):
        dao = WaterDAO()
        result = dao.get_all_water()
        result_list = []
        for row in result:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(Water=result_list), 200
    
    def updateWater(self, json, water_id):
        dao = WaterDAO()
        check = dao.get_water_by_id(water_id)
        if not check:
            return jsonify("ERROR: Water not found"), 404
        else:
            water_container = json['water_cotainer']
            water_quantity = json['water_quantity']
            water_type = json['water_type']
            dao.update_water(water_id, water_quantity, water_container, water_type)
            return jsonify("Water updated", {"water_type": water_type, "water_quantity": water_quantity}), 200

    def deleteWater(self, water_id):
        dao = WaterDAO()
        check = dao.get_water_by_id(water_id)
        if not check:
            return jsonify("ERROR: Water not found"), 404
        else:
            dao.delete_water(water_id)
            return jsonify("Water deleted", {"water_id": water_id}), 200