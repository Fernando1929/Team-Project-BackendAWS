from db_config.dbconfig import mysql_config
import psycopg2


class MedicineDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (
            pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("connection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def get_all_medicine(self):
        cursor = self.conn.cursor()
        query = "select med_type, med_quantity from medicine;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_medicine_by_id(self, m_id):
        cursor = self.conn.cursor()
        query = "select med_type, med_quantity from medicine where med_id = %s;"
        cursor.execute(query, (m_id,))
        result = cursor.fetchone()
        return result

    def insert_medicine(self, r_id, medicine_type, medicine_quantity):
        cursor = self.conn.cursor()
        ##check if medicine already exists
        query = "insert into medicine (resource_id, med_type, med_quantity) values (%s,%s,%s) returning med_id;"
        cursor.execute(query, (r_id, medicine_type, medicine_quantity,))
        med_id = cursor.fetchone()[0]
        self.conn.commit()
        return med_id

    def change_medicine_quantity(self, medicine_quantity. m_id):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "update medicine set med_quantity=%s where med_id=%s;"
        cursor.execute(query, (medicine_quantity, m_id,))
        self.conn.commit()
        return m_id
    
    def get_medicine_by_type(self, medicine_type):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "select * from medicine where med_type=%s;"
        cursor.execute(query, (medicine_type,))
        result = cursor.fetchone()
        return result
    