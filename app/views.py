# views.py
from utils import *

from flask import render_template, Response, send_from_directory
import gevent
import random
from functools import wraps, update_wrapper
from datetime import datetime
from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen_thread(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stylize')
def stylize():
    print("hello")
    generate_styles()
    return 'success'

@app.route('/result')
def about():
    return render_template("result.html")

@app.route('/style_img/<int:id>')
def style_img(id):
    filename = "img/style" + str(id) + ".png"
    return send_from_directory('static', filename, cache_timeout=0)

def task(pid):
    """
    Some non-deterministic task
    """
    gevent.sleep(random.randint(0,2)*0.001)
    print('Task %s done' % pid)

def asynchronous():
    threads = [gevent.spawn(task, i) for i in xrange(10)]
    gevent.joinall(threads)

@app.route('/test')
def test():
    asynchronous()
    return 'test'
