from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import cv2
import mysql.connector
import numpy as np
import pandas as pd
import math
import timeit
import collections as cl
# import pdfkit
from matplotlib import pyplot as plt
# from fpdf import FPDF

from fitur_warna import histogram
from fitur_tekstur import contrast, energy, entropy, homogeneity, check_value

app = Flask(__name__)

##########################################################################################################


def mean(data):
    a = str(round(sum(data) / len(data), 2))
    return a

##########################################################################################################

##########################################################################################################
# koneksi db


def opendb():
    global conn, cursor
    conn = mysql.connector.connect(
        user='root',
        password='',
        database='db_tarimpang',
        host='127.0.0.1'
    )
    cursor = conn.cursor()


def closedb():
    global conn, cursor
    conn.close()
    cursor.close()
##########################################################################################################
##########################################################################################################

##########################################################################################################

##########################################################################################################


@app.route('/')
def index():
    return render_template('home.html')
##########################################################################################################


@app.route('/ekstraksi_fitur',  methods=['GET', 'POST'])
def ekstraksi_fitur():
    if request.method == 'GET':
        opendb()
        cursor.execute('select * from tb_data')
        result = []
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status in cursor.fetchall():
            result.append((id_data, nama, red1, red2, red3, green1, green2, green3, blue1,
                           blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status))

        closedb()
        return render_template('ekstraksi_fitur.html', result=result)
    else:
        citra = request.files['file']  # mengambil filename gambar

        img = cv2.imdecode(np.fromstring(request.files['file'].read(
        ), np.uint8), cv2.IMREAD_UNCHANGED)  # membuat vaiable dari name
        # # histogram
        data = histogram(img)

        # # Tekstur
        data_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h = 0
        w = 0
        h, w = data_img.shape
        result = check_value(data_img, h, w)
        result = np.array(result)
        glcm = np.unique(result, return_counts=True, axis=0)
        count_glcm = np.sum(glcm[1])
        avg_glcm = glcm[1]/count_glcm
        data_glcm = {'key': glcm[0], 'val': glcm[1], 'norm': avg_glcm}

        ent = entropy(data_glcm)
        ctr = contrast(data_glcm)
        eng = energy(data_glcm)
        hmg = homogeneity(data_glcm)
        target = request.form['Target']

        # input database
        datas = (citra.filename, str(data[6]), str(data[7]), str(data[8]), str(data[3]), str(data[4]), str(
            data[5]), str(data[0]), str(data[1]), str(data[2]), str(ent), str(ctr), str(eng), str(hmg), str(target))

        opendb()
        cursor.execute('''insert into  `tb_data`(`nama`, `red1`, `red2`, `red3`, `green1`, `green2`, `green3`, `blue1`, `blue2`, `blue3`, `entropy`, `contrast`, `energy`, `homogeneity`, `target`, `status`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','1')''' % datas)

        # Select semua data (tabel)
        # cursor.execute('select * from tb_data')
        # result= []
        # for id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
        #     result.append((id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status))

        conn.commit()
        closedb()

    return render_template('ekstraksi_fitur.html')
##########################################################################################################


@app.route('/tampil_data',  methods=['GET'])
def tampil_data():

    opendb()
    cursor.execute('select * from tb_data where status = 1')
    result = []
    for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status in cursor.fetchall():
        result.append((id_data, nama, red1, red2, red3, green1, green2, green3, blue1,
                       blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status))
    cursor.execute('select * from tb_data where status = 2')
    res = []
    for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status in cursor.fetchall():
        res.append((id_data, nama, red1, red2, red3, green1, green2, green3, blue1,
                    blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status))

    closedb()

    return render_template('tampil_data.html', result=result, res=res)
##########################################################################################################


