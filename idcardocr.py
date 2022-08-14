from PIL import Image
import pytesseract
import cv2
import numpy as np
import re
from matplotlib import pyplot as plt
from multiprocessing import Pool, Queue, Lock, Process, freeze_support
import time

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
x = 1280.00 / 3840.00
# Switch_for_get_data:int = 0
pixel_x = int(x * 3840)
print(x, pixel_x)





def idcardocr(imgname , mode=1):
    print(u'เริ่มต้นการระบุตัวตน...')
    if mode == 1:
        # generate_mask(x)
        img_data_gray, img_org = img_resize_gray(imgname)
        result_dict = dict()
        name_pic = find_name(img_data_gray, img_org)
        # showimg(name_pic)
        # print 'name'
        result_dict['fullname_th'] = get_name(name_pic)
        # print(result_dict['name'])

        ######## ยังใช้งานไม่ได้ดี
        # firstname_en_pic = find_firstname_en(img_data_gray, img_org)
        # result_dict['firstname_en'] = get_firstname(firstname_en_pic)
        # showimg(firstname_en_pic)
        # lastname_en_pic = find_lastname_en(img_data_gray, img_org)
        # result_dict['lastname_en'] = get_lastname(lastname_en_pic)
        # showimg(lastname_en_pic)

        # address_pic = find_address(img_data_gray, img_org)
        # showimg(address_pic)
        # print 'address'
        # result_dict['address'] = get_address(address_pic)
        # print(get_address(address_pic))

        idnum_pic = find_idnum(img_data_gray, img_org)
        result_dict['idnum'] = get_idnum(idnum_pic)

        birth_day = find_birth(img_data_gray,img_org)
        # showimg(birth_day)
        Cal_Date = get_birthday(birth_day)
        Date_result = Cal_Birthday_th(Cal_Date)
        result_dict['Date_Birthday_th'] = Date_result
        result_dict['Date_Birthday_en'] = get_birthday(birth_day)

        print(result_dict)
    elif mode == 0:
        # generate_mask(x)
        img_data_gray, img_org = img_resize_gray(imgname)
        result_dict = dict()
        name_pic = find_name(img_data_gray, img_org)
        # showimg(name_pic)
        # print 'name'
        result_dict['name'] = get_name(name_pic)
        # print result_dict['name']

        idnum_pic = find_idnum(img_data_gray, img_org)
        # showimg(idnum_pic)
        # print 'idnum'

        result_dict['idnum'], result_dict['birth'] = get_idnum_and_birth(idnum_pic)
        result_dict['sex'] = ''
        result_dict['nation'] = ''
        result_dict['address'] = ''

    else:
        print(u"模式选择错误！")

    # showimg(img_data_gray)
    return result_dict

def Cal_Birthday_th(word):
    datebth = ['','','']
    part = word.split()
    if part[1] == 'Jan.':
        datebth[1] = 'ม.ค.'
    elif part[1] == 'Feb.':
        datebth[1] = 'ก.พ.'
    elif part[1] == 'Mar.':
        datebth[1] = 'มี.ค.'
    elif part[1] == 'Apr.':
        datebth[1] = 'เม.ย.'
    elif part[1] == 'May.':
        datebth[1] = 'พ.ค.'
    elif part[1] == 'Jun.':
        datebth[1] = 'มิ.ย.'
    elif part[1] == 'Jul.':
        datebth[1] = 'ก.ค.'
    elif part[1] == 'Aug.':
        datebth[1] = 'ส.ค.'
    elif part[1] == 'Sep.':
        datebth[1] = 'ก.ย.'
    elif part[1] == 'Oct.':
        datebth[1] = 'ต.ค.'
    elif part[1] == 'Nov.':
        datebth[1] = 'พ.ย.'
    elif part[1] == 'Now.':
        datebth[1] = 'พ.ย.'
    elif part[1] == 'Noy.':
        datebth[1] = 'พ.ย.'
    elif part[1] == 'Dec.':
        datebth[1] = 'ธ.ค.'
    else:datebth[1] = part[1]

    datebth[0] = int(part[0])
    a = int(part[2])+543
    datebth[2] = a
    print(datebth)
    return datebth

