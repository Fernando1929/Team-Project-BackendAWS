from flask import jsonify
from dao.resource import ResourceDAO


class Resource:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['resource_name'] = row[1]
        result['resource_availability'] = row[2]
        return result

    def createResource(self, json):
        resource_name = json['resource_name']
        resource_availability = json['resource_availability']
        dao = ResourceDAO()
        rid = dao.insert_resource(resource_name, resource_availability)
        if rid:
            return jsonify("Added resource", {"resource_id": rid}), 200
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
    
    def updateResource(self, json, rid):
        dao = ResourceDAO()
        check = dao.get_resource_by_id(rid)
        if not check:
            return jsonify("ERROR: not a resource"), 404
        else:
            resource_name = json["resource_name"]
            resource_availability = json["resource_availability"]
            dao.update_resource(resource_name, resource_availability, rid)
            return jsonify("Resource updated", {"resource_id": rid}), 200
    
    def deleteResource(self, rid):
        dao = ResourceDAO()
        check = dao.delete_resource(rid)
        if not check:
            return jsonify("ERROR: not a resource"), 404
        else:
            return jsonify("Resource deleted", {"resource_id": rid}), 200

