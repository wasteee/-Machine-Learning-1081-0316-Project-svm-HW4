"""The template of the main script of the machine learning process
"""
import pickle
import numpy as np
from os import listdir
from os.path import isfile, join

dirpath = 'C:\\Users\\fghj8\\MLGame-master\\games\\arkanoid\\log\\svmm2'
BallPosition = []
PlatformPosition = []
LRUP = []
Slope = []
last_ball_x = 0
last_ball_y = 0
files = listdir(dirpath)
log_number = 0
Frame = []
bricks = []
hit = False
hitarray = []

for k in range(0,1):
    for f in files:
      log_number = log_number + 1
      fullpath = join(dirpath, f)
      if isfile(fullpath):
        with open(fullpath , "rb") as f1:
            data_list1 = pickle.load(f1)
        for i in range(0 , len(data_list1)):
            table = np.array(np.zeros((208,408)))
            for k in range(len(bricks)):
                for p in range(0,25):
                    for j in range(0,10):
                        table[bricks[k][0] + p][bricks[k][1] + j ] = 1
            BallPosition.append(data_list1[i].ball)
            PlatformPosition.append(data_list1[i].platform)
            Frame.append(data_list1[i].frame)
            if(last_ball_x - data_list1[i].ball[0] > 0):
                LR = 1
                if(last_ball_y - data_list1[i].ball[1] > 0):
                    #going up
                    UP = 0
                    
                    #U.L
                    j = data_list1[i].ball[0]
                    k = data_list1[i].ball[1] - 3
                    while(j > 0 and k > 0):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j-1
                        k = k-1
                        hit = False
                    if(hit==False):
                        j = data_list1[i].ball[0]+3
                        k = data_list1[i].ball[1]-3
                        while(j > 0 and k > 0):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j-1
                            k = k-1
                            hit = False
                        
                    if(hit):
                        hitarray.append(np.array((j,k)))
                    else:
                        hitarray.append(np.array((-1,-1)))
                else:
                    #going down
                    UP = 1
                    
                    j = data_list1[i].ball[0]
                    k = data_list1[i].ball[1]
                    while(j > 0 and k < 400):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j-1
                        k = k+1
                        hit = False
                    if(hit==False):
                        j = data_list1[i].ball[0]
                        k = data_list1[i].ball[1]+3
                        while(j > 0 and k < 400):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j-1
                            k = k+1
                            hit = False
                    if(hit):
                        hitarray.append(np.array((j,k)))
                    else:
                        hitarray.append(np.array((-1,-1)))
                    
            else:
                LR = 0
                if(last_ball_y - data_list1[i].ball[1] > 0):
                    #going up
                    UP = 0
                    
                    #U.R
                    j = data_list1[i].ball[0]
                    k = data_list1[i].ball[1]
                    while(j < 200 and k > 0):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j+1
                        k = k-1
                        hit = False
                    if(hit==False):
                        j = data_list1[i].ball[0]
                        k = data_list1[i].ball[1]-3
                        while(j < 200 and k > 0):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j+1
                            k = k-1
                            hit = False
                    if(hit):
                        hitarray.append(np.array((j,k)))
                    else:
                        hitarray.append(np.array((-1,-1)))
                else:
                    #going down
                    UP = 1
                    
                    #D.R.
                    j = data_list1[i].ball[0]+3
                    k = data_list1[i].ball[1]
                    while(j < 200 and k < 400):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j+1
                        k = k+1
                        hit = False
                    if(hit==False):
                        j = data_list1[i].ball[0]
                        k = data_list1[i].ball[1]
                        while(j < 200 and k < 400):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j+1
                            k = k+1
                            hit = False
                    if(hit):
                        hitarray.append(np.array((j,k)))
                    else:
                        hitarray.append(np.array((-1,-1)))
            
            LRUP.append(np.array((LR,UP)))
            delta_x = int(data_list1[i].ball[0]) - int(last_ball_x)
            delta_y = int(data_list1[i].ball[1]) - int(last_ball_y)
            #get Slope
            #print(fullpath)
            try:
                m = delta_y/delta_x
            except:
                m = 0.0001
                print(fullpath)
            Slope.append(np.array((m,data_list1[i].platform[0])))
            
            last_ball_x = data_list1[i].ball[0]
            last_ball_y = data_list1[i].ball[1]


PlatX = np.array(PlatformPosition) [:,0][:,np.newaxis]
PlatX_next = PlatX[1:,:]
instrust = (PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5



Ballarray = np.array(BallPosition[:-1])
LRUP = np.array((LRUP[:-1]))
hitarray = np.array((hitarray[:-1]))
S = np.array((Slope[:-1]))
x = np.hstack((Ballarray,LRUP,S,hitarray))


y = instrust 
np.set_printoptions(threshold=np.inf)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.05,random_state = 41)

from sklearn.svm import SVR
#from sklearn.metrics import accuracy_score

svr = SVR(gamma=0.001,C = 1.0,epsilon = 0.1)

svr.fit(x_train,y_train)   
y_predict = svr.predict(x_test)


from sklearn.metrics import r2_score#R square

R2 = r2_score(y_test,y_predict)

#ysvr_bef_scaler = svr.predict(x_test)
#acc_svr_bef_scaler = accuracy_score(ysvr_bef_scaler,y_test)

print(len(Frame))
print('log number : ' + str(log_number))
print('R2 = ',R2)

filename = "C:\\Users\\fghj8\\MLGame-master\\games\\arkanoid\\svr_example_m2.sav"
pickle.dump(svr,open(filename,"wb"))

#from sklearn.preprocessing import StandardScaler
#scaler = StandardScaler()
#scaler.fit(x_train)
#x_train_stdnorm = scaler.transform(x_train)
#svm.fit(x_train_stdnorm,y_train)
#x_test_stdnorm = scaler.transform(x_test)
#ysvm_aft_scaler = svm.predict(x_test_stdnorm)
#acc_svm_aft_scaler = accuracy_score(ysvm_aft_scaler,y_test)
#print(acc_svm_aft_scaler)
#
#filename = "C:\\Users\\fghj8\\MLGame-master\\games\\arkanoid\\svm_scaler_m2.sav"
#pickle.dump(svm,open(filename,"wb"))
    
            

