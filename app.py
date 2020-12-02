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
        eks = 2.71828183
        phi = 3.14159
        opendb()
        akurasi = 0
        error = 0
        cursor.execute('select * from tb_data where status = 2 ')
        for d in cursor.fetchall():
            semongko = d[-2]
            uji = []
            result = []
            uji = np.array(d[2:15])
            p_data = []
            for i in range(1, 5):
                cursor.execute(
                    'select * from tb_data where status = 1 and target = "'+str(i)+'"')
                data_latih = []
                target_latih = []
                for data in cursor.fetchall():
                    data_latih.append(data[2:15])
                    target_latih.append(data[15])
                    p_data.append(data[15])
                data_latih = np.array(data_latih)
                data_latih_transpose = np.transpose(data_latih)
                # ====================MEAN===========================
                mean = np.mean(data_latih_transpose, axis=1)
                # =================STANDARDEVIASI====================
                std_dev = np.sqrt(
                    sum((data_latih-mean)**2)/(len(data_latih)-1))
                # ====================GAUSSIAN=======================
                eks_p = -(((uji-mean)**2)/(2*(std_dev)**2))

                p = (1/(np.sqrt(2*phi)*std_dev))*eks**eks_p
                result.append(p)
            result = np.array(result)
            res_t = np.transpose(result)
            p_data = np.unique(p_data, return_counts=True)
            p_data = p_data[1]/sum(p_data[1])
            res = 1
            for i in range(len(res_t)):
                res *= res_t[i]
            ouput = res*p_data
            wk = max(ouput)
            wk = (list(ouput).index(wk)+1)
            if wk is semongko:
                akurasi += 1
            else:
                error += 1
        print('akurasi : ', (akurasi/(akurasi+error))*100, '%')
        print('error : ', (error/(akurasi+error))*100, '%')
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
