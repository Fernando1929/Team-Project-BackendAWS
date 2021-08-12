from db_config.dbconfig import mysql_config
import mysql.connector


class FoodDAO:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = mysql_config['DB_USERNAME'], 
            password = mysql_config['DB_PASSWORD'], 
            host = mysql_config['DB_WEBSERVER'], 
            database = mysql_config['DB_DATABASE']
        )

    def get_all_food(self):
        cursor = self.cnx.cursor()
        query = "select food_category, food_quantity, food_type from food "
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_food_by_id(self, f_id):
        cursor = self.cnx.cursor()
        query = "select food_category, food_quantity, food_type from food where food_id = %s "
        cursor.execute(query, (f_id,))
        result = cursor.fetchone()
        return result

    def insert_food(self, r_id, food_category, food_quantity, food_type):
        cursor = self.cnx.cursor()
        query = "insert into food (resource_id, food_category, food_quantity, food_type) values (%s,%s,%s,%s) "
        cursor.execute(query, (r_id, food_category, food_quantity, food_type,))
        food_id = cursor.fetchone()[0]
        self.cnx.commit()
        return food_id

    def change_food_quantity(self, food_quantity, f_id):
        cursor = self.cnx.cursor()
        ##add check to verify if the resource even exists.
        query = "update food set food_quantity=%s where food_id=%s "
        cursor.execute(query, (food_quantity, f_id,))
        self.cnx.commit()
        return f_id

    def get_food_quantity(self, f_id):
        cursor = self.cnx.cursor()
        query = "select food_quantity from food where food_id = %s "
        cursor.execute(query, (f_id,))
        result = cursor.fetchone()
        return result

    def update_food(self, food_category, food_quantity, food_type, f_id):
        cursor = self.cnx.cursor()
        ##add check to verify if the resource even exists.
        query = "update food set food_category=%s, food_quantity=%s, food_type=%s where food_id=%s "
        cursor.execute(query, (food_category, food_quantity, food_type, f_id,))
        self.cnx.commit()
        return f_id
    