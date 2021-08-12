from flask import jsonify
from dao.clothDAO import ClothDAO



class Cloth:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['cloth_type'] = row[1]
        result['cloth_quantity'] = row[2]
        return result

    def createCloth(self, json):
        resource_id = json['resource_id']
        cloth_name = json['cloth_type']
        cloth_quantity = json['cloth_quantity']
        dao = ClothDAO()
        cid = dao.insert_cloth(resource_id, cloth_type, cloth_quantity)
        if cid:
            return jsonify("Added cloth", {"cloth_id": cid}), 200
        return jsonify("ERROR"), 404

    def getCloth(self, cid):
        dao = ClothDAO()
        cloth = dao.get_cloth_by_id(cid)
        if cloth:
            result = self.build_map_dict(cloth)
            return jsonify(result), 200
        return jsonify("NOT FOUND"), 404

    def getAllCloth(self):
        dao = ClothDAO()
        result = dao.get_all_cloth()
        result_list = []
        for row in result:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(Cloth=result_list), 200
    
    def changeClothQuantity(self, cloth_quantity, cloth_id):
        dao = ClothDAO()
        check = dao.get_cloth_by_id
        if not check:
            return jsonify("ERROR: Cloth not found"), 404
        else:
            self.build_map_dict(check)
            amount = check[2] + cloth_quantity
            if cloth_quantity < 0:
                if cloth_quantity <= check[2]:
                    dao.change_cloth_quantity(amount, cloth_id)
                    return jsonify("Cloth quantity updated", {"cloth_id": cloth_id, "cloth_quantity": amount}) 200
                else:
                    return jsonify("ERROR: Cloth needed exceeds available"), 406
            else:
                dao.change_cloth_quantity(amount, cloth_id)
                return jsonify("Cloth quantity updated", {"cloth_id": cloth_id, "cloth_quantity": amount}) 200

