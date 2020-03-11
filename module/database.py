import pymysql

class DB_SQL():
    def __init__(self):
        self.db = pymysql.connect(
            host= '34.80.56.3',
            port=3306,
            user='root',
            passwd='alsl1203',
            db='MINECRAFT',
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    def __del__(self):
        self.db.close()

    def show_tables(self):
        self.cursor.execute('show tables')
    
    def get_count_table(self, table):
        sql = """SELECT COUNT(*) FROM {} WHERE IsDelete=FALSE;""".format(table)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def delete_forum(self, id):
        sql = """UPDATE Forum SET IsDelete=TRUE WHERE ID={};""".format(id)
        self.cursor.execute(sql)
        self.db.commit()
    
    def select_table(self, _str):
        self.cursor.execute(_str)
        return self.cursor.fetchall()

    def update_forum(self, id, name, title, date, contents, pw):
        sql = """UPDATE Forum SET Name='{}', Title='{}', Date='{}', Contents='{}', PW='{}' WHERE ID='{}';""".format(name, title, date, contents, pw, id)
        self.cursor.execute(sql)
        self.db.commit()
    
    def insert_user(self, uid, pw, email, nickname, m_nickname):
        sql = """INSERT INTO User(uID, PW, Email, Nickname, mNickname) VALUES('{}', '{}', '{}', '{}', '{}');""".format(uid, pw, email, nickname, m_nickname)
        self.cursor.execute(sql)
        self.db.commit()
    
    def insert_forum(self, name, title, date, contents, pw):
        sql = """INSERT INTO Forum(Name, Title, Date, Contents, PW, View, IsDelete) VALUES('{}', '{}', '{}', '{}', '{}', 0, FALSE);""".format(name, title, date, contents, pw)
        self.cursor.execute(sql)
        self.db.commit()

    def insert_notice(self, name, title, date, contents):
        sql = """INSERT INTO Notice(Name, Title, Date, Contents, View, IsDelete) VALUES('{}', '{}', '{}', '{}', 0, FALSE);""".format(name, title, date, contents)
        self.cursor.execute(sql)
        self.db.commit()
    
    def insert_question(self, name, email, telep, homepage, uType, route, question):
        sql = """INSERT INTO Question(Name, Email, Telep, Homepage, Type, Route, Question) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(name, email, telep, homepage, uType, route, question)
        self.cursor.execute(sql)
        self.db.commit()

if __name__ == "__main__":
    db = DB_SQL()
    while True:
        _ = input()
        print(db.select_table(_))