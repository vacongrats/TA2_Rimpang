import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
# a= math.log(2)
# print(a)
def persentase(histo):
    persen=[]
    for i in range(len(histo)):
        persen.append((histo[i]/sum(histo))*100)
    # print(sum(persen))    
    return persen

img=cv2.imread('KE1.png',0)
# thresh = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
print(img)
# cv2.imshow('Threshold', img)
# print(img)
histr=cv2.calcHist([img],[0],None,[256],[0,256])
persen = persentase(histr)
cv2.imshow('citra',img)
# print(histr)
print(persen)
plt.plot(histr)
# plt.plot(persen)
plt.show()

cv2.waitKey(0)