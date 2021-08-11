from flask import jsonify
from dao.resourceDAO import ClothDAO



class Resource:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['cloth_type'] = row[1]
        result['cloth_quantity'] = row[2]
        return result

    def createCloth(self, json):
        resource_id = json['resource_id']
        resource_name = json['cloth_type']
        resource_availability = json['cloth_quantity']
        dao = ResourceDAO()
        cid = dao.insert_resource(resource_id, cloth_type, cloth_quantity)
        if cid:
            return jsonify("Added cloth", {"cloth_id": cid}), 200
        return jsonify("ERROR"), 404

    def getResource(self, rid):
        dao = ResourceDAO()
        resource = dao.get_resource_by_id(rid)
        if resource:
            result = self.build_map_dict(resource)
            return jsonify(result), 200
        return jsonify("NOT FOUND"), 404

    def getAllResources(self):
        dao = ResourceDAO()
        result = dao.get_all_resources()
        result_list = []
        for row in result:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(Resources=result_list), 200
    
    def changeResourceAvailability(self, rid):
        dao = ResourceDAO()
        check = dao.get_cloth_by_id
        if not check:
            return jsonify("ERROR: not a resource"), 404
        else:
            self.build_map_dict(check)
            if check[2]
                dao.change_resource_availability(0, rid)
                return jsonify("Resource is no longer available", {"resource_id": rid}) 200
            else:
                dao.change_resource_availability(1, rid)
                return jsonify("Resource is now available", {"resource_id": rid}) 200

