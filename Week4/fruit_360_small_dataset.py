import torch
from torch.utils.data import Dataset
import os
from torchvision.io import read_image
import matplotlib.pyplot as plt
import numpy as np 

#-------------------------------------------------------------------------------------------------------------------------------------------------------
## Update the following information####
'''
Config Variables
'''
path = "/home/mehul/code/Kratos/QSTP-2021/Assignment 4/fruit_new"      #Enter the path of the folder that contains the Dataset

classes = [                                                 #Enter all the classes you wish to train your model on in the list
    'Papaya',
    'Orange',
    'Salak',
    'Peach'
]

#-------------------------------------------------------------------------------------------------------------------------------------------------------

class fruit_360_small(Dataset):
    def __init__(self, root_dir, train=True , transform=None, target_transform=None):
        '''
        Arguments: root_dir: path of the dataset folder
                   train: returns train dataset if True, else returns test dataset
                   transform: transforms to be made on the input data
                   target_transorm: transforms on the target data
        '''
        self.root_dir = root_dir
        self.train = train
        self.transform = transform
        self.target_transform = target_transform
        self.length = 0
        self.class_items =[]
        self.num_of_class = len(classes)
        self.class_labels = classes

        if (self.train):
            self.root_dir = os.path.join(self.root_dir,'train')
        else:
            self.root_dir = os.path.join(self.root_dir,'test')
        
        path = self.root_dir
        for c in classes:
            self.class_items.append(self.length)
            self.length+= len(os.listdir(os.path.join(self.root_dir,str(c)))) 
            
    def __len__(self):
        return self.length
    
    def __getitem__(self,idx):
        class_id = 0
        while (class_id < self.num_of_class) and (idx >= self.class_items[class_id]):
            class_id+=1
        class_id-=1
        label = classes[class_id]
        idx = idx - self.class_items[class_id]

        path = self.root_dir
        for p in os.listdir(path):
            if p==label:
                path = os.path.join(path,p)
                path = os.path.join(path, str(idx)+".jpg")
                img = read_image(path)
                img = img.type(torch.float)
                break
        
        label = class_id
        if (self.transform):
            img = self.transform(img)
        if self.target_transform:
            label = self.target_transform(class_id)
        return img,label

if __name__=='__main__':
    dat = fruit_360_small(path,train = True)
    img,label = dat[np.random.randint(len(dat))]
    print(f"Size of Dataset is {len(dat)}")
    img = img.permute(1,2,0)
    plt.imshow(img/255.0)
    plt.title(dat.class_labels[label])
    plt.show()
