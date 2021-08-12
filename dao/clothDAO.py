from db_config.dbconfig import mysql_config
import mysql.connector


class ClothDAO:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = mysql_config['DB_USERNAME'], 
            password = mysql_config['DB_PASSWORD'], 
            host = mysql_config['DB_WEBSERVER'], 
            database = mysql_config['DB_DATABASE']
        )

    def get_all_cloth(self):
        cursor = self.cnx.cursor()
        query = "select cloth_type, cloth_quantity from cloth "
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_cloth_by_id(self, c_id):
        cursor = self.cnx.cursor()
        query = "select cloth_type, cloth_quantity from cloth where cloth_id = %s "
        cursor.execute(query, (c_id,))
        result = cursor.fetchone()
        return result

    def insert_cloth(self, r_id, cloth_category, cloth_quantity, cloth_type):
        cursor = self.cnx.cursor()
        query = "insert into cloth (resource_id, cloth_category, cloth_quantity, cloth_type) values (%s,%s,%s,%s) "
        cursor.execute(query, (r_id, cloth_category, cloth_quantity, cloth_type,))
        cloth_id = cursor.fetchone()[0]
        self.cnx.commit()
        return cloth_id

    def change_cloth_quantity(self, cloth_quantity, c_id):
        cursor = self.cnx.cursor()
        ##add check to verify if the resource even exists.
        query = "update cloth set cloth_quantity=%s where cloth_id=%s "
        cursor.execute(query, (cloth_quantity, c_id))
        self.cnx.commit()
        return c_id

    def get_cloth_quantity(self, c_id):
        cursor = self.cnx.cursor()
        query = "select cloth_quantity from cloth where cloth_id = %s "
        cursor.execute(query, (c_id,))
        result = cursor.fetchone()
        return result
    
    def update_cloth(self, cloth_type, cloth_quantity, c_id):
        cursor = self.cnx.cursor()
        query = "update cloth set cloth_type=%s, cloth_quantity=%s where cloth_id=%s "
        cursor.execute(query, cloth_type, cloth_quantity, c_id)
        self.cnx.commit()
        return c_id