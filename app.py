import os
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from Main import changeVideo

# UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            changeVideo(filename)
            # return send_file(file, mimetype='video')
            # return redirect(url_for('upload_file', name=filename))
            return send_file('video.avi')
        
    return '''
    <!doctype html>
    <title>Badminton Video Ai Analyser</title>
    <h1>Badminton Video Ai Analyser By Kevin</h1>
    <h2>Upload a Badminton Video</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <p>After uploading a video, this program will automatically analyze and edit the video before downloading to your computer</p>
    <p>Warning: longer videos may take multiple minutes to process</p>
    <p>Tip: short stationary videos with badminton as the focus will work best</p>
    '''

# app.run(host='0.0.0.0')