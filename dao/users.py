from db_config.dbconfig import mysql_config
import mysql.connector

class UserDAO:

    def __init__ (self):
        self.cnx = mysql.connector.connect(
                            user = mysql_config['DB_USERNAME'], 
                            password = mysql_config['DB_PASSWORD'],
                            host = mysql_config['DB_WEBSERVER'],
                            database = mysql_config['DB_DATABASE'])

    def insert(self, user_id, username, password):
        cursor = self.cnx.cursor()
        query = "insert into users(user_firstname, user_lastname, user_date_birth, user_email) values (%s, %s, %s, %s) returning user_id"
        cursor.execute(query, (user_id, username, password))
        login_id = cursor.fetchone()[0]
        self.conn.commit()
        return login_id

    def update(self, user_id):
        cursor = self.cnx.cursor()
        query = "update users set user_firstname = %s, user_lastname = %s, user_date_birth = %s, user_email = %s where user_id = %s returning user_id"
        cursor.execute(query, (user_id, username, password, login_id,))
        login_id = cursor.fetchone()[0]
        self.conn.commit()
        return login_id

    def getUserById(self, user_id):
        cursor = self.cnx.cursor()
        query = "select user_id, user_firstname, user_lastname, user_date_birth from users where user_id = %s"
        cursor.execute(query,(user_id,))
        result =  cursor.fetchone()
        return result

    def delete(self, user_id):
        cursor =  self.cnx.cursor()
        query = "delete from users where user_id = %s returning user_id"
        cursor.execute(query, (user_id,))
        self.conn.commit()
        return user_id