from markupsafe import escape
import idcardocr
import findidcard
import json
from flask import jsonify
import uuid
import cgi
import cv2
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def process(img_name):
    try:
        idfind = findidcard.findidcard()
        idcard_img = idfind.find(img_name)
        cv2.imwrite('tmp-crop/Main-image.jpg', idcard_img)
        # print(idcard_img)
        # result_dict = {'error': 0}
        image_for_use = 'tmp-crop/Main-image.jpg'
        result_dict = idcardocr.idcardocr(cv2.UMat(cv2.imread(image_for_use)))
        # print(result_dict)
        # result_dict['error'] = 0
    except Exception as e:
        result_dict = {'error':1}
        print(e)
    return result_dict


def check_image(img_name):
    try:
        idfind = findidcard.findidcard()
        idcard_img = idfind.find(img_name)
        cv2.imwrite('tmp-crop/Check-image.jpg', idcard_img)
        # print(idcard_img)
        # result_dict = {'error': 0}
        image_for_check = 'tmp-crop/Check-image.jpg'
        name_use = 'tmp-crop/Main-image.jpg'
        point = findidcard.Check_part(image_for_check,name_use)
        if point > 0.7:
            result_check = {'Staus':'pass'}
            print('pass')
        else:
            result_check = {'Staus': 'not pass'}
            print('not pass')
    except Exception as e:
        result_check = {'error':1}
        print(e)
    return result_check

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(f'tmp/image.jpg')
        data = request.form['mode_id']

        if data == '1':
            result = process("tmp/image.jpg")
        elif data == '2':
            result = check_image("tmp/image.jpg")
    return  jsonify(result)

if __name__ == '__main__':
    app.run()

