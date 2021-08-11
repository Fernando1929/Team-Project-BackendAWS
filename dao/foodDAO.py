from db_config.dbconfig import mysql_config
import psycopg2


class FoodDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (
            pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("connection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def get_all_food(self):
        cursor = self.conn.cursor()
        query = "select food_category, food_quantity, food_type from food;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_food_by_id(self, f_id):
        cursor = self.conn.cursor()
        query = "select food_category, food_quantity, food_type from food where food_id = %s;"
        cursor.execute(query, (f_id,))
        result = cursor.fetchone()
        return result

    def insert_food(self, r_id, food_category, food_quantity, food_type):
        cursor = self.conn.cursor()
        query = "insert into food (resource_id, food_category, food_quantity, food_type) values (%s,%s,%s,%s) returning food_id;"
        cursor.execute(query, (r_id, food_category, food_quantity, food_type,))
        food_id = cursor.fetchone()[0]
        self.conn.commit()
        return food_id

    def change_food_quantity(self, food_quantity, f_id):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "update food set food_quantity=%s where food_id=%s;"
        cursor.execute(query, (food_quantity, f_id,))
        self.conn.commit()
        return f_id

    def get_food_quantity(self, f_id):
        cursor = self.conn.cursor()
        query = "select food_quantity from food where food_id = %s;"
        cursor.execute(query, (f_id,))
        result = cursor.fetchone()
        return result
    