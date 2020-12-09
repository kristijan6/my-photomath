import cv2
from imutils import contours
from matplotlib import pyplot as plt
import numpy as np
import os
import glob

class DataLoader():
    def __init__(self):
        pass
    
    def sort_and_get_boxes(self, contours, hierarchy):
        # x,y,w,h
        data = []

        for index, cnt in enumerate(contours):
            # If contour has parent other than main frame, skip it
            parent = hierarchy[0][index][3]
            if parent != 0:
                continue

            x,y,w,h = cv2.boundingRect(cnt)

            if w < 500 and w > 10:
                data.append((x,y,w,h))

        data = sorted(data, key=lambda x: x)

        return data
    
    def delete_existing_files(self):
        files = glob.glob("recognized_data/*")
        for f in files:
            os.remove(f)
            
    def prepare_input(self, image_path):
        img = cv2.imread(image_path, 0)
        dim = (1000, 200) 
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

        ret,thresh = cv2.threshold(img,130,255,cv2.THRESH_BINARY)
        plt.imshow(thresh,'gray')
        plt.show()

        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        data = self.sort_and_get_boxes(contours, hierarchy)

        self.delete_existing_files()
        i = 0
        for x,y,w,h in data:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

            #save individual images
            cv2.imwrite("recognized_data/" + str(i)+".jpg",thresh[y:y+h,x:x+w])
            i=i+1
        plt.imshow(img,'gray')
        plt.show()
        
    def preprocess(self, img, dim = (32,32)):
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        return img
    
    def get_input(self):
        files = sorted(glob.glob("recognized_data/*"))
        input_data = []
        for f in files:
            input_data.append(self.preprocess(cv2.imread(f, 0)))

        return np.array(input_data)
    
    def load_data(self, data_folder):
        images = []
        labels = []

        files = glob.glob(data_folder + "*")
        for file in files:
            filename = int(file.split("/")[1].split(".")[0].split("_")[0])

            img = cv2.imread(file, 0)
            img = self.preprocess(img)

            images.append(img)
            labels.append(filename)

        images = np.array(images)
        labels = np.array(labels)
        return images, labels