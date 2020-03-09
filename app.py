from flask import Flask, render_template, request
from module.ShrimpServer import ShrimpServer
from module.database import DB_SQL

app = Flask(__name__)
ss = ShrimpServer()
#db = DB_SQL()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open')
def is_open():
    ss.connect()
    return render_template('open.html', is_open = ss.stats, count = ss.getPlayerLen())

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/index2')
def index2():
    return render_template('index2.html', value=request.args.get('value', 'null'))

@app.route('/notice', methods=['GET'])
def notice():
    #row = db.select_table("SELECT ID, Name, Title, Date, View From Notice LIMIT 0,10;")
    #print(row)
    #return render_template('notice.html', notices=row)
    return render_template('notice.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')