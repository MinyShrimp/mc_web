from flask import Flask, render_template
from ShrimpServer import ShrimpServer

app = Flask(__name__)
ss = ShrimpServer()

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

@app.route('/info')
def info():
    return render_template('info.html')