from db_config.dbconfig import mysql_config
import psycopg2


class FuelDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (
            pg_config['dbname'], pg_config['user'], pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("connection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

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
    