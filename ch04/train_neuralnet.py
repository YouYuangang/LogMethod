# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 为了导入父目录的文件而进行的设定
import numpy as np
import matplotlib.pyplot as plt
#from dataset.mnist import load_mnist
from two_layer_net import TwoLayerNet
import pickle
# 读入数据
#(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

def save_params(file_name="params.pkl"):
    params = {}
    for key in ('W1', 'b1', 'W2', 'b2', 'W3','b3'):
        params[key] = network.params[key]
    with open(file_name, 'wb') as f:
        pickle.dump(params, f)

def load_params(file_name="params.pkl"):
    with open(file_name, 'rb') as f:
        params = pickle.load(f)
    for key in ('W1', 'b1', 'W2', 'b2', 'W3','b3'):
        network.params[key] = params[key]


file_path = open('data.pkl','rb')
data = pickle.load(file_path)
x_train_tmp,t_train_tmp,x_test_tmp,t_test_tmp = data["data_set"],data['re_set'],data['test_set'],data['re_test_set']

x_train,t_train,x_test,t_test = np.zeros((10000,1000)), np.zeros((10000,10)),np.zeros((2000,1000)), np.zeros((2000,10))
for i in range(10000):
    tmp = t_train_tmp[i]
    t_train[i][int(tmp)] = 1
    for j in range(1000):
        x_train[i][j] = x_train_tmp[i][j]

for i in range(2000):
    tmp = t_test_tmp[i]
    t_test[i][int(tmp)] = 1
    for j in range(60):
        x_test[i][j] = x_test_tmp[i][j]

print(x_train.shape)
print(t_train.shape)
print(x_test.shape)

#network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)
network = TwoLayerNet(input_size=1000, hidden_size=100, output_size=10,weight_init_std=2)

iters_num = 10000  # 适当设定循环的次数
train_size = x_train.shape[0]
batch_size = 100
learning_rate = 0.1#0.1

train_loss_list = []
train_acc_list = []
test_acc_list = []

iter_per_epoch = max(train_size / batch_size, 1)

for i in range(iters_num):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]
    
    # 计算梯度
    #grad = network.numerical_gradient(x_batch, t_batch)
    grad = network.gradient(x_batch, t_batch)
    
    # 更新参数
    for key in ('W1', 'b1', 'W2', 'b2', 'W3','b3'):
        network.params[key] -= learning_rate * grad[key]
    
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)
    
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

# 绘制图形
save_params()
markers = {'train': 'o', 'test': 's'}
x = np.arange(len(train_acc_list))
plt.plot(x, train_acc_list, label='train acc')
plt.plot(x, test_acc_list, label='test acc', linestyle='--')
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.ylim(0, 1.0)
plt.legend(loc='lower right')
plt.show()
