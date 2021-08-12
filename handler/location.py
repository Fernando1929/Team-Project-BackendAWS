from flask import jsonify
from dao.location import LocationDAO
from dao.users import UserDAO

class LocationHandler:

    def build_location_dict(self, row):
        result = {}
        result['location_id'] = row[0]
        result['user_id'] = row[1]
        result['city'] = row[2]
        result['state_province'] = row[3]
        return result

    def build_location_attributes(self, location_id, user_id, city, state_province):
        result = {}
        result['location_id'] = location_id
        result['user_id'] = user_id
        result['city'] = city
        result['state_province'] = state_province
        return result

    def getAllLocations(self):
        dao = LocationDAO()
        location_list = dao.getAllLocations()
        result_list = []
        for row in location_list:
            result = self.build_location_dict(row)
            result_list.append(result)
        return jsonify(Locations = result_list)

    def getLocationById(self, location_id):
        dao = LocationDAO()
        row = dao.getLocationById(location_id)
        if not row:
            return jsonify(Error = "Address Not Found"), 404
        else:
            location = self.build_location_dict(row)
            return jsonify(Address = location)

    def getLocationByUserId(self, user_id):
        user_dao = UserDAO()
        if not user_dao.getUserById(user_id):
            return jsonify(Error = "User not found."), 404
        else:
            dao = LocationDAO()
            row = dao.getLocationByUserId(user_id)
            if not row:
                return jsonify(Error = "Address Not Found"), 404
            else:
                location = self.build_location_dict(row)
                return jsonify(Address = location)


    def searchLocations(self, args):
        city = args.get("city")
        state_province = args.get("state_province")
        country = args.get("country")
        zipcode = args.get("zipcode")

        dao = LocationDAO()
        location_list = []
        if (len(args) == 1) and city:
            location_list = dao.getLocationsByCity(city)
        elif (len(args) == 1) and state_province:
            location_list = dao.getLocationsByStateOrProvince(state_province)
        elif (len(args) == 1) and country:
            location_list = dao.getLocationsByCountry(country)
        elif (len(args) == 1) and zipcode:
            location_list = dao.getLocationsByZipcode(zipcode)
        elif (len(args) == 2) and city and country:
            location_list = dao.getLocationsByCityAndCountry(city, country)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in location_list:
            result = self.build_location_dict(row)
            result_list.append(result)
        return jsonify(Locations = result_list)

    def insertAddress(self, json):
        user_id = json["user_id"]
        locationline = json["locationline"]
        city = json["city"]
        state_province = json["state_province"]
        country = json["country"]
        zipcode = json["zipcode"]

        user_dao = UserDAO()
        if not user_dao.getUserById(user_id):
            return jsonify(Error = "User not found."), 404
        else:
            if user_id and locationline and city and state_province and country and zipcode:
                Locaction_DAO = LocationDAO()
                location_id = Locaction_DAO.insert(user_id, locationline, city, state_province, country, zipcode)
                result = self.build_location_attributes(location_id, user_id, locationline, city, state_province, country, zipcode)
                return jsonify(Address = result), 201
            else:
                return jsonify(Error = "Unexpected attributes in post request"), 400

    def updateAddress(self, location_id, json):
        Locaction_DAO = LocationDAO()
        if not Locaction_DAO.getLocationById(location_id):
            return jsonify(Error = "Address not found."), 404
        else:
            user_id = json["user_id"]
            locationline = json["locationline"]
            city = json["city"]
            state_province = json["state_province"]
            country = json["country"]
            zipcode = json["zipcode"]

            if user_id and locationline and city and state_province and country and zipcode:
                Locaction_DAO = LocationDAO()
                location_id = Locaction_DAO.update(location_id, user_id, locationline, city, state_province, country, zipcode)
                result = self.build_location_attributes(location_id, user_id, locationline, city, state_province, country, zipcode)
                return jsonify(Address = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in update request"), 400

    def deleteAddress(self, location_id):
        Locaction_DAO = LocationDAO()
        if not Locaction_DAO.getLocationById(location_id):
            return jsonify(Error = "Address not found."), 404
        else:
            Locaction_DAO.delete(location_id)
            return jsonify(DeleteStatus = "OK"), 200