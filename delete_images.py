import os

img_dir = "C:\\Users\\kb48\\Downloads\\LymphNodeProject\\Segmentations\\"
for file in os.listdir(img_dir): 
   
    if 'rotate' in file:
        print(file)
        os.remove(img_dir + file) 