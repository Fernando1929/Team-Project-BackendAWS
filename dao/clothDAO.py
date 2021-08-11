from db_config.dbconfig import mysql_config
import psycopg2


class ClothDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (
            pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("connection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def get_all_cloth(self):
        cursor = self.conn.cursor()
        query = "select cloth_type, cloth_quantity from cloth;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_cloth_by_id(self, c_id):
        cursor = self.conn.cursor()
        query = "select cloth_type, cloth_quantity from cloth where cloth_id = %s;"
        cursor.execute(query, (c_id,))
        result = cursor.fetchone()
        return result

    def insert_cloth(self, r_id, cloth_category, cloth_quantity, cloth_type):
        cursor = self.conn.cursor()
        query = "insert into cloth (resource_id, cloth_category, cloth_quantity, cloth_type) values (%s,%s,%s,%s) returning cloth_id;"
        cursor.execute(query, (r_id, cloth_category, cloth_quantity, cloth_type,))
        cloth_id = cursor.fetchone()[0]
        self.conn.commit()
        return cloth_id

    def change_cloth_quantity(self, cloth_quantity, c_id):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "update cloth set cloth_quantity=%s where cloth_id=%s;"
        cursor.execute(query, (cloth_quantity, c_id))
        self.conn.commit()
        return c_id

    def get_cloth_quantity(self, c_id):
        cursor = self.conn.cursor()
        query = "select cloth_quantity from cloth where cloth_id = %s;"
        cursor.execute(query, (c_id,))
        result = cursor.fetchone()
        return result
    