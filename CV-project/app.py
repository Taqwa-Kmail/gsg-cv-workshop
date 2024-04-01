from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import uuid
import posixpath
from ultralytics import YOLO




app = Flask(__name__)
app.config['ALLOWED_EXT'] = { 'jpg','png', 'jpeg'}
app.config['UPLOAD'] = 'static/uploads'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXT']

def stitch_images(image_paths):
    images = [cv2.imread(image_path) for image_path in image_paths]
    stitcher = cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        return stitched_image
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('file[]')
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD'], filename))
                uploaded_files.append(filename)
        return redirect(url_for('results', filenames=uploaded_files))
    return render_template('index.html')



@app.route('/results')
def results():
    filenames = request.args.getlist('filenames')
    image_paths = [os.path.join(app.config['UPLOAD'], filename) for filename in filenames]
    stitched_image = stitch_images(image_paths)
    # Generate filename
    stitched_filename = str(uuid.uuid4()) + '.jpg'
    stitched_image_path = os.path.join(app.config['UPLOAD'], stitched_filename)
    cv2.imwrite(stitched_image_path, stitched_image)
    #Canny edge detection
    edges = cv2.Canny(stitched_image, 100, 200)
    #Gaussian blur
    blurred = cv2.GaussianBlur(stitched_image, (5,5), 0)
    #DoG
    blurred_big = cv2.GaussianBlur(stitched_image, (9,9), 0)
    dog = blurred - blurred_big
    #morphological operation
    kernel_size = int(request.args.get('kernel_size', 3))
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    cleaned_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
   
    edge_filename = str(uuid.uuid4()) + '_edges.jpg'
    edge_image_path = os.path.join(app.config['UPLOAD'], edge_filename)
    cv2.imwrite(edge_image_path, cleaned_edges)

    return render_template('results.html', filenames=filenames, stitched_filename=stitched_filename,edge_filename=edge_filename)

@app.route('/edge_result', methods=['POST'])
def edge_result():
    edge_filename = request.form['edge_filename']
    edge_image_path = os.path.join(app.config['UPLOAD'], edge_filename)
    edge_image_path = edge_image_path.replace(os.path.sep, posixpath.sep)
    return render_template('edge_result.html', edge_image_path=edge_image_path)
 

@app.route('/adjust_kernel', methods=['POST'])
def adjust_kernel():
    kernel_size = int(request.form['kernel_size'])
    edge_image_path = request.form['edge_image_path']
    edge_image = cv2.imread(edge_image_path, cv2.IMREAD_GRAYSCALE)
    #new kernel size
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    cleaned_edges = cv2.morphologyEx(edge_image, cv2.MORPH_CLOSE, kernel)
    updated_edge_filename = str(uuid.uuid4()) + '_edges.jpg'
    updated_edge_image_path = os.path.join(app.config['UPLOAD'], updated_edge_filename)
    cv2.imwrite(updated_edge_image_path, cleaned_edges)
    
    return updated_edge_image_path




if __name__ == '__main__':
    app.run(debug=True)
