import pymysql
import datetime
import hashlib
import sqlite3

class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
             user='mytwits_user',
             passwd='mytwits_password',
             db='mytwits')
    def get_user(self, user_id):
        query = "select * from users where user_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query,user_id)
            return  cursor.fetchone()


    def get_all_twits(self):
        query = "select u.username, t.twit_id, t.twit, t.created_at from twits t, users u where t.user_id=u.user_id order by t.created_at desc;"
        with self.db.cursor(pymysql.cursors.DictCursor) as cursor:
             cursor.execute(query)
             return cursor.fetchall()  # The method fetches all (or all remaining)rows of a query result set and returns a list of tuples

    def get_twit(self,twit_id):
        query = "select twit_id, twit, created_at from twits where twit_id=%s"
        with self.db.cursor(pymysql.cursors.DictCursor) as cursor:
             cursor.execute(query, twit_id)
             return cursor.fetchone()
             # more detals about cursor.fetchone at
             # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html

    def get_user_twits(self,username):
        query = "select u.username, t.twit, t.created_at from twits t,\
        users u where t.user_id=u.user_id and u.username=% order by t.created_at desc;"
        with self.db.cursor() as cursor:
             cursor.execute(query,(username))
             return cursor.fetchall()

    def add_twit(self,twit,user_id):
        query = "insert into twits (twit,user_id) values \
        (%s,%s);"
        with self.db.cursor() as cursor:
            cursor.execute(query, (twit,user_id))
            return self.db.commit()

    def update_twit(self,twit,twit_id):
        query = "update twits set twit=%s where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query,(twit,twit_id))
            return self.db.commit()

    def delete_twit(self,twit_id):
        query = "delete from twits where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, twit_id)
            return self.db.commit()

    def add_user(self,username,password,salt,hashed,email):
        query = "insert into users (username,password,salt,hashed,email) values \
        (%s,%s,%s,%s,%s);"
        with self.db.cursor() as cursor:
             cursor.execute(query, (username, password, salt, hashed, email))
        return self.db.commit()

    def rowcount(self):
        query = "select * from twits"
        with self.db.cursor() as cursor:
            return cursor.execute(query)
    
    def add_file(self,filename,data,user_id):
        query = "update users set filename=%s where user_id=%s;"
        query2 = "update users set data=%s where user_id=%s;"
        with self.db.cursor() as cursor:
             cursor.execute(query, (filename,user_id))
             cursor.execute(query2, (data,user_id))
             return self.db.commit()

    def get_file(self,user_id):
        query = "select data from users where user_id=%s;"
        with self.db.cursor() as cursor:
             cursor.execute(query, user_id)
             return cursor.fetchone()[0]
    
    def get_filename(self,user_id):
        query = "select filename from users where user_id=%s;"
        with self.db.cursor() as cursor:
             cursor.execute(query, user_id)
             return cursor.fetchone()

    def check_password(self,username,password):
         query = "select user_id, salt, hashed from users where username = %s;"
         with self.db.cursor() as cursor:
            cursor.execute(query,(username))
            user = cursor.fetchone()
            if user:
                user_id, salt, hashed = user
                if hashlib.sha512((salt + password).encode('utf-8')).hexdigest()== hashed:
                    return user_id
            return None

db = DBHelper()