def generate_mask(x):
    # TH Generate mask
    # name_mask_pic = cv2.UMat(cv2.imread('name_th_mask.jpg'))
    # birth_mask_pic = cv2.UMat(cv2.imread('birth_th_mask.jpg'))
    # address_mask_pic = cv2.UMat(cv2.imread('address_mask.jpg'))
    idnum_mask_pic = cv2.UMat(cv2.imread('idnum_mask.jpg'))
    # TH resize
    # name_mask_pic = img_resize_x(name_mask_pic)
    # birth_mask_pic = img_resize_x(birth_mask_pic)
    # address_mask_pic = img_resize_x(address_mask_pic)
    idnum_mask_pic = img_resize_x(idnum_mask_pic)

    # cv2.imwrite('name_mask_%s.jpg' % pixel_x, name_mask_pic)
    # cv2.imwrite('birth_mask_%s.jpg' % pixel_x, birth_mask_pic)
    # cv2.imwrite('address_mask_%s.jpg' % pixel_x, address_mask_pic)
    cv2.imwrite('idnum_mask_%s.jpg' % pixel_x, idnum_mask_pic)

def img_resize_x(imggray):
    # print 'dheight:%s' % dheight
    crop = imggray
    size = crop.get().shape
    dheight = int(size[0] * x)
    dwidth = int(size[1] * x)
    crop = cv2.resize(crop, (dwidth, dheight), cv2.INTER_CUBIC)
    return crop

# idcardocr里面resize以高度为依据, 用于get部分
def img_resize(imggray, dheight):
    # print 'dheight:%s' % dheight
    crop = imggray
    size = crop.get().shape
    height = size[0]
    width = size[1]
    width = width * dheight / height
    crop = cv2.resize(crop, (int(width), dheight), cv2.INTER_CUBIC)
    return crop

def img_resize_gray(imgorg):

    # imgorg = cv2.imread(imgname)
    crop = imgorg
    size = crop.get().shape
    # print size
    height = size[0]
    width = size[1]
    # 参数是根据3840调的
    height = int(height * 3840 * x / width)
    # print height
    crop = cv2.resize(crop, (int(3840 * x), height), cv2.INTER_CUBIC)
    return hist_equal(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)), crop

