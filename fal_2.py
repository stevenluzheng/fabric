#coding:utf-8
import numpy as np
import falconn
import time

all_data = np.load("train.npy")
all_label=[]
all_feature=[]

for data in all_data:
    all_feature.append(data[0])
    all_label.append(data[1])
n = len(all_feature)
d = len(all_feature[0])
p = falconn.get_default_parameters(n, d)
t = falconn.LSHIndex(p)
dataset = np.array(all_feature)
t.setup(dataset)

all_data_test=np.load("test.npy")
all_label_test=[]
all_feature_test=[]

for data in all_data_test:
    all_feature_test.append(data[0])
    all_label_test.append(data[1])


K=1 #the target
average_ratio=0.0
t1=time.time()
#test_num=len(all_feature_test)
test_num=200000
for i in range(0,test_num):
    u =np.array(all_feature_test[i])
    res = t.find_k_nearest_neighbors(u, K)
    true_num = 0
    for temp in res:
        if(all_label[temp]==all_label_test[i]):
            true_num+=1
    print "Item_"+str(i)
    print float(true_num)/(K)
    average_ratio+=float(true_num)/(K)
print "Average Correct Ratio:"+str(average_ratio/float(test_num))
print "Time:"+str(time.time() - t1)
