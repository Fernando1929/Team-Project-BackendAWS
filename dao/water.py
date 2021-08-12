from db_config.dbconfig import mysql_config
import mysql.connector


class WaterDAO:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = mysql_config['DB_USERNAME'], 
            password = mysql_config['DB_PASSWORD'], 
            host = mysql_config['DB_WEBSERVER'], 
            database = mysql_config['DB_DATABASE']
        )

    def get_all_water(self):
        cursor = self.cnx.cursor()
        query = "select water_quantity, water_container, water_type from water"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_water_by_id(self, w_id):
        cursor = self.cnx.cursor()
        query = "select water_quantity, water_container, water_type from water where water_id = %s"
        cursor.execute(query, (w_id,))
        result = cursor.fetchone()
        return result

    def insert_water(self, r_id, water_quantity, water_container, water_type):
        cursor = self.cnx.cursor()
        ##check if water already exists
        query = "insert into water (resource_id, water_quantity, water_container, water_type) values (%s,%s,%s,%s)"
        cursor.execute(query, (r_id, water_quantity, water_container, water_type))
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        water_id = cursor.fetchone()[0]
        self.cnx.commit()
        return water_id

    def update_water(self, w_id, water_quantity, water_container, water_type):
        cursor = self.cnx.cursor()
        ##add check to verify if the resource even exists.
        query = "update water set water_quantity=%s, water_container=%s, water_type=%s where water_id=%s"
        cursor.execute(query, (water_quantity, water_container, water_type, w_id,))
        self.cnx.commit()
        return w_id
    
    def get_water_by_type(self, water_type):
        cursor = self.cnx.cursor()
        ##add check to verify if the resource even exists.
        query = "select * from water where water_type=%s"
        cursor.execute(query, (water_type,))
        result = cursor.fetchone()
        return result
    