# views.py
from utils import *

from flask import render_template, Response, make_response, send_from_directory
from functools import wraps, update_wrapper
from datetime import datetime
from app import app

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stylize')
def stylize():
    generate_styles()
    return 'success'

@app.route('/result')
def about():
    return render_template("result.html")

@app.route('/style_img/<int:id>')
def style_img(id):
    filename = "img/style" + str(id) + ".png"
    return send_from_directory('static', filename, cache_timeout=0)
