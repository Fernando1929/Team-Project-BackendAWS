from db_config.dbconfig import mysql_config
import mysql.connector

class CredentialsDAO:

    def __init__ (self):
        self.cnx = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])

    def insert(self, user_id, username, password):
        cursor = self.cnx.cursor()
        query = "INSERT INTO credentials (user_id, username, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, username, password))
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        cred_id = cursor.fetchone()[0]
        self.cnx.commit()
        return cred_id

    def update(self, cred_id, username, password, user_id):
        cursor = self.cnx.cursor()
        query = "UPDATE credentials SET user_id = %s, username = %s, password = %s WHERE cred_id = %s"
        cursor.execute(query, (user_id, username, password, cred_id))
        self.cnx.commit()
        return cred_id

    def getCredentialsById(self, cred_id):
        cursor = self.cnx.cursor()
        query = "SELECT * FROM credentials WHERE cred_id = %s"
        cursor.execute(query,(cred_id,))
        result =  cursor.fetchone()
        return result
        
    def getCredentialsByUserId(self, user_id):
        cursor = self.cnx.cursor()
        query = "SELECT cred_id, username, password, user_id FROM credentials NATURAL JOIN users WHERE user_id = %s"
        cursor.execute(query,(user_id,))
        result =  cursor.fetchone()
        print(result)
        return result

    def delete(self, user_id):
        cursor =  self.cnx.cursor()
        query =  "DELETE FROM users WHERE user_id = %s returning user_id"
        cursor.execute(query, (user_id,))
        self.cnx.commit()
        return user_id