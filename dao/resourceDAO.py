from db_config.dbconfig import mysql_config
import mysql.connector


class ResourceDAO:
   def __init__ (self):
        self.conn = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])

    def get_all_resources(self):
        cursor = self.conn.cursor()
        query = "select * from resources;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_resource_by_id(self, r_id):
        cursor = self.conn.cursor()
        query = "select * from resources where resource_id = %s;"
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    def insert_resource(self, r_name, r_availability):
        cursor = self.conn.cursor()
        query = "insert into resources (resource_name, resource_availability) values (%s,%s) returning resource_id;"
        cursor.execute(query, (r_name, r_availability,))
        resource_id = cursor.fetchone()[0]
        self.conn.commit()
        return resource_id

    def change_resource_availability(self, r_availability, r_id):
        cursor = self.conn.cursor()
        ##add check to verify if the resource even exists.
        query = "update resources set resource_availability=%s where resource_id=%s;"
        cursor.execute(query, (r_availability, r_id))
        self.conn.commit()
        return r_id

    def delete_resource(self, r_id):
        cursor = self.conn.cursor()
        query =  "delete from resources where resource_id = %s returning resource_id;"
        cursor.execute(query, (r_id,))
        resource_id = cursor.fetchone()[0]
        self.conn.commit()
        return resource_id
    