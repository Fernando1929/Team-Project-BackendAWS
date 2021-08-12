from db_config.dbconfig import mysql_config
import mysql.connector



class MedicineDAO:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = mysql_config['DB_USERNAME'], 
            password = mysql_config['DB_PASSWORD'], 
            host = mysql_config['DB_WEBSERVER'], 
            database = mysql_config['DB_DATABASE']
        )

    def get_all_medicine(self):
        cursor = self.cnx.cursor()
        query = "select resource_id, med_type, med_quantity from medicine;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_medicine_by_id(self, m_id):
        cursor = self.cnx.cursor()
        query = "select resource_id, med_type, med_quantity from medicine where med_id = %s "
        cursor.execute(query, (m_id,))
        result = cursor.fetchone()
        return result

    def insert_medicine(self, r_id, medicine_type, medicine_quantity):
        cursor = self.cnx.cursor()
        query = "insert into medicine (resource_id, med_type, med_quantity) values (%s,%s,%s) "
        cursor.execute(query, (r_id, medicine_type, medicine_quantity,))
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        med_id = cursor.fetchone()[0]
        self.cnx.commit()
        return med_id

    def update_medicine(self, medicine_type, medicine_quantity, m_id):
        cursor = self.cnx.cursor()
        query = "update medicine set med_type=%s, med_quantity=%s where med_id=%s "
        cursor.execute(query, (medicine_type, medicine_quantity, m_id))
        self.cnx.commit()
        return m_id
    
    def delete_medicine(self, m_id):
        cursor = self.cnx.cursor()
        query =  "delete from medicine where med_id = %s returning med_id;"
        cursor.execute(query, (m_id,))
        med_id = cursor.fetchone()[0]
        self.cnx.commit()
        return med_id
    