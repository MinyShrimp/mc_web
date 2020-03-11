import hashlib

from datetime import datetime
from flask import Flask, render_template, request, redirect

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
    #ss.connect()
    return render_template('open.html', is_open = ss.stats, count = ss.getPlayerLen())

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/index2')
def index2():
    return render_template('index2.html', value=request.args.get('value', 'null'), id=request.args.get('id', 'null'), type=request.args.get('type', 'null'))

@app.route('/notice', methods=['GET'])
def notice():
    page = request.args.get('page', 1)
    row = db.select_table("SELECT ID, Name, Title, Date, View FROM Notice WHERE IsDelete=FALSE ORDER BY ID desc LIMIT {}, {};".format( 10 * (page - 1), 10 * page - 1 ))
    return render_template('notice.html', notices=row, count=db.get_count_table('Notice')[0]['COUNT(*)'])

@app.route('/forum', methods=['GET'])
def forum():
    page = request.args.get('page', 1)
    row = db.select_table("SELECT ID, Name, Title, Date, View FROM Forum WHERE IsDelete=FALSE ORDER BY ID desc LIMIT {}, {};".format( 10 * (page - 1), 10 * page - 1 ))
    return render_template('forum.html', notices=row, count=db.get_count_table('Forum')[0]['COUNT(*)'])

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        sha = hashlib.sha256()
        sha.update(request.form['pw'].encode("cp949"))
        
        _pw = db.select_table("SELECT PW FROM Forum WHERE ID={};".format(request.form['id']))[0]['PW']
        if _pw != sha.hexdigest():
            return redirect('/index2?value=4')
        
        if request.form['type'] == '1': # delete
            db.delete_forum(request.form['id'])
            return redirect('/index2?value=4')
        else: # fix
            return redirect('/index2?value=9&id={}'.format(request.form['id']))#render_template('write.html', data=_data[0])
    else:
        _data = db.select_table("SELECT Name, Title, Contents FROM Forum WHERE ID={};".format(request.args.get('id', 'None')))
        if len(_data) == 0:
            return render_template('write.html', data={'Title': '', 'Name': '', 'Contents': ''}, _type=0, _id=0)
        else:
            return render_template('write.html', data=_data[0], _type=1, _id=request.args.get('id', 'None'))

@app.route('/viewer', methods=['GET'])
def viewer():
    row = db.select_table("SELECT Name, Title, Date, View, Contents FROM {} WHERE ID={};".format(request.args.get('type', 'Notice'), request.args.get('id', '1')))[0]
    return render_template('viewer.html', view=row, type=request.args.get('type', 'Notice'), id=request.args.get('id', '1'))

@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/map')
def _map():
    return render_template('map.html')

@app.route('/post', methods=['POST'])
def post():
    sha = hashlib.sha256()
    sha.update(request.form['pw'].encode("cp949"))
    if request.form['type'] == '1': # 수정
        print(request.form)
        db.update_forum( int(request.form['id']), request.form['name'], request.form['title'], datetime.today().strftime("%Y-%m-%d %H:%M:%S"), request.form['comment'], sha.hexdigest() )
    else: # 새로 작성
        db.insert_forum( request.form['name'], request.form['title'], datetime.today().strftime("%Y-%m-%d %H:%M:%S"), request.form['comment'], sha.hexdigest() )
    return redirect('/index2?value=4')