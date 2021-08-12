from db_config.dbconfig import mysql_config
import mysql.connector


class FuelDAO:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = mysql_config['DB_USERNAME'], 
            password = mysql_config['DB_PASSWORD'], 
            host = mysql_config['DB_WEBSERVER'], 
            database = mysql_config['DB_DATABASE']
        )

    def get_all_fuel(self):
        cursor = self.cnx.cursor()
        query = "select resource_id, fuel_type, fuel_quantity from fuel "
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_fuel_by_id(self, f_id):
        cursor = self.cnx.cursor()
        query = "select resource_id, fuel_type, fuel_quantity from fuel where fuel_id = %s "
        cursor.execute(query, (f_id,))
        result = cursor.fetchone()
        return result

    def insert_fuel(self, r_id, fuel_type, fuel_quantity):
        cursor = self.cnx.cursor()
        query = "insert into fuel (resource_id, fuel_type, fuel_quantity) values (%s,%s,%s) "
        cursor.execute(query, (r_id, fuel_type, fuel_quantity,))
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        fuel_id = cursor.fetchone()[0]
        self.cnx.commit()
        return fuel_id

    def update_fuel(self, fuel_type, fuel_quantity, f_id):
        cursor = self.cnx.cursor()
        query = "update fuel set fuel_type=%s, fuel_quantity=%s where fuel_id=%s "
        cursor.execute(query, (fuel_type, fuel_quantity, f_id))
        self.cnx.commit()
        return f_id
    
    def delete_fuel(self, f_id):
        cursor = self.cnx.cursor()
        query =  "delete from fuel where fuel_id = %s returning fuel_id;"
        cursor.execute(query, (f_id,))
        fuel_id = cursor.fetchone()[0]
        self.cnx.commit()
        return fuel_id
    