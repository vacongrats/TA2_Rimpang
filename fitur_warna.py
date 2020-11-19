import cv2
import numpy as np
from matplotlib import pyplot as plt

def persentase(histo):
    persen=[]
    for i in range(len(histo)):
        persen.append((histo[i]/sum(histo))*100)
    # print(sum(persen))    
    return persen

def histogram(img):
    color = ['b','g','r']
    # print(data)
    data= []
    for i in range(len(color)):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        persen = persentase(histr)
        data.append(np.average(persen[0:85]))
        data.append(np.average(persen[85:170]))
        data.append(np.average(persen[170 :255]))
    # # print(data)
    return data

# filename = 'D://xampp//htdocs//TA2_Rimpang//L1.png'
# img = cv2.imread(filename)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
# print('gr : ',gray)
# print('hh : ', thresh)

# =====================================================================================================
# filename = 'D://xampp//htdocs//TA2_Rimpang//L1.png'
# img = cv2.imread(filename)

# histo = histogram(img)
# print(histo)

# r = np.array([255,0,0])
# g = np.array([0,255,0])
# b = np.array([0,0,255])
# rgb = cv2.inRange(r,g,b)

# plt.plot(histo)


# img_shape = img.shape
# height = img_shape[0]
# width = img_shape[1]

# persen=None
# color = ['b','g','r']
# for i in range(len(color)):
#     histr = cv2.calcHist([img],[i],None,[256],[0,256])
#     persen = persentase(histr)

#     print(i)
#     print(np.average(persen[0:84]))
#     print(np.average(persen[85:170]))
#     print(np.average(persen[171:255]))

    # print(sum(persen))

    # plt.plot(histr)


# plt.show()