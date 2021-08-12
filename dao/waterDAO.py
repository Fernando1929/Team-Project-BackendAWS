from db_config.dbconfig import mysql_config
import psycopg2


class WaterDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (
            pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("connection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def get_all_water(self):
        cursor = self.conn.cursor()
        query = "select water_quantity, water_container, water_type from water;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_water_by_id(self, w_id):
        cursor = self.conn.cursor()
        query = "select water_quantity, water_container, water_type from water where water_id = %s;"
        cursor.execute(query, (w_id,))
        result = cursor.fetchone()
        return result

    def insert_water(self, r_id, water_quantity, water_container, water_type):
        cursor = self.conn.cursor()
        ##check if water already exists
        query = "insert into water (resource_id, water_quantity, water_container, water_type) values (%s,%s,%s,%s) returning water_id;"
        cursor.execute(query, (r_name, r_availability,))
        water_id = cursor.fetchone()[0]
        self.conn.commit()
        return water_id

    def change_water_quantity(self, (r_id, water_type, water_quantity,)):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "update water set water_quantity=%s where water_id=%s;"
        cursor.execute(query, (water_quantity, w_id,))
        self.conn.commit()
        return w_id
    
    def get_water_by_type(self, water_type):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "select * from water where water_type=%s;"
        cursor.execute(query, (water_type,))
        result = cursor.fetchone()
        return result
    