import numpy as np
import collections as cl
import math
import cv2
# from fitur_warna import histogram


def check_value(data, h, w):
    first = []
    for i in range(0, h):
        for j in range(0, w):
            try:
                first.append([data[i, j], data[i, j+1]])
            except:
                pass
    return first


def contrast(data):
    result = 0
    for i in range(len(data['key'])):
        contrast = 0
        baris, kolom = data['key'][i]
        contrast = ((baris-kolom)**2) * data['norm'][i]
        result += contrast
    return result


def energy(data):
    result = 0
    for i in range(len(data['key'])):
        energy = 0
        energy = (data['norm'][i])**2
        result += energy
    return result


def ketetapan(data):
    if(data < 0):
        data = data * -1
    else:
        data
    return data


def homogeneity(data):
    result = 0
    for i in range(len(data['key'])):
        homogeneiti = 0
        baris, kolom = data['key'][i]
        homogeneiti = (data['norm'][i])/(1+ketetapan(baris-kolom))
        result += homogeneiti
    return result


def entropy(data):
    result = 0
    for i in range(len(data['key'])):
        entropy = 0
        entropy = -(data['norm'][i])*(math.log(data['norm'][i]))
        # print('n', data['norm'][i], 'b', math.log(data['norm'][i]))
        result += entropy
    return result


def correlation(data):
    result = 0
    rerata_baris = 0
    rerata_kolom = 0
    dev_baris = 0
    dev_kolom = 0
    res_baris = 0
    res_kolom = 0
    jumlah_kemunculan = np.sum(data['val'])

    for i in range(len(data['key'])):
        baris, kolom = data['key'][i]
        rerata_baris += baris*data['val'][i]
        rerata_kolom += kolom*data['val'][i]

    rerata_baris = rerata_baris/jumlah_kemunculan
    rerata_kolom = rerata_kolom/jumlah_kemunculan

    for i in range(len(data['key'])):
        baris, kolom = data['key'][i]
        dev_baris = (baris-rerata_baris)**2 * data['norm'][i]
        dev_kolom = (kolom-rerata_kolom)**2 * data['norm'][i]
        res_baris += dev_baris
        res_kolom += dev_kolom

    res_baris = np.sqrt(res_baris)
    res_kolom = np.sqrt(res_kolom)

    for i in range(len(data['key'])):
        baris, kolom = data['key'][i]
        correlation = ((baris-rerata_baris)*(kolom-rerata_kolom)
                       * (data['norm'][i])) / (res_baris * res_kolom)
        result += correlation
    return result
