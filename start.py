# -*- coding: utf-8 -*-

import io
import os
import uuid
from flask import Flask, render_template, flash, request, redirect, url_for, send_file, after_this_request
from werkzeug.utils import secure_filename
from modifier import modifier_icon

app = Flask(__name__)

UPLOAD_FOLDER = './input'
OUTPUT_FOLDER = './output'
ALLOWED_EXTENSIONS = {'xml', 'dds'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_page():
   return render_template('upload.html')

@app.route('/download')
def download_page():
   dds = request.args.get('dds')
   xml = request.args.get('xml')
   return render_template('download.html', dds = dds, xml = xml)

@app.route('/files/<filename>')
def download_file(filename):
    [_, ext] = os.path.splitext(filename)
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    src_path = os.path.join(UPLOAD_FOLDER, filename)

    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)

    os.remove(file_path)
    os.remove(src_path)

    return send_file(return_data, as_attachment = True, attachment_filename = f'battleAtlas{ext}')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'dds' not in request.files:
            flash('没有选择dds文件')
            return redirect(request.url)
        if 'xml' not in request.files:
            flash('没有选择xml文件')
            return redirect(request.url)
        dds = request.files['dds']
        xml = request.files['xml']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if dds.filename == '':
            flash('没有上传dds文件')
            return redirect(request.url)
        if xml.filename == '':
            flash('没有上传xml文件')
            return redirect(request.url)

        if dds and allowed_file(dds.filename):
            ddsName = str(uuid.uuid4())
            dds.save(os.path.join(UPLOAD_FOLDER, f'{ddsName}.dds'))
        if xml and allowed_file(xml.filename):
            xmlName = str(uuid.uuid4())
            xml.save(os.path.join(UPLOAD_FOLDER, f'{xmlName}.xml'))

        modifier_icon(ddsName, xmlName)
        
        return redirect(url_for('download_page', dds=ddsName, xml=xmlName))
		
if __name__ == '__main__':
    app.run(debug = True)