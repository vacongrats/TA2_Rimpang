import numpy as np
yes = np.array([86, 96, 80, 65, 70, 80, 70, 90, 75])
no = np.array([85, 90, 70, 95, 91])
eks = 2.71828183
phi = 3.14159
mean_yes = np.mean(yes)
mean_no = np.mean(no)

std_dev_yes =np.sqrt(sum((yes-mean_yes)**2)/(len(yes)-1))
std_dev_no = np.sqrt(sum((no-mean_no)**2)/(len(no)-1))

eks_yes = -(((74-mean_yes)**2)/(2*(std_dev_yes)**2))
eks_no = -(((74-mean_no)**2)/(2*(std_dev_no)**2))
# print(eks_yes)
# p_yes =  
p_no = (1/np.sqrt(2*phi)*std_dev_no)*eks**eks_no
# print(p_yes,'\n',p_no)

# rumus1 =(1/(np.sqrt((2*phi))*10.2))*eks**(-((74-79.1)**2)/(2*(10.2)**2))
rumus1 =(1/(np.sqrt((2*phi))*std_dev_yes))*eks**(-((74-mean_yes)**2)/(2*(std_dev_yes)**2))
rumus2 =(1/(np.sqrt((2*phi))*std_dev_no))*eks**(-((74-mean_no)**2)/(2*(std_dev_no)**2))
# rumus2 =(1/(np.sqrt((2*phi))*9.7))*eks**(-((74-86.2)**2)/(2*(9.7)**2))
print(rumus1)
print(rumus2)