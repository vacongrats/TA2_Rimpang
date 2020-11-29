import numpy as np
import mysql.connector


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
    # print(uji)
    # uji = np.array(uji[2:15])
    p_data = []
    for i in range(1, 5):
        # print('data ke : ', i)
        cursor.execute(
            'select * from tb_data where status = 1 and target = "'+str(i)+'"')
        data_latih = []
        target_latih = []
        for data in cursor.fetchall():
            data_latih.append(data[2:15])
            target_latih.append(data[15])
            p_data.append(data[15])
        # print('t :', target_latih)
        data_latih = np.array(data_latih)
        data_latih_transpose = np.transpose(data_latih)
        # ====================MEAN===========================
        mean = np.mean(data_latih_transpose, axis=1)
        # p_kelas = np.mean(target_latih)
        # print('p kls :', p_kelas)
        # =================STANDARDEVIASI====================
        std_dev = np.sqrt(sum((data_latih-mean)**2)/(len(data_latih)-1))
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
