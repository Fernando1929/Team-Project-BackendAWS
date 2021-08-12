from db_config.dbconfig import mysql_config
import mysql.connector

class SurvivorDAO:
    
    def __init__(self):
        self.cnx = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])


    def getAllSurvivors(self):
        cursor = self.cnx.cursor()
        query = "select  user_id, survivor_id, user_firstname, user_lastname, user_date_birth from users natural join survivor"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSurvivorById(self, survivor_id):
        cursor = self.cnx.cursor()
        query = "select user_id, survivor_id, user_firstname, user_lastname, user_date_birth from survivor natural join users where survivor_id = %s;"
        cursor.execute(query, (survivor_id,))
        result = cursor.fetchone()
        return result

    def getSurvivorByFirstname(self, survivor_firstname):
        cursor = self.cnx.cursor()
        query = "select user_id, survivor_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from survivor natural inner join users natural inner join user_phone where user_firstname = %s;"
        cursor.execute(query, (survivor_firstname,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSurvivorByLastname(self, survivor_lastname):
        cursor = self.cnx.cursor()
        query = "select user_id, survivor_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from survivor natural inner join users natural inner join user_phone where user_lastname = %s;"
        cursor.execute(query, (survivor_lastname,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSurvivorByFirstnameAndLastname(self, survivor_firstname, survivor_lastname):
        cursor = self.cnx.cursor()
        query = "select user_id, survivor_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from survivor natural inner join users where user_firstname = %s and user_lastname = %s;"
        cursor.execute(query, (survivor_firstname, survivor_lastname))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSurvivorByDateOfBirth(self, survivor_date_birth):
        cursor = self.cnx.cursor()
        query = "select user_id, survivor_id, user_firstname, user_lastname, user_date_birth, user_email, phone_id, user_phone from survivor natural inner join users where user_date_birth = %s;"
        cursor.execute(query, (survivor_date_birth,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, user_id):
        cursor = self.cnx.cursor()
        query = "insert into survivor(user_id) values (%s) returning survivorid;"
        cursor.execute(query, (user_id,))
        survivor_id = cursor.fetchone()[0]
        self.cnx.commit()
        return survivor_id

    # There is nothing to update in survivor table. We only need to get the user id to do the update.
    def update(self, survivor_id):
        cursor = self.cnx.cursor()
        query = "select user_id from survivor where survivor_id = %s;"
        cursor.execute(query, (survivor_id,))
        user_id = cursor.fetchone()[0]
        self.cnx.commit()
        return user_id

    def delete(self, survivor_id):
        cursor = self.cnx.cursor()
        query = "delete from survivor where survivor_id = %s returning user_id;"
        cursor.execute(query,(survivor_id,))
        user_id = cursor.fetchone()[0]
        self.cnx.commit()
        return user_id