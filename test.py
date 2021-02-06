#Importing all the libraries
import cv2 
import numpy as np
from statistics import mode,median
import time
import tkinter as tk
import tkinter.font as font
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
a=[1,1,0,0,5]
print(mode(a))