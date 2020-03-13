# -*- coding: utf-8 -*-

import hashlib
import os, re

from datetime import datetime
from flask import Flask, render_template, request, redirect, session, escape, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename

from module.ShrimpServer import ShrimpServer
from module.database import DB_SQL

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = './files/uploads'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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
    try:
        page = int(request.args.get('page', 1))
        row = db.select_page('Notice', page)
        return render_template('notice.html', notices=row, count=db.get_count_table('Forum')[0]['COUNT(*)'])
    except TypeError:
        return redirect('/error')

@app.route('/forum', methods=['GET'])
def forum():
    try:
        page = int(request.args.get('page', 1))
        row = db.select_page('Forum', page)
        return render_template('forum.html', notices=row, count=db.get_count_table('Forum')[0]['COUNT(*)'])
    except TypeError:
        return redirect('/error')

@app.route('/write', methods=['GET', 'POST'])
def write():
    try:
        if request.method == 'POST':
            sha = hashlib.sha256()
            sha.update(request.form['pw'].encode("cp949"))
            
            _pw = db.select_table('Forum', 'PW', 'ID={}'.format(request.form['id']))[0]['PW']
            if _pw != sha.hexdigest():
                return redirect('/index2?value=4')
            
            if request.form['type'] == '1': # delete
                db.delete_forum(request.form['id'])
                return redirect('/index2?value=4')
            else: # fix
                return redirect('/index2?value=9&id={}'.format(request.form['id']))#render_template('write.html', data=_data[0])
        else:
            _data = db.select_table('Forum', 'Name, Title, Contents', 'ID={}'.format(request.args.get('id', 'None')))
            if len(_data) == 0:
                return render_template('write.html', data={'Title': '', 'Name': '', 'Contents': ''}, _type=0, _id=0)
            else:
                return render_template('write.html', data=_data[0], _type=1, _id=request.args.get('id', 'None'))
    except:
        return redirect('/index2?value=4')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            _p = re.compile('[.].+')
            _m = _p.search(file.filename).group()
            _f = file.filename.replace(_m, datetime.today().strftime('%y%m%d%H%M%S') + _m)
            
            filename = secure_filename(_f)
            
            file.save(app.config['UPLOAD_FOLDER'] + "/" + filename)
            return url_for('uploaded_file', filename=filename)
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/viewer', methods=['GET'])
def viewer():
    try:
        row = db.select_table('{}'.format(request.args.get('type', 'Notice')), 'Name, Title, Date, View, Contents', 'ID={}'.format(request.args.get('id', '1')))[0]
        return render_template('viewer.html', view=row, type=request.args.get('type', 'Notice'), id=request.args.get('id', '1'))
    except TypeError:
        return redirect('/index2?value={}'.format(3 if request.args.get('type', 'Notice') == 'Notice' else 4))

@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/q_send', methods=['POST'])
def q_send_post():
    try:
        db.insert_question(request.form['name'], request.form['email'], request.form['telep'], request.form['homepage'], request.form['type'], request.form['route'], request.form['question'])
        return redirect('/index2?value=10')
    except:
        return redirect('/error')

@app.route('/q_send_complete')
def q_send():
    return render_template('q_send.html')

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
    try:
        sha = hashlib.sha256()
        sha.update(request.form['pw'].encode("cp949"))
        if request.form['type'] == '1': # 수정
            db.update_forum( int(request.form['id']), request.form['name'], request.form['title'], datetime.today().strftime("%Y-%m-%d %H:%M:%S"), request.form['comment'], sha.hexdigest() )
        else: # 새로 작성
            db.insert_forum( request.form['name'], request.form['title'], datetime.today().strftime("%Y-%m-%d %H:%M:%S"), request.form['comment'], sha.hexdigest() )
        return redirect('/index2?value=4')
    except:
        redirect('/error')

@app.route('/admin')
def admin():
    return render_template('admin-login.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        sha = hashlib.sha256()
        sha.update(request.form['pw'].encode("cp949"))
        _table = db.select_table("User", "uID, PW")
        for _t in _table:
            if request.form['id'] == _t['uID']:
                if sha.hexdigest() == _t['PW']:
                    if 'uid' in session:
                        result = '{}'.format(session['uid'])
                    else:
                        session['uid'] = request.form['id']
                        result = '{}'.format(escape(session['uid']))
                    return redirect("/admin-home?result={}".format(result))
        else:
            return redirect('/index2?value=1')
    except:
        return redirect('/index2?value=1')

@app.route('/admin-home', methods=['GET'])
def admin_home():
    try:
        if escape(session['uid']) != request.args.get('result', ''):
            return redirect("/admin")
        else:
            return render_template('admin-home.html')
    except KeyError:
        return redirect("/admin")

@app.route('/admin-logout')
def admin_logout():
    session.pop('uid', None)
    return render_template('admin-login.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='80', debug=True)