# -*- coding: utf-8 -*-

import os
from tqdm import tqdm_notebook
from random import shuffle
import shutil
import random

def organize_datasets(path_to_data, samplesize=3311,val_ratio=0.1,test_ratio=0.2):

    # 寻找当前images的路径
    files = os.listdir(path_to_data)
    files = [os.path.join(path_to_data, f) for f in files]
    
    # 打乱顺序 （防止前一半都是虫草，后一半都是人参这种情况）
    shuffle(files)
    
    # 计算test, training, validation的数据量，2:1:7 as prefered, 不过这个没有任何规定，只要train够大就行
    testsize = int(samplesize*test_ratio)
    valsize = int(samplesize*val_ratio)
    trainsize = samplesize - testsize - valsize
    
    # 将所有data按照上一步决定的数据量，分成三份，WITH NO OVERLAP!!!这几行代码里只分了index
    sample_index = list(range(0,samplesize))
    test_index = random.sample(sample_index,testsize)
    val_index = random.sample(list(set(sample_index).difference(set(test_index))),valsize)
    train_index = random.sample(list(set(list(set(sample_index).difference(set(test_index)))).difference(set(val_index))),trainsize)

    # 通过上一步分好的index，把图片的路径也分成三份
    train, test, val = [files[i] for i in train_index], [files[j] for j in test_index], [files[k] for k in val_index]
    
    # 删掉已存在的“data”文件夹，为了接下来把我们分好的数据放到data文件夹里
    #deleted already existed file folder, inorder to allow us put our files into the folder
    shutil.rmtree('./data/')
    print('/data/ removed')
    
    # 建立六个文件夹，路径分别是
    # data/train/chongcao
    # data/train/renshen
    # data/val/chongcao
    # data/val/renshen
    # data/test/chongcao
    # data/test/renshen
    for c in ['chongcao', 'renshen']:
        os.makedirs('./data/train/{0}/'.format(c))
        os.makedirs('./data/val/{0}/'.format(c))
        os.makedirs('./data/test/{0}/'.format(c))
    print('folders created !')
    
    # 将原始数据按照上述分配方式，分配到六个文件夹中， tqdm_notebook(train)其实就是个list，每个元素是一个image的路径
    for t in tqdm_notebook(train):
        if 'chongcao' in t:
            shutil.copy2(t, os.path.join('.', 'data', 'train', 'chongcao'))
            
        else:
            shutil.copy2(t, os.path.join('.', 'data', 'train', 'renshen'))
            
    for s in tqdm_notebook(test):
        if 'chongcao' in s:
            shutil.copy2(s, os.path.join('.', 'data', 'test', 'chongcao'))
            
        else:
            shutil.copy2(s, os.path.join('.', 'data', 'test', 'renshen'))
            
    for v in tqdm_notebook(val):
        if 'chongcao' in v:
            shutil.copy2(v, os.path.join('.', 'data', 'val', 'chongcao'))
            
        else:
            shutil.copy2(v, os.path.join('.', 'data', 'val', 'renshen'))
            
    print('Data copied!')
    
    



if __name__== "__main__":
    organize_datasets(path_to_data='./train/', samplesize=3311,val_ratio=0.1,test_ratio=0.2)

