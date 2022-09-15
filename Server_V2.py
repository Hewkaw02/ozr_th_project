from flask import Flask, render_template, request
import idcardocr
import findidcard
import json
import cgi
import cv2
from werkzeug import secure_filename
app.config['UPLOAD_FOLDER']

app = Flask(__name__)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


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


if __name__ == '__main__':
    app.run(debug=True)