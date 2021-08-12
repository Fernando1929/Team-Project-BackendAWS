from flask import jsonify
from dao.waterDAO import WaterDAO



class Water:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['water_container'] = row[1]
        result['water_quantity'] = row[2]
        result['water_type'] = row[3]
        return result

    def createWater(self, json):
        resource_id = json['resource_id']
        water_container = json['water_container']
        water_quantity = json['water_quantity']
        water_name = json['water_type']
        dao = WaterDAO()
        fid = dao.insert_water(resource_id, water_container, water_quantity, water_type)
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
    
    def changeWaterQuantity(self, water_quantity, water_id):
        dao = WaterDAO()
        check = dao.get_water_by_id
        if not check:
            return jsonify("ERROR: Water not found"), 404
        else:
            self.build_map_dict(check)
            amount = check[2] + water_quantity
            if water_quantity < 0:
                if amount >= 0:
                    dao.change_water_quantity(amount, water_id)
                    return jsonify("Water quantity updated", {"water_id": water_id, "water_quantity": amount}) 200
                else:
                    return jsonify("ERROR: Water needed exceeds available"), 406
            else:
                dao.change_water_quantity(amount, water_id)
                return jsonify("Water quantity updated", {"water_id": water_id, "water_quantity": amount}) 200

