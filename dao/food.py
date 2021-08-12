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
        query = "select resource_id, food_category, food_quantity, food_type from food "
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_food_by_id(self, f_id):
        cursor = self.cnx.cursor()
        query = "select resource_id, food_category, food_quantity, food_type from food where food_id = %s "
        cursor.execute(query, (f_id,))
        result = cursor.fetchone()
        return result

    def insert_food(self, r_id, food_category, food_quantity, food_type):
        cursor = self.cnx.cursor()
        query = "insert into food (resource_id, food_category, food_quantity, food_type) values (%s,%s,%s,%s)"
        cursor.execute(query, (r_id, food_category, food_quantity, food_type,))
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        food_id = cursor.fetchone()[0]
        self.cnx.commit()
        return food_id

    def update_food(self, food_category, food_quantity, food_type, f_id):
        cursor = self.cnx.cursor()
        query = "update food set food_category=%s, food_quantity=%s, food_type=%s where food_id=%s "
        cursor.execute(query, (food_category, food_quantity, food_type, f_id,))
        self.cnx.commit()
        return f_id
    
    def delete_food(self, f_id):
        cursor = self.cnx.cursor()
        query =  "delete from food where food_id = %s;"
        cursor.execute(query, (f_id,))
        food_id = cursor.fetchone()[0]
        self.cnx.commit()
        return food_id
    