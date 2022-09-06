# -*- coding: utf-8 -*-
import idcardocr
import findidcard
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import cv2
import time
import uuid
import cgi

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


# SocketServer.ForkingMixIn, SocketServer.ThreadingMixIn
class ForkingServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        #self.end_headers()

    def do_GET(self):
        self._set_headers()
        # self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        # post_data = self.rfile.read(content_length) # <--- Gets the data itself
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        print(pdict)




        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        # print(pdict)
        multipart_data = cgi.parse_multipart(self.rfile, pdict)


        data = multipart_data.get('key-mode')
        print(data)


        fo = open("tmp/image.jpg", "wb")
        fo.write(multipart_data.get('pic')[0])

        if data == ['1']:
            result = process("tmp/image.jpg")
        elif data == ['2']:
            result = check_image("tmp/image.jpg")
        else:
            print(3)
        # filename = uuid.uuid1()
        # print(str(multipart_data))
        # print(multipart_data.get('pic')[0])
        # data = multipart_data.get('key-mode')
        # fo.close()
        # result = process("tmp/123test.jpg")
        # print result
        self._set_headers()
        self.send_header("Content-Length", str(len(json.dumps(result).encode('utf-8'))))
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

def http_server(server_class=ForkingServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    cv2.ocl.setUseOpenCL(False)
    print('Starting httpd...')
    print(u"Status OpenCL：%s"%cv2.ocl.useOpenCL())
    httpd.serve_forever()

if __name__=="__main__":

    # p = Pool()
    #r9 = p.apply_async(process, args=('9.jpg',))
    #r14 = p.apply_async(process, args=('14.jpg',))
    # p.apply_async(http_server)
    # p.apply_async(http_server)
    # p.apply_async(http_server)
    # p.apply_async(http_server)
    # p.close()
    # p.join()
    #print r9.get(), r14.get()
    http_server()
    # cv2.ocl.setUseOpenCL(True)
    # t1 = round(time.time() * 1000)
    # for i in range(1,15):
    #     print(process('./testimages/%s.jpg'%i))
    # t2 = round(time.time() * 1000)
    # print('time:%s' % (t2 - t1))

