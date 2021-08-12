from db_config.dbconfig import mysql_config
import mysql.connector


class resourceDAO:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = mysql_config['DB_USERNAME'], 
            password = mysql_config['DB_PASSWORD'], 
            host = mysql_config['DB_WEBSERVER'], 
            database = mysql_config['DB_DATABASE']
        )

    def get_all_resources(self):
        cursor = self.cnx.cursor()
        query = "select resource_name, resource_availability from resources "
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_resource_by_id(self, r_id):
        cursor = self.cnx.cursor()
        query = "select resource_name, resource_availability from resources where resource_id = %s "
        cursor.execute(query, (r_id,))
        result = cursor.fetchone()
        return result

    def insert_resource(self, resource_name, resource_availability):
        cursor = self.cnx.cursor()
        query = "insert into resources (resource_name, resource_availability) values (%s,%s) "
        cursor.execute(query, (resource_name, resource_availability))
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        res_id = cursor.fetchone()[0]
        self.cnx.commit()
        return res_id

    def update_resource(self, resource_name, resource_availability, r_id):
        cursor = self.cnx.cursor()
        ##add check to verify if the resource even exists.
        query = "update resources set resource_name=%s, resource_availability=%s where resource_id=%s "
        cursor.execute(query, (resource_name, resource_availability, r_id))
        self.cnx.commit()
        return r_id
    