def find_name(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread('name_th_mask.jpg', 0))
    w, h = cv2.UMat.get(template).shape[::-1]

    # showimg(template)
    # showimg(crop_gray)
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    # showimg(res)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(max_loc)
    top_left = (max_loc[0] + w - 20, max_loc[1] - int(90 * x))
    # print(top_left)
    bottom_right = (top_left[0] + int(2500 * x), top_left[1] + int(350 * x))
    # print(bottom_right)
    result = cv2.UMat.get(crop_org)[top_left[1] - 10:bottom_right[1], top_left[0] - 10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    # showimg(result)
    return cv2.UMat(result)

def find_firstname_en(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread('name_en_firstname.jpg', 0))
    w, h = cv2.UMat.get(template).shape[::-1]

    # showimg(template)
    # showimg(crop_gray)
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    # showimg(res)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(max_loc)
    top_left = (max_loc[0] + w - 600, max_loc[1] - int(120 * x))
    print(top_left)
    bottom_right = (top_left[0] + int(1000 * x), top_left[1] + int(150 * x))
    print(bottom_right)
    result = cv2.UMat.get(crop_org)[top_left[1] - 10:bottom_right[1], top_left[0] - 10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    showimg(result)
    return cv2.UMat(result)

def find_lastname_en(crop_gray, crop_org):
    template = cv2.UMat(cv2.imread('name_en_lastname.jpg', 0))
    w, h = cv2.UMat.get(template).shape[::-1]

    # showimg(template)
    # showimg(crop_gray)
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    # showimg(res)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(max_loc)
    top_left = (max_loc[0] + w - 20, max_loc[1] - int(90 * x))
    # print(top_left)
    bottom_right = (top_left[0] + int(2000 * x), top_left[1] + int(350 * x))
    # print(bottom_right)
    result = cv2.UMat.get(crop_org)[top_left[1] - 10:bottom_right[1], top_left[0] - 10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    showimg(result)
    return cv2.UMat(result)

def find_address(crop_gray, crop_org):
        template = cv2.UMat(cv2.imread('address_mask.jpg', 0))
        w, h = cv2.UMat.get(template).shape[::-1]

        showimg(template)
        showimg(crop_gray)
        #t1 = round(time.time()*1000)
        res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
        #t2 = round(time.time()*1000)
        #print 'time:%s'%(t2-t1)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = (max_loc[0] + w - 80, max_loc[1] + int(30*x))
        # print(top_left)
        bottom_right = (top_left[0] + int(1800*x), top_left[1] + int(300*x))
        # print(bottom_right)
        result = cv2.UMat.get(crop_org)[top_left[1]-10:bottom_right[1], top_left[0]-10:bottom_right[0]]
        cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
        # showimg(crop_gray)
        return cv2.UMat(result)

def find_idnum(crop_gray, crop_org):
        template = cv2.UMat(cv2.imread('idnum_mask_1.jpg', 0))
        # showimg(template)
        # showimg(crop_gray)
        w, h = cv2.UMat.get(template).shape[::-1]
        res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
        # showimg(res)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = (max_loc[0] + w - 720, max_loc[1] + int(150*x))
        print(top_left)
        bottom_right = (top_left[0] + int(1400*x), top_left[1] + int(300*x))
        print(bottom_right)
        result = cv2.UMat.get(crop_org)[top_left[1]-10:bottom_right[1], top_left[0]-10:bottom_right[0]]
        cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
        # showimg(crop_gray)
        return cv2.UMat(result)

def find_birth (crop_gray, crop_org):
    template = cv2.UMat(cv2.imread('birth_en_mask.jpg', 0))
    # showimg(template)
    # showimg(crop_gray)
    w, h = cv2.UMat.get(template).shape[::-1]
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    # showimg(res)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = (max_loc[0] + w , max_loc[1] - int(50 * x))
    print(top_left)
    bottom_right = (top_left[0] + int(1000 * x), top_left[1] + int(200 * x))
    print(bottom_right)
    result = cv2.UMat.get(crop_org)[top_left[1] - 10:bottom_right[1], top_left[0] - 10:bottom_right[0]]
    cv2.rectangle(crop_gray, top_left, bottom_right, 255, 2)
    showimg(result)
    return cv2.UMat(result)

def showimg(img):
        cv2.namedWindow("contours", 0)
        cv2.resizeWindow("contours", 1280, 720)
        cv2.imshow("contours", img)
        cv2.waitKey()

def get_name(img):
    # cv2.imshow("method3", img)
    # cv2.waitKey()
    print('name')
    _, _, red = cv2.split(img)  # split 会自动将UMat转换回Mat
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(red, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 50)
    # red = cv2.medianBlur(red, 3)
    red = img_resize(red, 150)
    img = img_resize(img, 150)
    # showimg(red)
    # cv2.imwrite('name.png', red)
    #    img2 = Image.open('address.png')
    # img = Image.fromarray(cv2.UMat.get(red).astype('uint8'))
    # return get_result_vary_length(red, 'chi_sim', img, '-psm 7')
    return get_result_name_length(red, 'tha', img, '--psm 6')
    # return punc_filter(pytesseract.image_to_string(img, lang='chi_sim', config='-psm 13').replace(" ",""))

def get_address(img):
    # _, _, red = cv2.split(img)
    # red = cv2.medianBlur(red, 3)
    print('address')
    _, _, red = cv2.split(img)
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50)
    red = img_resize(red, 300)
    # img = img_resize(img, 300)
    # cv2.imwrite('address_red.png', red)
    img = Image.fromarray(cv2.UMat.get(red).astype('uint8'))
    # return punc_filter(get_result_vary_length(red,'chi_sim', img, '-psm 6'))
    return get_result_address(red, 'tha+eng', img, '--psm 6')
    # return punc_filter(pytesseract.image_to_string(img, lang='chi_sim', config='-psm 3').replace(" ",""))

def get_idnum(img):
    _, _, red = cv2.split(img)
    # print('idnum')
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50)
    red = img_resize(red, 150)
    # cv2.imwrite('idnum_red.png', red)
    # idnum_str = get_result_fix_length(red, 18, 'idnum', '-psm 8')
    # idnum_str = get_result_fix_length(red, 18, 'eng', '--psm 8 ')
    img = Image.fromarray(cv2.UMat.get(red).astype('uint8'))
    idnum_str = get_result_idnum(red, 'eng', img, '--psm 8 ')
    return idnum_str

def get_birthday(img):
    _, _, red = cv2.split(img)
    # print('idnum')
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50)
    red = img_resize(red, 150)
    # cv2.imwrite('idnum_red.png', red)
    # idnum_str = get_result_fix_length(red, 18, 'idnum', '-psm 8')
    # idnum_str = get_result_fix_length(red, 18, 'eng', '--psm 8 ')
    img = Image.fromarray(cv2.UMat.get(red).astype('uint8'))
    idnum_str = get_result_birthday(red, 'eng', img, '--psm 7 ')
    return idnum_str

