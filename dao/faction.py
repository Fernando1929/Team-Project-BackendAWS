from db_config.dbconfig import mysql_config
import mysql.connector

class FactionsDAO:
    
    # faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory 
    def __init__(self):
        self.cnx = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])
    
    def getAllFactions(self): #Done
        cursor = self.cnx.cursor()
        query = "Select faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory from faction"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getFactionById(self, faction_id): #Done
        cursor = self.cnx.cursor()
        query = "Select faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory from faction where faction_id = %s"
        cursor.execute(query,(faction_id,))
        result = cursor.fetchone()
        return result

    def getFactionByName(self, faction_name):
        cursor = self.cnx.cursor()
        query = "Select faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory where faction_name = %s"
        cursor.execute(query,(faction_name,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getFactionByAddress(self, faction_address):
        cursor = self.cnx.cursor()
        query = "Select faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory where faction_address = %s"
        cursor.execute(query,(faction_address,))
        result = []
        for row in cursor:
            result.append(row)
        return result


    def getFactionByLeaderId(self, leader_id):
        cursor = self.cnx.cursor()
        query = "Select faction_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory, leader_id from faction Natural Join faction_leader where leader_id = %s"
        cursor.execute(query,(leader_id,))
        result = cursor.fetchone()
        return result

    def insert(self, leader_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory):
        cursor = self.cnx.cursor()
        query = "insert into faction (leader_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory) values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(leader_id, faction_name, faction_population, faction_rating, faction_wealth, faction_territory,))
        query = "SELECT LAST_INSERT_ID()" 
        cursor.execute(query)
        faction_id = cursor.fetchone()[0]
        self.cnx.commit()
        return faction_id

    def update(self, faction_id, faction_name, faction_address, faction_phone):
        cursor = self.cnx.cursor()
        query = "update faction set faction_name = %s, faction_address = %s, faction_phone = %s where faction_id = %s"
        cursor.execute(query,(faction_name, faction_address, faction_phone,faction_id))
        self.cnx.commit()
        return faction_id

    def delete(self, faction_id):
        cursor = self.cnx.cursor()
        query = "delete from faction where faction_id = %s"
        cursor.execute(query,(faction_id,))
        self.cnx.commit()
        return faction_id