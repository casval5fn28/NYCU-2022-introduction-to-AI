import os
import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from math import *

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
             First , read the detectData.txt through given datapath in " main.py ". 
        In "detectData.txt" , if a line's length equals to 2 , then collect its line[0] as file name
        of image and line[1] as number of faces , and set these two data in the "data" array. While a 
        line's length equals to 4 , collect line[0]~[3] for locating the rectangles , then get a 19x19 
        grayscale version of original image . After that, use " clf.classify() " to detect faces and 
        get the result of "whether it's a face".
             If the result obtained above equals to 1 , then mark it with green lines , while using 
        red lines for results that equals to 0 . After doing several turns of marking , the images marked 
        with green/red rectangle in desired size will be shown .
    """
    
    data = []
    
    for line in open(dataPath, "r"):
        line = line.split()
        if len(line) == 2 :
            file_path = line[0]
            img = cv2.imread(dataPath[0:12] + file_path)
            pic = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            data.append((img, int(line[1])))

        else :
            for i in range(4) :
                line[i] = int(line[i])
            
            tmp_pic = pic[line[1] : line[1] + line[3], line[0] : line[0] + line[2]]
            tmp_pic = cv2.resize(tmp_pic,(19, 19))
            tmp_res = clf.classify(tmp_pic)
            if tmp_res == 1:
                cv2.rectangle(img, (line[0], line[1]), (line[0] + line[2], line[1] + line[3]), (0, 255, 0), 2)   
            else:
                cv2.rectangle(img, (line[0], line[1]), (line[0] + line[2], line[1] + line[3]), (0, 0, 255), 2)
    
    
    for i in data:
        ims = cv2.resize(i[0], (960, 638))
        cv2.imshow('My Image',ims)
        cv2.waitKey(0)
        
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)