def get_firstname(img):
    _, _, red = cv2.split(img)
    # print('idnum')
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50)
    red = img_resize(red, 150)
    # cv2.imwrite('idnum_red.png', red)
    # idnum_str = get_result_fix_length(red, 18, 'idnum', '-psm 8')
    # idnum_str = get_result_fix_length(red, 18, 'eng', '--psm 8 ')
    img = Image.fromarray(cv2.UMat.get(red).astype('uint8'))
    idnum_str = get_result_firstname(red, 'eng', img, '--psm 7 ')
    return idnum_str

def get_lastname(img):
    _, _, red = cv2.split(img)
    # print('idnum')
    red = cv2.UMat(red)
    red = hist_equal(red)
    red = cv2.adaptiveThreshold(red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 50)
    red = img_resize(red, 150)
    # cv2.imwrite('idnum_red.png', red)
    # idnum_str = get_result_fix_length(red, 18, 'idnum', '-psm 8')
    # idnum_str = get_result_fix_length(red, 18, 'eng', '--psm 8 ')
    img = Image.fromarray(cv2.UMat.get(red).astype('uint8'))
    idnum_str = get_result_lastname(red, 'eng', img, '--psm 8 ')
    return idnum_str

def get_result_fix_length(red, fix_length, langset, custom_config=''):
    red_org = red
    cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours, hierarchy = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    # 描边一次可以减少噪点
    cv2.drawContours(red, contours, -1, (0, 255, 0), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    # for x, y, w, h in contours:
    #     imgrect = cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # showimg(imgrect)

    h_threshold = 54
    numset_contours = []
    calcu_cnt = 1
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > h_threshold:
            numset_contours.append((x, y, w, h))
    while len(numset_contours) != fix_length:
        if calcu_cnt > 50:
            print(u'计算次数过多！目前阈值为：', h_threshold)
            break
        numset_contours = []
        calcu_cnt += 1
        if len(numset_contours) > fix_length:
            h_threshold += 1
            contours_cnt = 0
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h > h_threshold:
                    contours_cnt += 1
                    numset_contours.append((x, y, w, h))
        if len(numset_contours) < fix_length:
            h_threshold -= 1
            contours_cnt = 0
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h > h_threshold:
                    contours_cnt += 1
                    numset_contours.append((x, y, w, h))
    result_string = ''
    numset_contours.sort(key=lambda num: num[0])
    for x, y, w, h in numset_contours:
        result_string += pytesseract.image_to_string(cv2.UMat.get(red_org)[y - 10:y + h + 10, x - 10:x + w + 10],
                                                     lang=langset, config=custom_config)
    # print(new_r)
    # cv2.imwrite('fixlengthred.png', cv2.UMat.get(red_org)[y-10:y + h +10 , x-10:x + w + 10])
    print(result_string)
    return result_string

def get_result_idnum(red, langset, org_img, custom_config=''):
    red_org = red
    # cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(contours))
    # 描边一次可以减少噪点
    cv2.drawContours(red, image, -1, (255, 255, 255), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    numset_contours = []
    height_list = []
    width_list = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        height_list.append(h)
        # print(h,w)
        width_list.append(w)
    height_list.remove(max(height_list))
    width_list.remove(max(width_list))
    height_threshold = 0.70 * max(height_list)
    width_threshold = 1.4 * max(width_list)
    # print('height_threshold:'+str(height_threshold)+'width_threshold:'+str(width_threshold))
    big_rect = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > height_threshold and w < width_threshold:
            # print(h,w)
            numset_contours.append((x, y, w, h))
            big_rect.append((x, y))
            big_rect.append((x + w, y + h))
    big_rect_nparray = np.array(big_rect, ndmin=3)
    x, y, w, h = cv2.boundingRect(big_rect_nparray)

    imgrect = cv2.rectangle(color_img, (x - 10, y - 20), (x + w + 500, y + h), (0, 255, 0), 2)
    showimg(imgrect)


    # showimg(cv2.UMat.get(org_img)[y-20:y + h + 20, x + 20:x + w +20])

    result_string = ''
    result_string += pytesseract.image_to_string(cv2.UMat.get(red_org)[y:y + h, x:x + w],
                                                 langset,
                                                 custom_config)

    # print(result_string)
    # cv2.imwrite('varylength.png', cv2.UMat.get(org_img)[y - 20 :y + h, x + 100:x + w +20])
    cv2.imwrite('varylengthred.png', cv2.UMat.get(red_org)[y :y + h , x :x + w])
    return result_string

def get_result_address(red, langset, org_img, custom_config=''):
    red_org = red
    # cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(contours))
    # 描边一次可以减少噪点
    cv2.drawContours(red, image, -1, (255, 255, 255), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    numset_contours = []
    height_list = []
    width_list = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        height_list.append(h)
        # print(h,w)
        width_list.append(w)
    height_list.remove(max(height_list))
    width_list.remove(max(width_list))
    height_threshold = 0.70 * max(height_list)
    width_threshold = 1.4 * max(width_list)
    # print('height_threshold:'+str(height_threshold)+'width_threshold:'+str(width_threshold))
    big_rect = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > height_threshold and w < width_threshold:
            # print(h,w)
            numset_contours.append((x, y, w, h))
            big_rect.append((x, y))
            big_rect.append((x + w, y + h))
    big_rect_nparray = np.array(big_rect, ndmin=3)
    x, y, w, h = cv2.boundingRect(big_rect_nparray)

    # imgrect = cv2.rectangle(color_img, (x - 10, y - 20), (x + w + 500, y + h), (0, 255, 0), 2)
    # showimg(imgrect)


    # showimg(cv2.UMat.get(org_img)[y-20:y + h + 20, x + 20:x + w +20])

    result_string = ''
    result_string += pytesseract.image_to_string(cv2.UMat.get(red_org)[y - 20 :y + h, x + 100:x + w +20],
                                                 langset,
                                                 custom_config)

    # print(result_string)
    # cv2.imwrite('varylength.png', cv2.UMat.get(org_img)[y  :y + h , x :x + w])
    # cv2.imwrite('varylengthred.png', cv2.UMat.get(red_org)[y :y + h , x :x + w])
    return result_string

def get_result_birthday(red, langset, org_img, custom_config=''):
    red_org = red
    # cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(contours))
    # 描边一次可以减少噪点
    cv2.drawContours(red, image, -1, (255, 255, 255), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    numset_contours = []
    height_list = []
    width_list = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        height_list.append(h)
        # print(h,w)
        width_list.append(w)
    height_list.remove(max(height_list))
    width_list.remove(max(width_list))
    height_threshold = 0.70 * max(height_list)
    width_threshold = 1.4 * max(width_list)
    # print('height_threshold:'+str(height_threshold)+'width_threshold:'+str(width_threshold))
    big_rect = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > height_threshold and w < width_threshold:
            # print(h,w)
            numset_contours.append((x, y, w, h))
            big_rect.append((x, y))
            big_rect.append((x + w, y + h))
    big_rect_nparray = np.array(big_rect, ndmin=3)
    x, y, w, h = cv2.boundingRect(big_rect_nparray)

    imgrect = cv2.rectangle(color_img, (x - 10, y - 20), (x + w + 10, y + h), (0, 255, 0), 2)
    showimg(imgrect)


    # showimg(cv2.UMat.get(org_img)[y-20:y + h + 20, x + 20:x + w +20])

    result_string = ''
    result_string += pytesseract.image_to_string(cv2.UMat.get(imgrect)[y:y + h, x:x + w],
                                                 langset,
                                                 custom_config)

    # print(result_string)
    # cv2.imwrite('varylength.png', cv2.UMat.get(org_img)[y  :y + h , x :x + w])
    # cv2.imwrite('varylengthred.png', cv2.UMat.get(red_org)[y :y + h , x :x + w])
    return result_string

def get_result_name_length(red, langset, org_img, custom_config=''):
    red_org = red
    # cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 描边一次可以减少噪点
    cv2.drawContours(red, image, -1, (255, 255, 255), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    numset_contours = []
    height_list = []
    width_list = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        height_list.append(h)
        # print(h,w)
        width_list.append(w)
    height_list.remove(max(height_list))
    width_list.remove(max(width_list))
    height_threshold = 0.70 * max(height_list)
    width_threshold = 1.4 * max(width_list)
    # print('height_threshold:'+str(height_threshold)+'width_threshold:'+str(width_threshold))
    big_rect = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > height_threshold and w < width_threshold:
            # print(h,w)
            numset_contours.append((x, y, w, h))
            big_rect.append((x, y))
            big_rect.append((x + w, y + h))
    big_rect_nparray = np.array(big_rect, ndmin=3)
    x, y, w, h = cv2.boundingRect(big_rect_nparray)

    imgrect = cv2.rectangle(color_img, (x - 200, y ), (x + w, y + h), (0, 255, 0), 2)
    # showimg(imgrect)
    # showimg(cv2.UMat.get(org_img)[y-20:y + h + 20, x + 20:x + w +20])

    result_string = ''
    result_string += pytesseract.image_to_string(cv2.UMat.get(imgrect)[y :y + h + 70, x - 50:x + w+100],
                                                 langset,
                                                 custom_config)

    print(result_string)
    # cv2.imwrite('varylength.png', cv2.UMat.get(org_img)[y :y + h + 70, x - 100:x + w+100])
    # cv2.imwrite('varylengthred.png', cv2.UMat.get(red_org)[y :y + h , x - 50:x + w])
    return result_string

def get_result_lastname(red, langset, org_img, custom_config=''):
    red_org = red
    # cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 描边一次可以减少噪点
    cv2.drawContours(red, image, -1, (255, 255, 255), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    numset_contours = []
    height_list = []
    width_list = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        height_list.append(h)
        # print(h,w)
        width_list.append(w)
    height_list.remove(max(height_list))
    width_list.remove(max(width_list))
    height_threshold = 0.70 * max(height_list)
    width_threshold = 1.4 * max(width_list)
    # print('height_threshold:'+str(height_threshold)+'width_threshold:'+str(width_threshold))
    big_rect = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > height_threshold and w < width_threshold:
            # print(h,w)
            numset_contours.append((x, y, w, h))
            big_rect.append((x, y))
            big_rect.append((x + w, y + h))
    big_rect_nparray = np.array(big_rect, ndmin=3)
    x, y, w, h = cv2.boundingRect(big_rect_nparray)

    imgrect = cv2.rectangle(color_img, (x , y ), (x + w, y + h ), (0, 255, 0), 2)
    showimg(imgrect)
    # showimg(cv2.UMat.get(org_img)[y-20:y + h + 20, x + 20:x + w +20])

    result_string = ''
    result_string += pytesseract.image_to_string(cv2.UMat.get(imgrect)[y :y + h , x :x + w],
                                                 langset,
                                                 custom_config)

    print(result_string)
    # cv2.imwrite('varylength.png', cv2.UMat.get(org_img)[y :y + h + 70, x - 100:x + w+100])
    # cv2.imwrite('varylengthred.png', cv2.UMat.get(red_org)[y :y + h , x - 50:x + w])
    return result_string

def get_result_firstname(red, langset, org_img, custom_config=''):
    red_org = red
    # cv2.fastNlMeansDenoising(red, red, 4, 7, 35)
    rec, red = cv2.threshold(red, 127, 255, cv2.THRESH_BINARY_INV)
    image, contours = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 描边一次可以减少噪点
    cv2.drawContours(red, image, -1, (255, 255, 255), 1)
    color_img = cv2.cvtColor(red, cv2.COLOR_GRAY2BGR)
    numset_contours = []
    height_list = []
    width_list = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        height_list.append(h)
        # print(h,w)
        width_list.append(w)
    height_list.remove(max(height_list))
    width_list.remove(max(width_list))
    height_threshold = 0.70 * max(height_list)
    width_threshold = 1.4 * max(width_list)
    # print('height_threshold:'+str(height_threshold)+'width_threshold:'+str(width_threshold))
    big_rect = []
    for cnt in image:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > height_threshold and w < width_threshold:
            # print(h,w)
            numset_contours.append((x, y, w, h))
            big_rect.append((x, y))
            big_rect.append((x + w, y + h))
    big_rect_nparray = np.array(big_rect, ndmin=3)
    x, y, w, h = cv2.boundingRect(big_rect_nparray)

    imgrect = cv2.rectangle(color_img, (x , y ), (x + w, y + h), (0, 255, 0), 2)
    showimg(imgrect)
    # showimg(cv2.UMat.get(org_img)[y-20:y + h + 20, x + 20:x + w +20])

    result_string = ''
    result_string += pytesseract.image_to_string(cv2.UMat.get(imgrect)[y :y + h + 70, x - 50:x + w+100],
                                                 langset,
                                                 custom_config)

    print(result_string)
    # cv2.imwrite('varylength.png', cv2.UMat.get(imgrect)[y  :y + h +500 , x - 200:x +100 ])
    # cv2.imwrite('varylengthred.png', cv2.UMat.get(imgrect)[y :y + h , x - 50:x + w])
    return result_string

def punc_filter(str):
    temp = str
    xx = u"([\u4e00-\u9fff0-9A-Z]+)"
    pattern = re.compile(xx)
    results = pattern.findall(temp)
    string = ""
    for result in results:
        string += result
    return string

# 这里使用直方图拉伸，不是直方图均衡
def hist_equal(img):
    # clahe_size = 8
    # clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(clahe_size, clahe_size))
    # result = clahe.apply(img)
    # test

    # result = cv2.equalizeHist(img)

    image = img.get()  # UMat to Mat
    # result = cv2.equalizeHist(image)
    lut = np.zeros(256, dtype=image.dtype)  # 创建空的查找表
    # lut = np.zeros(256)
    hist = cv2.calcHist([image],  # 计算图像的直方图
                        [0],  # 使用的通道
                        None,  # 没有使用mask
                        [256],  # it is a 1D histogram
                        [0, 256])
    minBinNo, maxBinNo = 0, 255
    # 计算从左起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(hist):
        if binValue != 0:
            minBinNo = binNo
            break
    # 计算从右起第一个不为0的直方图柱的位置
    for binNo, binValue in enumerate(reversed(hist)):
        if binValue != 0:
            maxBinNo = 255 - binNo
            break
    # print minBinNo, maxBinNo
    # 生成查找表
    for i, v in enumerate(lut):
        if i < minBinNo:
            lut[i] = 0
        elif i > maxBinNo:
            lut[i] = 255
        else:
            lut[i] = int(255.0 * (i - minBinNo) / (maxBinNo - minBinNo) + 0.5)
    # 计算,调用OpenCV cv2.LUT函数,参数 image --  输入图像，lut -- 查找表
    # print lut
    result = cv2.LUT(image, lut)
    # print type(result)
    # showimg(result)
    return cv2.UMat(result)

# image check

# def idimagecheck(imgname ,imgcheck, mode=1):
#
#     print(u'เริ่มต้นการเช็คตัวตน...')
#     if mode == 1:
#         # generate_mask(x)
#         img_data_gray, img_org = img_resize_gray(imgname)
#         name_pic = find_name(img_data_gray, img_org)
#
#
#
#     elif mode == 0:
#
#
#     else:
#         print(u"模式选择错误！")
#
#
#     return

# def Check_part():
#
#     template = cv2.UMat(cv2.imread(image_for_check))
#     use = cv2.UMat(cv2.imread(image_for_use))
#
#     res = cv2.matchTemplate(use, template, cv2.TM_CCOEFF_NORMED)
#     conf = res.max()
#
#     print(conf)
#     # for name in test:
#     #     img = (cv2.imread(name, 0))
#     #     print(f"Confidence for {name:}")
#     #     # result =
#     #     print(cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED).max())





if __name__ == "__main__":

    image_for_use = 'testimages/112.jpg'
    idocr = idcardocr(cv2.UMat(cv2.imread(image_for_use)))

    # image_for_check = 'testiamges/322.jpg'
    # test = [image_for_check]
    # Check_part()
    # idcheck = idimagecheck(cv2.UMat(cv2.imread(image_for_use)), cv2.UMat(cv2.imread(image_for_check)))

    print(idocr)
    # for i in range(15):
    #     idocr = idcardocr(cv2.UMat(cv2.imread('testimages/%s.jpg'%(i+1))))
    #     print(idocr['idnum'])

