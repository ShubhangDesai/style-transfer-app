# views.py
from modules import Camera
from modules import StyleCNN

from PIL import Image
from StringIO import StringIO

from flask import render_template, Response, send_file
from app import app

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def get_pil_pic(camera):
    pic = camera.get_pic()
    return Image.fromarray(pic)

@app.route('/cam_image')
def cam_image():
    pic = get_pil_pic(Camera())

    img_io = StringIO()
    pic.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

@app.route('/about')
def about():
    return render_template("about.html")
