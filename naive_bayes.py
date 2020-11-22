import mysql.connector
import numpy as np

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

def pengurangan_mean_value(data,mean,key):
    print(key,' \n')
    total_data = []
    std_dev = []
    for i in range(len(mean)):
        val =0
        for j in range(len(data)):
            val += (data[j] - mean[i])**2
        std_dev.append(np.sqrt(val/(len(data)-1)))
    # print('standart deviasi : \n',std_dev)
    # print('mean : \n',mean)
    return (std_dev,mean)
opendb()
no = 0
datas =[]
data={}
eksponen = 2.71828183
phi = 3.14159
for j in range(1,5):
    data_red1 = []
    data_red2 = []
    data_red3 = []
    data_green1 = []
    data_green2 = []
    data_green3 = []
    data_blue1 = []
    data_blue2 = []
    data_blue3 = []
    ent = []
    eng =[]
    homogen = []
    contrs = []
    target = []
    cursor.execute('select * from tb_data where status = 1 and target = "'+str(j)+'"')
    for i in cursor.fetchall():
        data_red1.append(i[2])
        data_red2.append(i[3])
        data_red3.append(i[4])
        data_green1.append(i[5])
        data_green2.append(i[6])
        data_green3.append(i[7])
        data_blue1.append(i[8])
        data_blue2.append(i[9])
        data_blue3.append(i[10])
        ent.append(i[11])
        contrs.append(i[12])
        eng.append(i[13])
        homogen.append(i[14])
        target.append(i[15])
    data[j]={'red1':data_red1,
            'red2' :data_red2,
            'red3' :data_red3,
            'green1' :data_green1,
            'green2' :data_green2,
            'green3' :data_green3,
            'blue1' :data_blue1,
            'blue2' :data_blue2,
            'blue3' :data_blue3,
            'entropy' :ent,
            'contrast' :contrs,
            'energy' :eng,
            'homogeneity' :homogen,
            'target' : target
            }
mean_red1 = []
mean_red2 = []
mean_red3 = []
mean_green1 = []
mean_green2 = []
mean_green3 = []
mean_blue1 = []
mean_blue2 = []
mean_blue3 = []
mean_entropy = []
mean_contrast = []
mean_energy = []
mean_homogeneity = []
for k in range(1,5):
    mean_red1.append(sum(data[k]['red1'])/len(data[k]['red1']))    
    mean_red2.append(sum(data[k]['red2'])/len(data[k]['red2']))    
    mean_red3.append(sum(data[k]['red3'])/len(data[k]['red3']))    
    mean_green1.append(sum(data[k]['green1'])/len(data[k]['green1']))
    mean_green2.append(sum(data[k]['green2'])/len(data[k]['green2']))
    mean_green3.append(sum(data[k]['green3'])/len(data[k]['green3']))
    mean_blue1.append(sum(data[k]['blue1'])/len(data[k]['blue1']))
    mean_blue2.append(sum(data[k]['blue2'])/len(data[k]['blue2']))
    mean_blue3.append(sum(data[k]['blue3'])/len(data[k]['blue3']))
    mean_entropy.append(sum(data[k]['entropy'])/len(data[k]['entropy']))
    mean_contrast.append(sum(data[k]['contrast'])/len(data[k]['contrast']))
    mean_energy.append(sum(data[k]['energy'])/len(data[k]['energy']))
    mean_homogeneity.append(sum(data[k]['homogeneity'])/len(data[k]['homogeneity']))
# print('m red1 :',mean_red1)
# print('m red2 :',mean_red2)
# print('m red3 :',mean_red3)
# print('m green1 :',mean_green1)
# print('m green2 :',mean_green2)
# print('m green3 :',mean_green3)
# print('m blue1 :',mean_blue1)
# print('m blue2 :',mean_blue2)
# print('m blue3 :',mean_blue3)
# print('m entropy :',mean_entropy)
# print('m contrast :',mean_contrast)
# print('m energy :',mean_energy)
# print('m homogeneity :',mean_homogeneity)
cursor.execute('select * from tb_data where status = 2 LIMIT 1')
uji = cursor.fetchone()
for i in range(1,5):
    print('target',i)
    sr1,mr1 = pengurangan_mean_value(data[i]['red1'],mean_red1,'red1')
    p = (1/(np.sqrt(2*phi))*sr1[i])*eksponen - ((uji[2]-mr1[i]**2)/(2*(sr1[i])**2))
    print(p)


closedb()