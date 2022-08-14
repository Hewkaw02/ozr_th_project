import idcardocr
import findidcard
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import cv2, time
import uuid
import cgi

def process(img_name):
    try:
        idfind = findidcard.findidcard()
        idcard_img = idfind.find(img_name)
        result_dict = idcardocr.idcardocr(idcard_img)
        result_dict['error'] = 0
    except Exception as e:
        result_dict = {'error':1}
        print(e)
    return result_dict

if __name__=="__main__":

    process('testimages/1.jpg')