@app.route('/testing',  methods=['GET', 'POST'])
def testing():

    if request.method == 'POST':

        datas = []
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data_uji = []
        Target1 = []
        Target2 = []

        x = None

        opendb()
        # =============DATA==================
        cursor.execute('select * from tb_data where status = 1')
        # cursor.execute('select target, count(target) as jumlah from tb_data group by target')
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            datas.append([red1, red2, red3, green1, green2, green3, blue1,
                          blue2, blue3, entropy, contrast, energy, homogeneity])
            Target1.append(target)

        cursor.execute(
            'select * from tb_data where `target` = 1 and status = 1')
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            data1.append([red1, red2, red3, green1, green2, green3, blue1,
                          blue2, blue3, entropy, contrast, energy, homogeneity])

        cursor.execute(
            'select * from tb_data where `target` = 2 and status = 1')
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            data2.append([red1, red2, red3, green1, green2, green3, blue1,
                          blue2, blue3, entropy, contrast, energy, homogeneity])

        cursor.execute(
            'select * from tb_data where `target` = 3 and status = 1')
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            data3.append([red1, red2, red3, green1, green2, green3, blue1,
                          blue2, blue3, entropy, contrast, energy, homogeneity])

        cursor.execute(
            'select * from tb_data where `target` = 4 and status = 1')
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            data4.append([red1, red2, red3, green1, green2, green3, blue1,
                          blue2, blue3, entropy, contrast, energy, homogeneity])

        # ===============MEAN========  =======
        x = np.array(Target1)
        res = (np.unique(x, axis=0, return_counts=True))
        avg = res[1]/sum(res[1])
        print('res : ', res)
        print('mean : ', avg)

        # print('data :',datas)
        mean01 = 0
        mean1 = 0
        mean2 = 0
        mean3 = 0
        mean4 = 0
        mean5 = 0
        mean6 = 0
        mean7 = 0
        mean8 = 0
        mean9 = 0
        mean10 = 0
        mean11 = 0
        mean12 = 0
        mean13 = 0

        # ========================================================================
        for i in range(len(data1)):
            mean01 = (data1[i][0] + data1[i][0])/res[1][0]
            # print('data1 :',data1[i][0])
        print('mean1 :', mean01)

        for i in range(len(data1)):
            mean2 = (data1[i][1] + data1[i][1])/res[1][0]
            # print('data2 :',data1[i][1])
        print('mean2 :', mean2)

        for i in range(len(data1)):
            mean3 = (data1[i][2] + data1[i][2])/res[1][0]
            # print('data3 :',data1[i][2])
        print('mean3 :', mean3)

        for i in range(len(data1)):
            mean4 = (data1[i][3] + data1[i][3])/res[1][0]
            # print('data4 :',data1[i][3])
        print('mean4 :', mean4)

        for i in range(len(data1)):
            mean5 = (data1[i][4] + data1[i][4])/res[1][0]
            # print('data5 :',data1[i][4])
        print('mean5 :', mean5)

        for i in range(len(data1)):
            mean6 = (data1[i][5] + data1[i][5])/res[1][0]
            # print('data6 :',data1[i][5])
        print('mean6 :', mean6)

        for i in range(len(data1)):
            mean7 = (data1[i][6] + data1[i][6])/res[1][0]
            # print('data7 :',data1[i][6])
        print('mean7 :', mean7)

        for i in range(len(data1)):
            mean8 = (data1[i][7] + data1[i][7])/res[1][0]
            # print('data8 :',data1[i][7])
        print('mean8 :', mean8)

        for i in range(len(data1)):
            mean9 = (data1[i][8] + data1[i][8])/res[1][0]
            # print('data9 :',data1[i][8])
        print('mean9 :', mean9)

        for i in range(len(data1)):
            mean10 = (data1[i][9] + data1[i][9])/res[1][0]
            # print('data10 :',data1[i][9])
        print('mean10 :', mean10)

        for i in range(len(data1)):
            mean11 = (data1[i][10] + data1[i][10])/res[1][0]
            # print('data11 :',data1[i][10])
        print('mean11 :', mean11)

        for i in range(len(data1)):
            mean12 = (data1[i][11] + data1[i][11])/res[1][0]
            # print('data12 :',data1[i][11])
        print('mean12 :', mean12)

        for i in range(len(data1)):
            mean13 = (data1[i][12] + data1[i][12])/res[1][0]
            # print('data13 :',data1[i][12])
        print('mean13 :', mean13)
        # ========================================================================
        # ========================================================================
        for i in range(len(data2)):
            mean1 = (data2[i][0] + data2[i][0])/res[1][1]
            # print('data1 :',data2[i][0])
        print('mean1 :', mean1)

        for i in range(len(data2)):
            mean2 = (data2[i][1] + data2[i][1])/res[1][1]
            # print('data2 :',data2[i][1])
        print('mean2 :', mean2)

        for i in range(len(data2)):
            mean3 = (data2[i][2] + data2[i][2])/res[1][1]
            # print('data3 :',data2[i][2])
        print('mean3 :', mean3)

        for i in range(len(data2)):
            mean4 = (data2[i][3] + data2[i][3])/res[1][1]
            # print('data4 :',data2[i][3])
        print('mean4 :', mean4)

        for i in range(len(data2)):
            mean5 = (data2[i][4] + data2[i][4])/res[1][1]
            # print('data5 :',data2[i][4])
        print('mean5 :', mean5)

        for i in range(len(data2)):
            mean6 = (data2[i][5] + data2[i][5])/res[1][1]
            # print('data6 :',data2[i][5])
        print('mean6 :', mean6)

        for i in range(len(data2)):
            mean7 = (data2[i][6] + data2[i][6])/res[1][1]
            # print('data7 :',data2[i][6])
        print('mean7 :', mean7)

        for i in range(len(data2)):
            mean8 = (data2[i][7] + data2[i][7])/res[1][1]
            # print('data8 :',data2[i][7])
        print('mean8 :', mean8)

        for i in range(len(data2)):
            mean9 = (data2[i][8] + data2[i][8])/res[1][1]
            # print('data9 :',data2[i][8])
        print('mean9 :', mean9)

        for i in range(len(data2)):
            mean10 = (data2[i][9] + data2[i][9])/res[1][1]
            # print('data10 :',data2[i][9])
        print('mean10 :', mean10)

        for i in range(len(data2)):
            mean11 = (data2[i][10] + data2[i][10])/res[1][1]
            # print('data11 :',data2[i][10])
        print('mean11 :', mean11)

        for i in range(len(data2)):
            mean12 = (data2[i][11] + data2[i][11])/res[1][1]
            # print('data12 :',data2[i][11])
        print('mean12 :', mean12)

        for i in range(len(data2)):
            mean13 = (data2[i][12] + data2[i][12])/res[1][1]
            # print('data13 :',data2[i][12])
        print('mean13 :', mean13)
        # ========================================================================
        # ========================================================================
        for i in range(len(data3)):
            mean1 = (data3[i][0] + data3[i][0])/res[1][2]
            # print('data1 :',data3[i][0])
        print('mean1 :', mean1)

        for i in range(len(data3)):
            mean2 = (data3[i][1] + data3[i][1])/res[1][2]
            # print('data3 :',data3[i][1])
        print('mean2 :', mean2)

        for i in range(len(data3)):
            mean3 = (data3[i][2] + data3[i][2])/res[1][2]
            # print('data3 :',data3[i][2])
        print('mean3 :', mean3)

        for i in range(len(data3)):
            mean4 = (data3[i][3] + data3[i][3])/res[1][2]
            # print('data4 :',data3[i][3])
        print('mean4 :', mean4)

        for i in range(len(data3)):
            mean5 = (data3[i][4] + data3[i][4])/res[1][2]
            # print('data5 :',data3[i][4])
        print('mean5 :', mean5)

        for i in range(len(data3)):
            mean6 = (data3[i][5] + data3[i][5])/res[1][2]
            # print('data6 :',data3[i][5])
        print('mean6 :', mean6)

        for i in range(len(data3)):
            mean7 = (data3[i][6] + data3[i][6])/res[1][2]
            # print('data7 :',data3[i][6])
        print('mean7 :', mean7)

        for i in range(len(data3)):
            mean8 = (data3[i][7] + data3[i][7])/res[1][2]
            # print('data8 :',data3[i][7])
        print('mean8 :', mean8)

        for i in range(len(data3)):
            mean9 = (data3[i][8] + data3[i][8])/res[1][2]
            # print('data9 :',data3[i][8])
        print('mean9 :', mean9)

        for i in range(len(data3)):
            mean10 = (data3[i][9] + data3[i][9])/res[1][2]
            # print('data10 :',data3[i][9])
        print('mean10 :', mean10)

        for i in range(len(data3)):
            mean11 = (data3[i][10] + data3[i][10])/res[1][2]
            # print('data11 :',data3[i][10])
        print('mean11 :', mean11)

        for i in range(len(data3)):
            mean12 = (data3[i][11] + data3[i][11])/res[1][2]
            # print('data12 :',data3[i][11])
        print('mean12 :', mean12)

        for i in range(len(data3)):
            mean13 = (data3[i][12] + data3[i][12])/res[1][2]
            # print('data13 :',data3[i][12])
        print('mean13 :', mean13)
        # ========================================================================
        # ========================================================================
        for i in range(len(data4)):
            mean1 = (data4[i][0] + data4[i][0])/res[1][3]
            # print('data1 :',data4[i][0])
        print('mean1 :', mean1)

        for i in range(len(data4)):
            mean2 = (data4[i][1] + data4[i][1])/res[1][3]
            # print('data4 :',data4[i][1])
        print('mean2 :', mean2)

        for i in range(len(data4)):
            mean3 = (data4[i][2] + data4[i][2])/res[1][3]
            # print('data3 :',data4[i][2])
        print('mean3 :', mean3)

        for i in range(len(data4)):
            mean4 = (data4[i][3] + data4[i][3])/res[1][3]
            # print('data4 :',data4[i][3])
        print('mean4 :', mean4)

        for i in range(len(data4)):
            mean5 = (data4[i][4] + data4[i][4])/res[1][3]
            # print('data5 :',data4[i][4])
        print('mean5 :', mean5)

        for i in range(len(data4)):
            mean6 = (data4[i][5] + data4[i][5])/res[1][3]
            # print('data6 :',data4[i][5])
        print('mean6 :', mean6)

        for i in range(len(data4)):
            mean7 = (data4[i][6] + data4[i][6])/res[1][3]
            # print('data7 :',data4[i][6])
        print('mean7 :', mean7)

        for i in range(len(data4)):
            mean8 = (data4[i][7] + data4[i][7])/res[1][3]
            # print('data8 :',data4[i][7])
        print('mean8 :', mean8)

        for i in range(len(data4)):
            mean9 = (data4[i][8] + data4[i][8])/res[1][3]
            # print('data9 :',data4[i][8])
        print('mean9 :', mean9)

        for i in range(len(data4)):
            mean10 = (data4[i][9] + data4[i][9])/res[1][3]
            # print('data10 :',data4[i][9])
        print('mean10 :', mean10)

        for i in range(len(data4)):
            mean11 = (data4[i][10] + data4[i][10])/res[1][3]
            # print('data11 :',data4[i][10])
        print('mean11 :', mean11)

        for i in range(len(data4)):
            mean12 = (data4[i][11] + data4[i][11])/res[1][3]
            # print('data12 :',data4[i][11])
        print('mean12 :', mean12)

        for i in range(len(data4)):
            mean13 = (data4[i][12] + data4[i][12])/res[1][3]
            # print('data13 :',data4[i][12])
        print('mean13 :', mean13)
        # ========================================================================
        # standar deviasi
        std1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean01)**2)/(res[1][0] - 1)
            print('data 1: ', data1[i][0])
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)
        sd1 = 0
        for i in range(len(data1)):
            sd1 = math.sqrt((data1[i][0] - mean1)**2)/(res[1][0] - 1)
        print('standev 1 :', std1)

        # =============UJI==================
        cursor.execute('select * from tb_data where status = 2')
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            data_uji.append([red1, red2, red3, green1, green2, green3,
                             blue1, blue2, blue3, entropy, contrast, energy, homogeneity])
            Target2.append(target)
        ############################################################################################################################
        # ==================NBC==================

        closedb()
        return render_template('testing.html')
    else:

        return render_template('testing.html')
##########################################################################################################

##########################################################################################################

##########################################################################################################


##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    # mode debug  agar tidak perlu ctrl-c   (tidak perlssu logout dulus)
    app.run(debug=True)
