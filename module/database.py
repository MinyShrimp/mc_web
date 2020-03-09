import pymysql

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
        self.cursor = db.cursor()
    
    def __del__(self):
        db.close()

    def show_tables(self):
        self.cursor.execute('show tables')
    
    def select_table(self, _str):
        self.cursor.execute(_str)
        return self.cursor.fetchall()
    
    def insert_user(self, uid, pw, email, nickname, m_nickname):
        sql = """INSERT INTO User(uID PW Email Nickname mNickname) VALUES('{}', '{}', '{}', '{}', '{}')""".format(uid, pw, email, nickname, m_nickname)
        self.cursor.execute(sql)
        self.db.commit()
    
    def insert_forum(self, name, title, date, contents):
        sql = """INSERT INTO Form(Name Title Date Contents) VALUES('{}', '{}', '{}', '{}')""".format(name, title, date, contents)
        self.cursor.execute(sql)
        self.db.commit()

    def insert_notice(self, name, title, date, contents):
        sql = """INSERT INTO Notice(Name Title Date Contents) VALUES('{}', '{}', '{}', '{}')""".format(name, title, date, contents)
        self.cursor.execute(sql)
        self.db.commit()
    
    def insert_question(self, name, email, telep, homepage, uType, route, question):
        sql = """INSERT INTO Question(Name Email Telep Homepage Type Route Question) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(name, email, telep, homepage, uType, route, question)
        self.cursor.execute(sql)
        self.db.commit()

if __name__ == "__main__":
    a = DB_SQL()
    a.show_tables()