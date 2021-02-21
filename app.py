# import os
import cv2
# import jsonify, json
import numpy as np
from flask import Flask, render_template, request, flash, url_for, redirect
# from flask.ext.navigation import Navigation
from werkzeug.utils import secure_filename

# setting up Flask instance
app = Flask(__name__)
# nav = Navigation(app)
app.secret_key = "TOTALLY SECRET KEY"

# UPLOAD_FOLDER = 'uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# Initial page
@app.route('/')
def home():
    return render_template('WelcomePage.html')


@app.route('/puzzle1')
def puzzle1():
    return render_template('index1.html')


@app.route('/puzzle2')
def puzzle2():
    return render_template('puzzle2.html')


@app.route('/upload1', methods=['GET', 'POST'])
def upload1():
    if request.method == 'POST':
        # if no file part has been uploaded
        if 'file' not in request.files:
            flash('No file part')

        # get the file
        file = request.files['file']

        # if no file has been selected
        if file.filename == '':
            flash('No selected file')
            # redirect(request.url)

        # save file to specified directory
        filename = secure_filename(file.filename)
        file.save(filename)

        # take the file and after saving it, send it to QR_decode_function
        detected_list_info = detect_qr_codes(filename)
        flash('file uploaded successfully')
        return render_template('index1.html', data=detected_list_info)


@app.route('/upload2', methods=['GET', 'POST'])
def upload2():
    if request.method == 'POST':
        # if no file part has been uploaded
        if 'file' not in request.files:
            flash('No file part')

        # get the file
        file = request.files['file']

        # if no file has been selected
        if file.filename == '':
            flash('No selected file')
            # redirect(request.url)

        # save file to specified directory
        filename = secure_filename(file.filename)
        file.save(filename)

        # take the file and after saving it, send it to QR_decode_function
        detected_list_info = detect_qr_codes(filename)
        flash('file uploaded successfully')
        return render_template('puzzle2.html', data=detected_list_info)


# Endpoint to upload file to server
# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
        # if no file part has been uploaded
#        if 'file' not in request.files:
#            flash('No file part')

        # get the file
#        file = request.files['file']

        # if no file has been selected
#        if file.filename == '':
#            flash('No selected file')
            # redirect(request.url)

        # save file to specified directory
#        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#        file.save(filename)

        # take the file and after saving it, send it to QR_decode_function
#        detected_list_info = detect_qr_codes(filename)
        #list_info = {}

        #for i in range(len(detected_list_info)):
        #    list_info[i] = detected_list_info[i]


        # send it straight to game itself
#        flash('file uploaded successfully')
        #return render_template('index1.html', data=list_info)
#        return render_template('index1.html', data=detected_list_info)
        # return render_template('result.html', data=detected_list_info)


# when uploaded file is too large
@app.errorhandler(413)
def large_file(e):
    # redirect user
    flash('File is too large, please submit a smaller file')
    return redirect(url_for(request.url)), 413


# function to detect qr_codes from single image
def detect_qr_codes(filename):
    def getY(index):
        return points[index][0][1]

    img = cv2.imread(filename)

    Img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.bitwise_not(img)

    qrDecoder = cv2.QRCodeDetector()

    retval, decoded_info, points, straight_qrcode = qrDecoder.detectAndDecodeMulti(np.hstack([img, img]))

    quad_filtered = []

    decoded_info_filtered_sorted = []

    for i in range(len(points)):
        if points[i][0][0] < img.shape[1]:
            quad_filtered.append(i)

    quad_filtered_sorted = sorted(quad_filtered, key=getY)

    for i in quad_filtered_sorted:
        decoded_info_filtered_sorted.append(decoded_info[i])
    return decoded_info_filtered_sorted


if __name__ == '__main__':
    app.run(debug=True)
