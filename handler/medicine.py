from flask import jsonify
from dao.medDAO import MedicineDAO



class Med:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['med_type'] = row[1]
        result['med_quantity'] = row[2]
        return result

    def createMed(self, json):
        resource_id = json['resource_id']
        med_name = json['med_type']
        med_quantity = json['med_quantity']
        dao = MedicineDAO()
        mid = dao.insert_medicine(resource_id, med_type, med_quantity)
        if mid:
            return jsonify("Added med", {"med_id": mid}), 200
        return jsonify("ERROR"), 404

    def getMed(self, mid):
        dao = MedDAO()
        med = dao.get_medicine_by_id(mid)
        if med:
            result = self.build_map_dict(med)
            return jsonify(result), 200
        return jsonify("NOT FOUND"), 404

    def getAllMed(self):
        dao = MedicineDAO()
        result = dao.get_all_medicine()
        result_list = []
        for row in result:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(Medicine=result_list), 200
    
    def changeMedicineQuantity(self, med_quantity, med_id):
        dao = MedicineDAO()
        check = dao.get_medicine_by_id(med_id)
        if not check:
            return jsonify("ERROR: Medicine not found"), 404
        else:
            self.build_map_dict(check)
            amount = check[2] + med_quantity
            if med_quantity < 0:
                if med_quantity <= check[2]:
                    dao.change_medicine_quantity(amount, med_id)
                    return jsonify("Medicine quantity updated", {"med_id": med_id, "med_quantity": amount}) 200
                else:
                    return jsonify("ERROR: Medicine needed exceeds available"), 406
            else:
                dao.change_medicine_quantity(amount, med_id)
                return jsonify("Medicine quantity updated", {"med_id": med_id, "med_quantity": amount}) 200

