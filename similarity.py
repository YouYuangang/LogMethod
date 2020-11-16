import numpy as np
import pickle
import random
'''
A_init = np.random.rand(10,10)

file_path = open("tmp.pkl",'wb')
data = {'A_init':A_init}
pickle.dump(data,file_path)
'''
#读取数据
'''
file_path = open("tmp.pkl", "rb")
data = pickle.load(file_path)
A_init = data['A_init']

A = A_init.copy()
re_set = []
X = np.zeros(A.shape)
'''
def get_similarityMatrx(A):
    for i in range(A.shape[0]):
        for j in range(A.shape[0]):
            if(A[i][j] < 0.45):
                A[i][j] -= 1
def init_re(X):
    X = ((-1) * np.ones((A.shape[0],A.shape[0]),dtype="int"))
    for i in range(A.shape[0]):
        X[i][i] = 1
        
    
def judge(i,j,X):
    tmp_X = X.copy()
    '''
    for k in range(X.shape[0]):
        if(k == i or k==j):
            continue
        if((X[i][k] + X[k][j] - X[i][j] -1)*(X[i][k] + X[k][j] + 2) != 0):
            return False
        for m in 
    '''
    for m in i:
        for n in j:
            tmp_X[m][n] = tmp_X[n][m] = 1
    if(sum(sum(tmp_X*A))<=max):
        return False
    return True

def getModify(i,j):
    global X
    global max
    global re_set
    '''
    X[i][j] = (-1)*X[i][j]
    X[j][i] = X[i][j]
    tmp = sum(sum(A*X))
        
    if(judge(i,j,X) and tmp >= max):
        max = tmp
        return True
    else:
        X[i][j] = (-1)*X[i][j]
        X[j][i] = X[i][j]
        return False
    '''
    if(judge(i,j,X)):
        for m in i:
            for n in j:
                X[m][n] = X[n][m] = 1
        i += j
        re_set.remove(j)
        max = sum(sum(X*A))

def join_set_test(point,new_set,old_set,re_set,X,A):
    X_test = X.copy()
    for other_point in re_set[old_set]:
        if(other_point != point):
            X_test[other_point][point] = X_test[point][other_point] = -1
    for other_point in re_set[new_set]:
        X_test[other_point][point] = X_test[point][other_point] = 1
    return sum(sum(X_test * A))

def K_means(K,A,X):
    max = sum(sum(A*X))
    print(max)
    #点所在集合位置
    point_pos = [-1]*A.shape[0]
    #不同集合所包含的点
    re_set = []
    init_set = random.sample(range(0,A.shape[0]),K)
    #初始化K个集合
    for pos,sample in enumerate(init_set):
        re_set.append([sample])
        point_pos[sample] = pos
    #寻找最优集合划分方案
    while(True):
        for num in range(A.shape[0]):
            best_pos = -1
            #测试是否有更好的集合
            for test_new in range(K):
                if( test_new != point_pos[num] and join_set_test(num,test_new,point_pos[num],re_set,X,A) > max):
                    best_pos = test_new
            #如果存在更好的集合，则加入新集合
            if(best_pos != -1):
                #从当前集合中移除
                if(point_pos[num] != -1):
                    re_set[point_pos[num]].remove(num)
                    for other_point in re_set[point_pos[num]]:
                        X[other_point][num] = X[num][other_point] = -1
                #加入新集合
                point_pos[num] = best_pos
                for other_point in re_set[best_pos]:
                    X[other_point][num] = X[num][other_point] = 1
                re_set[best_pos].append(num)
                
        #结束循环条件
        if max >= sum(sum(A*X)):
            break
        else:
            max = sum(sum(A*X))
        print("max = {}".format(max))
        
    return [i for i in re_set if i!=[]]
'''
get_similarityMatrx(A)
re_set = K_means(A.shape[0],A,X)
print(max)
print(re_set)
print(X)
'''