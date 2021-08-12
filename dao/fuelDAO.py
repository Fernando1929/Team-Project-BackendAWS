from db_config.dbconfig import mysql_config
import mysql.connector


class FuelDAO:
    def __init__ (self):
        self.conn = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])

    def get_all_fuel(self):
        cursor = self.conn.cursor()
        query = "select fuel_type, fuel_quantity from fuel;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_fuel_by_id(self, f_id):
        cursor = self.conn.cursor()
        query = "select fuel_type, fuel_quantity from fuel where fuel_id = %s;"
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    def insert_fuel(self, r_id, fuel_type, fuel_quantity):
        cursor = self.conn.cursor()
        ##check if fuel already exists
        query = "insert into fuel (resource_id, fuel_type, fuel_quantity) values (%s,%s,%s,%s) returning fuel_id;"
        cursor.execute(query, (r_name, r_availability,))
        fuel_id = cursor.fetchone()[0]
        self.conn.commit()
        return fuel_id

    def change_fuel_quantity(self, (r_id, fuel_type, fuel_quantity,)):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "update fuel set fuel_quantity=%s where fuel_id=%s returning fuel_id;"
        cursor.execute(query, (fuel_quantity, f_id,))
        self.conn.commit()
        return f_id
    
    def get_fuel_quantity(self, f_id):
        cursor = self.conn.cursor()
        query = "select fuel_quantity from fuel where fuel_id = %s;"
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    def delete_fuel(self, f_id):
        cursor = self.conn.cursor()
        query =  "delete from fuel where fuel_id = %s returning fuel_id;"
        cursor.execute(query, (f_id,))
        fuel_id = cursor.fetchone()[0]
        self.conn.commit()
        return fuel_id
    