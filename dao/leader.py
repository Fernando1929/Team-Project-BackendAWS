from db_config.dbconfig import mysql_config
import mysql.connector

class LeaderDAO:
    
    def __init__(self):
        self.cnx = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])


    def getAllLeaders(self):
        cursor = self.cnx.cursor()
        query = "select user_id, leader_id, user_firstname, user_lastname, user_date_birth from users natural join faction_leader"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getLeaderById(self, leader_id):
        cursor = self.cnx.cursor()
        query = "select user_id, leader_id, user_firstname, user_lastname, user_date_birth from users natural join faction_leader where leader_id = %s"
        cursor.execute(query, (leader_id,))
        result = cursor.fetchone()
        return result

    def getAllLeaderResources(self, Leader_id):
        cursor = self.cnx.cursor()
        query = "select resource_id, Leader_id, category_id, resource_name, resource_brand, resource_quantity, resource_price from resource where Leader_id = %s"
        cursor.execute(query, (Leader_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getLeadersByFirstnameAndLastname(self,Leader_firstname, Leader_lastname):
        cursor = self.cnx.cursor()
        query = "select user_id, Leader_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from Leader natural inner join users natural inner join user_phone where user_firstname = %s and user_lastname = %s"
        cursor.execute(query, (Leader_firstname, Leader_lastname))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getLeadersByFirstname(self,Leader_firstname):
        cursor = self.cnx.cursor()
        query = "select user_id, Leader_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from Leader natural inner join users natural inner join user_phone where user_firstname = %s"
        cursor.execute(query, (Leader_firstname,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getLeadersByLastname(self,Leader_lastname):
        cursor = self.cnx.cursor()
        query = "select user_id, Leader_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from Leader natural inner join users natural inner join user_phone where user_lastname = %s"
        cursor.execute(query, (Leader_lastname,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getLeadersByDateOfBirth(self,Leader_date_birth):
        cursor = self.cnx.cursor()
        query = "select user_id, Leader_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from Leader natural inner join users natural inner join user_phone where user_date_birth = %s"
        cursor.execute(query, (Leader_date_birth,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getLeadersByCompanyId(self, company_id):
        cursor = self.cnx.cursor()
        query = "select user_id, Leader_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from Leader natural inner join users natural inner join user_phone natural inner join represents WHERE company_id = %s"
        cursor.execute(query, (company_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, user_id):
        cursor = self.cnx.cursor()
        query = "insert into Leader(user_id) values (%s) returning Leader_id"
        cursor.execute(query, (user_id,))
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        leader_id = cursor.fetchone()[0]
        self.cnx.commit()
        return leader_id

    # There is nothing to update in customer table. We only need to get the user id to do the update.
    def update(self, Leader_id):
        cursor = self.cnx.cursor()
        query = "select user_id from Leader where Leader_id = %s"
        cursor.execute(query, (Leader_id,))
        user_id = cursor.fetchone()[0]
        self.cnx.commit()
        return user_id

    def delete(self, Leader_id):
        cursor = self.cnx.cursor()
        query = "delete from Leader where Leader_id = %s returning user_id"
        cursor.execute(query,(Leader_id,))
        user_id = cursor.fetchone()[0]
        self.cnx.commit()
        return user_id