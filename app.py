import hashlib

from datetime import datetime
from flask import Flask, render_template, request

from module.ShrimpServer import ShrimpServer
from module.database import DB_SQL

app = Flask(__name__)
ss = ShrimpServer()
db = DB_SQL()

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
    return render_template('index2.html', value=request.args.get('value', 'null'), id=request.args.get('id', 'null'), type=request.args.get('type', 'null'))

@app.route('/notice', methods=['GET'])
def notice():
    row = db.select_table("SELECT ID, Name, Title, Date, View From Notice ORDER BY ID desc LIMIT 0,10;")
    return render_template('notice.html', notices=row)

@app.route('/forum', methods=['GET'])
def forum():
    row = db.select_table("SELECT ID, Name, Title, Date, View From Form ORDER BY ID desc LIMIT 0,10;")
    return render_template('forum.html', notices=row)

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/viewer', methods=['GET'])
def viewer():
    row = db.select_table("SELECT Name, Title, Date, View, Contents From {} WHERE ID={};".format(request.args.get('type', 'Notice'), request.args.get('id', '1')))
    return render_template('viewer.html', view=row[0], type=request.args.get('type', 'Notice'))

@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/post', methods=['POST'])
def post():
    sha = hashlib.sha256()
    sha.update(request.form['pw'].encode("cp949"))
    db.insert_forum( request.form['name'], request.form['title'], datetime.today().strftime("%Y-%m-%d %H:%M:%S"), request.form['comment'], sha.hexdigest() )
    return render_template('index2.html', value=4)