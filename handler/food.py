from flask import jsonify
from dao.foodDAO import FoodDAO


class Food:
    def build_map_dict(self, row):
        result = {}
        result['resource_id'] = row[0]
        result['food_category'] = row[1]
        result['food_quantity'] = row[2]
        result['food_type'] = row[3]
        return result

    def createFood(self, json):
        resource_id = json['resource_id']
        food_category = json['food_category']
        food_quantity = json['food_quantity']
        food_name = json['food_type']
        dao = FoodDAO()
        fid = dao.insert_food(resource_id, food_category, food_quantity, food_type)
        if fid:
            return jsonify("Added food", {"food_id": fid}), 200
        return jsonify("ERROR"), 404

    def getFood(self, fid):
        dao = FoodDAO()
        food = dao.get_food_by_id(fid)
        if food:
            result = self.build_map_dict(food)
            return jsonify(result), 200
        return jsonify("NOT FOUND"), 404

    def getAllFood(self):
        dao = FoodDAO()
        result = dao.get_all_food()
        result_list = []
        for row in result:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(Food=result_list), 200
    
    def changeFoodQuantity(self, food_quantity, food_id):
        dao = FoodDAO()
        check = dao.get_food_by_id(food_id)
        if not check:
            return jsonify("ERROR: Food not found"), 404
        else:
            self.build_map_dict(check)
            amount = check[2] + food_quantity
            if food_quantity < 0:
                if food_quantity <= check[2]:
                    dao.change_food_quantity(amount, food_id)
                    return jsonify("food quantity updated", {"food_id": food_id, "food_quantity": amount}) 200
                else:
                    return jsonify("ERROR: Food needed exceeds available"), 406
            else:
                dao.change_food_quantity(amount, food_id)
                return jsonify("Food quantity updated", {"food_id": food_id, "food_quantity": amount}) 200

