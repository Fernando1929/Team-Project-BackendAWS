from flask import jsonify
from dao.resourceDAO import ResourceDAO
from model.user import UserDAO


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
    
    def changeResourceAvailability(self, rid):
        dao = ResourceDAO()
        check = dao.get_resource_by_id
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

