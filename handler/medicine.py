from flask import jsonify
from dao.medicine import MedicineDAO



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
        dao = MedicineDAO()
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
    
    def updateMed(self, json, med_id):
        dao = MedicineDAO()
        check = dao.get_med_by_id(med_id)
        if not check:
            return jsonify("ERROR: Medicine not found"), 404
        else:
            med_type = json['med_type']
            med_quantity = json['med_quantity']
            dao.update_med(med_type, med_quantity, med_id)
            return jsonify("Medicine updated", {"med_type": med_type, "med_quantity": med_quantity}), 200
        
    def deleteMed(self, med_id):
        dao = MedicineDAO()
        check = dao.delete_medicine(med_id)
        if not check:
            return jsonify("ERROR: Medicine not found"), 404
        else:
            return jsonify("Medicine deleted", {"med_id": med_id}), 200

