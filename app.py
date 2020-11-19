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
from fitur_tekstur import contrast, energy,entropy, homogeneity, check_value

app = Flask(__name__)

##########################################################################################################
def mean(data):
    a = str(round(sum(data) / len(data), 2))
    print('Mean data adalah ', a)
    return

##########################################################################################################

##########################################################################################################
#koneksi db
def opendb(): 
    global conn, cursor
    conn = mysql.connector.connect(
        user='root',
        password='',
        database = 'db_tarimpang',
        host = '127.0.0.1'
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
@app.route('/ekstraksi_fitur',  methods=['GET','POST'])
def ekstraksi_fitur():
    if request.method == 'GET':
        opendb()
        cursor.execute('select * from tb_data')
        result= []
        for id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status in cursor.fetchall():
            result.append((id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropys, contrasts, energys, homogeneitys, target, status))

        closedb()
        return render_template('ekstraksi_fitur.html',result=result) 
    else:
        citra = request.files['file']#mengambil filename gambar
        
        img = cv2.imdecode(np.fromstring(request.files['file'].read(),np.uint8),cv2.IMREAD_UNCHANGED) #membuat vaiable dari name
        # # histogram
        data = histogram(img)

        # # Tekstur
        data_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


        h=0
        w=0
        h,w = data_img.shape
        result = check_value(data_img,h,w)
        result = np.array(result)
        glcm = np.unique(result,return_counts=True,axis=0)
        count_glcm = np.sum(glcm[1])
        avg_glcm= glcm[1]/count_glcm
        data_glcm = {'key':glcm[0],'val':glcm[1],'norm':avg_glcm}

        ent = entropy(data_glcm)
        ctr = contrast(data_glcm)
        eng = energy(data_glcm)
        hmg = homogeneity(data_glcm)
        target = request.form['Target']
        
        #input database
        datas=(citra.filename, str(data[6]), str(data[7]), str(data[8]), str(data[3]), str(data[4]), str(data[5]), str(data[0]), str(data[1]),str(data[2]),str(ent),str(ctr),str(eng),str(hmg),str(target))
        
        opendb()
        cursor.execute('''insert into  `tb_data`(`nama`, `red1`, `red2`, `red3`, `green1`, `green2`, `green3`, `blue1`, `blue2`, `blue3`, `entropy`, `contrast`, `energy`, `homogeneity`, `target`, `status`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','1')'''% datas)
        
        # Select semua data (tabel)
        # cursor.execute('select * from tb_data')
        # result= []
        # for id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
        #     result.append((id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status))

        conn.commit()
        closedb()
    
    return render_template('ekstraksi_fitur.html')
##########################################################################################################
@app.route('/tampil_data')
def tampil_data():
    return render_template('tampil_data.html')
##########################################################################################################
@app.route('/testing',  methods=['GET','POST'])
def testing():

    if request.method == 'POST':
       
        datas = []
        data_uji = []
        Target1 = []
        Target2 = []
        mean=None
        jahe = 0
        kencur = 0
        kunyit = 0
        lengkuas = 0

        opendb()
        # =============DATA==================
        cursor.execute('select * from tb_data where status = 1')
        # cursor.execute('select target, count(target) as jumlah from tb_data group by target')
        for id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            datas.append([red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity])
            Target1.append(target)
           
        # ===============MEAN===============
        mean = np.array(Target1)
        res = (np.unique(mean,axis=0,return_counts=True))
        avg = res[1]/sum(res[1])
        print('res : ', res)
        print('mean : ', avg)


        # =============UJI==================
        cursor.execute('select * from tb_data where status = 2')
        for id_data,nama, red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity, target, status in cursor.fetchall():
            data_uji.append([red1, red2, red3, green1, green2, green3, blue1, blue2, blue3, entropy, contrast, energy, homogeneity])
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
    
    app.run(debug=True)#mode debug  agar tidak perlu ctrl-c   (tidak perlssu logout dulus)