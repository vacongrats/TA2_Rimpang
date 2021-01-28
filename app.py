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
        database='db_tarimpang2',
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

        return render_template('ekstraksi_fitur.html')
    else:
        citra = request.files['file']  # mengambil filename gambar

        img = cv2.imdecode(np.fromstring(request.files['file'].read(
        ), np.uint8), cv2.IMREAD_UNCHANGED)  # membuat vaiable dari name
        # img = citra1[150:300, 200:350]
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
        cursor.execute('''insert into  `tb_data`(`nama`, `red1`, `red2`, `red3`, `green1`, `green2`, `green3`, `blue1`, `blue2`, `blue3`, `entropy`, `contrast`, `energy`, `homogeneity`, `target`, `status`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','2')''' % datas)
        cursor.execute(
            'select * from `tb_data` where id_data order by id_data desc limit 1')
        result = []
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropys, contrasts, energys, homogeneitys, targets, status in cursor.fetchall():
            result.append((id_data, nama, red1, red2, red3, green1, green2, green3, blue1,
                           blue2, blue3, entropys, contrasts, energys, homogeneitys, targets, status))

        conn.commit()
        closedb()

    return render_template('ekstraksi_fitur.html', result=result)
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


@app.route('/training', methods=['POST'])
def training():
    opendb()
    cursor.execute('select * from tb_data where status = 2 ')
    for d in cursor.fetchall():
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

            kelas_mean = str(i)
            datas_mean = (kelas_mean, str(mean[0]), str(mean[1]), str(mean[2]), str(mean[3]), str(mean[4]),
                          str(mean[5]), str(mean[6]), str(mean[7]), str(mean[8]), str(mean[9]), str(mean[10]), str(mean[11]), str(mean[12]))
            cek = []
            # ==================DB====================
            cursor.execute(
                "select * from tb_mean where kelas=%s" % kelas_mean)
            for id_mean, kelas_mean, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity in cursor.fetchall():
                cek.append([kelas_mean, red1, red2, red3, green1, green2, green3,
                            blue1, blue2, blue3, entropy, contrast, energy, homogeneity])
            if len(cek) == 0:
                cursor.execute(
                    "insert into tb_mean(kelas, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')", datas_mean)
            else:
                cursor.execute(
                    "update tb_mean set red1=%s, red2=%s, red3=%s, green1=%s, green2=%s, green3=%s, blue1=%s, blue2=%s, blue3=%s, entropy=%s, contrast=%s, energy=%s, homogeneity=%s where kelas=%s", (
                        str(mean[0]), str(mean[1]), str(mean[2]), str(mean[3]), str(mean[4]), str(mean[5]), str(mean[6]), str(mean[7]), str(mean[8]), str(mean[9]), str(mean[10]), str(mean[11]), str(mean[12]),  kelas_mean)
                )
            conn.commit()

            # =================STANDARDEVIASI====================
            std_dev = np.sqrt(
                sum((data_latih-mean)**2)/(len(data_latih)-1))

            kelas_standev = str(i)
            datas_standev = (kelas_standev, str(std_dev[0]), str(std_dev[1]), str(std_dev[2]), str(std_dev[3]), str(std_dev[4]),
                             str(std_dev[5]), str(std_dev[6]), str(std_dev[7]), str(std_dev[8]), str(std_dev[9]), str(std_dev[10]), str(std_dev[11]), str(std_dev[12]))
            cek2 = []
            # ==================DB====================
            cursor.execute(
                "select * from tb_standev where kelas=%s" % kelas_standev)
            for id_standev, kelas_standev, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity in cursor.fetchall():
                cek2.append([kelas_standev, red1, red2, red3, green1, green2, green3,
                             blue1, blue2, blue3, entropy, contrast, energy, homogeneity])
            if len(cek2) == 0:
                cursor.execute(
                    "insert into tb_standev (kelas, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", datas_standev)
            else:
                cursor.execute(
                    "update tb_standev set red1=%s, red2=%s, red3=%s, green1=%s, green2=%s, green3=%s, blue1=%s, blue2=%s, blue3=%s, entropy=%s, contrast=%s, energy=%s, homogeneity=%s where kelas=%s", (
                        str(std_dev[0]), str(std_dev[1]), str(std_dev[2]), str(std_dev[3]), str(std_dev[4]), str(std_dev[5]), str(std_dev[6]), str(std_dev[7]), str(std_dev[8]), str(std_dev[9]), str(std_dev[10]), str(std_dev[11]), str(std_dev[12]),  kelas_standev))
            conn.commit()
    closedb()
    return render_template('testing.html')


