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

    def show_tables(self):
        self.cursor.execute('show tables')

if __name__ == "__main__":
    a = DB_SQL()
    a.show_tables()