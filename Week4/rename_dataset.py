import os
import sys
from shutil import copy2

def rename_files(path, new_path):
    file_list =  os.listdir(path).copy()
    idx = 0

    if not(os.path.isdir(new_path)):
        os.mkdir(new_path)

    for filename in file_list:
        f = os.path.join(path,filename)
        if os.path.isdir(f):
            f_n = os.path.basename(f)
            f_n = os.path.join(new_path,f_n)
            rename_files(f,f_n)
            continue
        if os.path.isfile(f):
            try:
                f_n = os.path.join(new_path,str(idx)+".jpg")
                copy2(f, f_n)
                idx+=1
            except:
                print(f"Failed to convert {f}")
    

if __name__=='__main__':
    '''
        Renames All the files in the Dataset folder of first argument and copies it to second folder
    '''
    path = sys.argv[1] 
    new_path = sys.argv[2]
    rename_files(path, new_path)