@app.route('/testing',  methods=['GET', 'POST'])
def testing():
    if request.method == 'POST':
        eks = 2.71828183
        phi = 3.14159

        opendb()

        benar = 0
        salah = 0
        benar_j = 0
        salah_j = 0
        benar_ke = 0
        salah_ke = 0
        benar_ku = 0
        salah_ku = 0
        benar_l = 0
        salah_l = 0
        akurasi = 0
        error = 0
        cm_benar = 0
        cm_salah = 0
        prediksi = []
        prediksi1 = []

        cursor.execute('select * from tb_data where status = 2 ')
        for d in cursor.fetchall():
            # target_uji.append(data[-2])
            se = d[-2]
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
                # ====================DENSITAS=======================
                mean_sql = None
                std_dev_sql = None
                cursor.execute(
                    "select * from tb_mean where kelas=%s limit 1" % (str(i)))
                mean_sql = cursor.fetchone()
                cursor.execute(
                    "select * from tb_standev where kelas=%s limit 1" % (str(i)))
                std_dev_sql = cursor.fetchone()

                mean = np.array(mean_sql[2:])
                std_dev = np.array(std_dev_sql[2:])

                eks_p = -(((uji-mean)**2)/(2*(std_dev)**2))

                p = (1/(np.sqrt(2*phi)*std_dev))*eks**eks_p
                result.append(p)
                # print("pro : ", p)

            # ===================Kelas Pemenang======================
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

            if wk is se:
                prediksi.append((wk, 0))
                benar += 1
            else:
                prediksi.append((wk, 1))
                salah += 1

            # =============================================
            if ((wk == 1) and (se == 1)):
                prediksi1.append(((wk == 1), 0))
                benar_j += 1
            if ((wk != 1) and (se == 1)):
                prediksi1.append(((wk == 1), 1))
                salah_j += 1

            if ((wk == 2) and (se == 2)):
                prediksi1.append(((wk == 2), 0))
                benar_ke += 1
            if ((wk != 2) and (se == 2)):
                prediksi1.append(((wk == 2), 1))
                salah_ke += 1

            if ((wk == 3) and (se == 3)):
                prediksi1.append(((wk == 3), 0))
                benar_ku += 1
            if ((wk != 3) and (se == 3)):
                prediksi1.append(((wk == 3), 1))
                salah_ku += 1

            if ((wk == 4) and (se == 4)):
                prediksi1.append(((wk == 4), 0))
                benar_l += 1
            if ((wk != 4) and (se == 4)):
                prediksi1.append(((wk == 4), 1))
                salah_l += 1

        akurasi = ((benar/(benar+salah))*100)
        error = ((salah/(benar+salah))*100)
        print("Jumlah Benar : ", benar)
        print("Jumlah Salah : ", salah)
        print('akurasi : ', akurasi, '%')
        print('error : ', error, '%')

        print("Jahe yang teridentifikasi : ", benar_j)
        print("Jahe yang tidak teridentifikasi : ", salah_j)
        print("Kencur yang teridentifikasi : ", benar_ke)
        print("Kencur yang tidak teridentifikasi : ", salah_ke)
        print("Kunyit yang teridentifikasi : ", benar_ku)
        print("Kunyit yang tidak teridentifikasi : ", salah_ku)
        print("Lengkuas  yang teridentifikasi : ", benar_l)
        print("Lengkuas yang tidak teridentifikasi : ", salah_l)
        cm_benar = ((benar_j+benar_ke+benar_ku+benar_l)/(benar+salah))
        print("Akurasi CM Benar : ", cm_benar)
        cm_salah = ((salah_j+salah_ke+salah_ku+salah_l)/(benar+salah))
        print("Akurasi CM Salah : ", cm_salah)

        cursor.execute('select * from tb_data where status = 2')
        result = []
        for id_data, nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status in cursor.fetchall():
            result.append((id_data, nama, red1, red2, red3, green1, green2, green3, blue1,
                           blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status))

        closedb()
        return render_template('testing.html', benar=benar, salah=salah, akurasi=akurasi, error=error, result=result, prediksi=prediksi, wk=wk, benar_j=benar_j, benar_ke=benar_ke, benar_ku=benar_ku, benar_l=benar_l)
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
