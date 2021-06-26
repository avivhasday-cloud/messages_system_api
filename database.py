import mysql.connector as mysql
import os
from dotenv import load_dotenv
from pathlib import Path  


# set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



class DataBase(object):
    def __init__(self):
        try:
            self.connection = mysql.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USERNAME'),
                passwd=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('DB')
            )
            print('connection established')
            self.cursor = self.connection.cursor()
        except mysql.Error as err:
            print(err.msg)

    def close_connection(self):
        self.connection.Close()

    def create_user(self, username, email, password):
        try:
            query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s);"
            params = (username, email, password)       
            self.cursor.execute(query, params)
            self.connection.commit()
            return {"Message": "User created"}

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}

    def get_user(self, username):
        try:
            query = "SELECT * FROM Users WHERE username=%s"
            params = (username,)       
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            if not result:
                return None
            user_object = {
                "id": result[0],
                "username": result[1],
                "email": result[2],
                "password":result[3]
            }
            return user_object

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}
    
    def get_all_messages_for_user(self, user_id):
        try:
            query = """SELECT * FROM Messages WHERE user_id=%s;"""
            params = (user_id,)
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            columns = [col[0] for col in self.cursor.description]
            output = []
            for row in result:
                message = dict(zip(columns, row))
                output.append(message)
            return {"data": output}

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}

    def get_all_unread_messages_for_user(self, user_id):
        try:
            query = """SELECT * FROM Messages WHERE user_id=%s AND read_status=0;"""
            params = (user_id,)
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            columns = [col[0] for col in self.cursor.description]

            output = []
            for row in result:
                message = dict(zip(columns, row))
                output.append(message)
            return {"data": output}

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}


    def write_message(self, data, user_id):
        try:
            query = """INSERT INTO Messages (user_id, sender, receiver, subject, content) 
                     VALUES (%s, %s, %s, %s, %s);"""
            params = (user_id, data['sender'], data['receiver'], data['subject'], data['content'])       
            self.cursor.execute(query, params)
            self.connection.commit()
            
            return {"Message": "Message sent!"}

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}


    def read_message(self, id):
        try:
            query = """UPDATE Messages SET read_status=1 WHERE id =%s;"""
            params = (id,)       
            self.cursor.execute(query, params)
            self.connection.commit()
            updated_row = self.get_message(id)
            return {"Data": updated_row}
            

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}

    def get_message(self, id):
        try:
            query = """SELECT * FROM Messages WHERE id=%s"""
            params = (id,)       
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            columns = [col[0] for col in self.cursor.description]
            message = dict(zip(columns, result))
            return message

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}


    def delete_message(self, id, user_id):
        try:
            query = """DELETE FROM Messages WHERE id=%s AND sender=(SELECT username FROM Users WHERE id=%s);"""
            params = (id,user_id)       
            self.cursor.execute(query, params)
            self.connection.commit()
            return {"Message": "Message deleted"}

        except mysql.Error as err:
            print(err.msg)
            return {"Message": "General Error"}



               

