from db_config.dbconfig import mysql_config
import mysql.connector

class LocationDAO:

    # location_id, user_id, city, state_province
    def __init__(self):
        self.cnx = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])

    def getAllLocations(self):
        cursor = self.cnx.cursor()
        query = "SELECT location_id, user_id, city, state_province FROM locations"
        cursor.execute(query)
        result = []
        
        for row in cursor:
            result.append(row)
        print(result)
        return result

    def getLocationById(self, location_id):
        cursor = self.cnx.cursor()
        query = "SELECT location_id, user_id, city, state_province FROM locations where location_id = %s"
        cursor.execute(query, (location_id,))
        result = cursor.fetchone()
        return result

    def getLocationByUserId(self, user_id):
        cursor = self.cnx.cursor()
        query = "SELECT location_id, user_id, city, state_province FROM locations WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def insert(self, user_id, addressline, city, state_province, country, zipcode):
        cursor = self.cnx.cursor()
        query = "INSERT INTO address (user_id, addressline, city, state_province, country, zipcode) VALUES (%s, %s, %s, %s, %s, %s) RETURNING address_id"
        cursor.execute(query, (user_id, addressline, city, state_province, country, zipcode))
        address_id = cursor.fetchone()[0]
        self.cnx.commit()
        return address_id

    def update(self, address_id, user_id, addressline, city, state_province, country, zipcode):
        cursor = self.cnx.cursor()
        query = "update address set user_id = %s, addressline = %s, city = %s, state_province = %s, country = %s, zipcode = %s where address_id = %s"
        cursor.execute(query, (user_id, addressline, city, state_province, country, zipcode, address_id,))
        self.cnx.commit()
        return address_id

    def delete(self, address_id):
        cursor = self.cnx.cursor()
        query = "delete from address where address_id = %s"
        cursor.execute(query, (address_id,))
        self.cnx.commit()
        return address_id