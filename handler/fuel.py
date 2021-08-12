from flask import jsonify
from dao.fuelDAO import FuelDAO



class Fuel:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['fuel_type'] = row[1]
        result['fuel_quantity'] = row[2]
        return result

    def createFuel(self, json):
        resource_id = json['resource_id']
        fuel_name = json['fuel_type']
        fuel_quantity = json['fuel_quantity']
        dao = FuelDAO()
        fid = dao.insert_fuel(resource_id, fuel_type, fuel_quantity)
        if fid:
            return jsonify("Added fuel", {"fuel_id": fid}), 200
        return jsonify("ERROR"), 404

    def getFuel(self, fid):
        dao = FuelDAO()
        fuel = dao.get_fuel_by_id(fid)
        if fuel:
            result = self.build_map_dict(fuel)
            return jsonify(result), 200
        return jsonify("NOT FOUND"), 404

    def getAllFuel(self):
        dao = FuelDAO()
        result = dao.get_all_fuel()
        result_list = []
        for row in result:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(Fuel=result_list), 200
    
    def changeFuelQuantity(self, fuel_quantity, fuel_id):
        dao = FuelDAO()
        check = dao.get_fuel_by_id(fuel_id)
        if not check:
            return jsonify("ERROR: Fuel not found"), 404
        else:
            self.build_map_dict(check)
            amount = check[2] + fuel_quantity
            if fuel_quantity < 0:
                if fuel_quantity <= check[2]:
                    dao.change_fuel_quantity(amount, fuel_id)
                    return jsonify("Fuel quantity updated", {"fuel_id": fuel_id, "fuel_quantity": amount}) 200
                else:
                    return jsonify("ERROR: Fuel needed exceeds available"), 406
            else:
                dao.change_fuel_quantity(amount, fuel_id)
                return jsonify("Fuel quantity updated", {"fuel_id": fuel_id, "fuel_quantity": amount}) 200
    
    def deleteFuel(self, fuel_id):
        dao = FuelDAO()
        check = dao.delete_fuel(fuel_id)
        if not check:
            return jsonify("ERROR: Fuel not found"), 404
        else:
            return jsonify("Fuel deleted", {"fuel_id": fuel_id}) 200

