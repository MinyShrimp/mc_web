# -*- coding: utf-8 -*-

import pymysql
import re

def is_db_regular(_str):
    p = re.compile('SELECT|UPDATE|UNION|DELETE|INSERT|WHERE|HAVING', re.I)
    return p.search(_str) == None 

def is_spc_regular(_str):
    p = re.compile('[~!@#$%^&*()_+|<>?:{}]')
    return p.search(_str) == None 

def is_regular(_str):
    return ( is_db_regular(_str) and is_spc_regular(_str) )

class DB_SQL():
    def __init__(self):
        self.db = pymysql.connect(
            host= '34.80.56.3',
            port=3306,
            user='root',
            passwd='****',
            db='MINECRAFT',
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    def __del__(self):
        self.db.close()
    
    def get_count_table(self, table):
        if is_regular(table):
            sql = """SELECT COUNT(*) FROM {} WHERE IsDelete=FALSE;""".format(table)
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            raise TypeError
    
    def delete_forum(self, id):
        if is_regular(id):
            sql = """UPDATE Forum SET IsDelete=TRUE WHERE ID={};""".format(id)
            self.cursor.execute(sql)
            self.db.commit()
        else:
            raise TypeError
    
    def select_table(self, table, selects, where):
        if is_regular(table) and is_regular(selects) and is_regular(where):
            sql = """SELECT {} FROM {} WHERE {};""".format()
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            raise TypeError
        
    def select_page(self, table, page):
        print(table, is_regular(table), is_db_regular(table), is_spc_regular(table))
        if is_regular(table):
            sql = """SELECT ID, Name, Title, Date, View FROM {} WHERE IsDelete=FALSE ORDER BY ID desc LIMIT {}, {};""".format( table, 10 * (page - 1), 10 * page - 1 )
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            raise TypeError

    def update_forum(self, id, name, title, date, contents, pw):
        for _ in [id, name, title, date, contents, pw]:
            if not is_regular(_):
                raise TypeError
        else:
            sql = """UPDATE Forum SET Name='{}', Title='{}', Date='{}', Contents='{}', PW='{}' WHERE ID='{}';""".format(name, title, date, contents, pw, id)
            self.cursor.execute(sql)
            self.db.commit()

    def insert_user(self, uid, pw, email, nickname, m_nickname):
        for _ in [uid, pw, email, nickname, m_nickname]:
            if not is_regular(_):
                raise TypeError
        else:
            sql = """INSERT INTO User(uID, PW, Email, Nickname, mNickname) VALUES('{}', '{}', '{}', '{}', '{}');""".format(uid, pw, email, nickname, m_nickname)
            self.cursor.execute(sql)
            self.db.commit()
    
    def insert_forum(self, name, title, date, contents, pw):
        for _ in [name, title, date, contents, pw]:
            if not is_regular(_):
                raise TypeError
        else:
            sql = """INSERT INTO Forum(Name, Title, Date, Contents, PW, View, IsDelete) VALUES('{}', '{}', '{}', '{}', '{}', 0, FALSE);""".format(name, title, date, contents, pw)
            self.cursor.execute(sql)
            self.db.commit()

    def insert_notice(self, name, title, date, contents):
        for _ in [name, title, date, contents]:
            if not is_regular(_):
                raise TypeError
        else:
            sql = """INSERT INTO Notice(Name, Title, Date, Contents, View, IsDelete) VALUES('{}', '{}', '{}', '{}', 0, FALSE);""".format(name, title, date, contents)
            self.cursor.execute(sql)
            self.db.commit()
    
    def insert_question(self, name, email, telep, homepage, uType, route, question):
        for _ in [name, email, telep, homepage, uType, route, question]:
            if not is_regular(_):
                raise TypeError
        else:
            sql = """INSERT INTO Question(Name, Email, Telep, Homepage, Type, Route, Question) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(name, email, telep, homepage, uType, route, question)
            self.cursor.execute(sql)
            self.db.commit()

if __name__ == "__main__":
    print(is_db_regular('Forum'))
    print(is_spc_regular('Forum'))
    print(is_regular('Forum'))