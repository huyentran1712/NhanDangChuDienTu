import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
 
window=tk.Tk()
window.title("Project")
window.resizable(0,0)
 
load1 = Image.open("letters_inverse.png")
photo1 = ImageTk.PhotoImage(load1)
 
header = tk.Button(window, image=photo1)
header.place(x=5,y=0)
 
canvas1  = Canvas(window, width=500, height=250, bg='ivory')
canvas1.place(x=5, y=120)
 
l1=tk.Label(canvas1,text="Digit",font=('Algerian',20))
l1.place(x=5,y=0)
 
t1=tk.Entry(canvas1,width=20, border=5)
t1.place(x=150, y=5)
 
def screen_capture():
   import pyscreenshot as ImageGrab
   import time
   import os
   os.startfile("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Accessories/Paint")
   s1=t1.get()
   os.chdir("D:/TRÍ TUỆ NHÂN TẠO/AppDigitRecog/captured_images")
   os.mkdir(s1)
   os.chdir("D:/TRÍ TUỆ NHÂN TẠO/AppDigitRecog/")
 
   images_folder="captured_images/"+s1+"/"
   time.sleep(15)
   for i in range(0,5):
       time.sleep(8)
       im=ImageGrab.grab(bbox=(60,170,400,550)) #x1,y1,x2,y2
       print("saved......",i)
       im.save(images_folder+str(i)+'.png')
       print("clear screen now and redraw now........")
   messagebox.showinfo("Result","Capturing screen is completed!!")
   
b1=tk.Button(canvas1,text="1. Open paint and capture the screen", font=('Algerian',15),bg="orange",fg="black",command=screen_capture)
b1.place(x=5, y=50)
 
def generate_dataset():
   import cv2
   import csv
   import glob
 
   header  =["label"]
   for i in range(0,784):
       header.append("pixel"+str(i))
   with open('dataset.csv', 'a') as f:
       writer = csv.writer(f)
       writer.writerow(header)
 
   for label in range(10):
       dirList = glob.glob("captured_images/"+str(label)+"/*.png")
 
       for img_path in dirList:
           im= cv2.imread(img_path)
           im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
           im_gray = cv2.GaussianBlur(im_gray,(15,15), 0)
           roi= cv2.resize(im_gray,(28,28), interpolation=cv2.INTER_AREA)
 
           data=[]
           data.append(label)
           rows, cols = roi.shape
 
           ## Add pixel one by one into data array
           for i in range(rows):
               for j in range(cols):
                   k =roi[i,j]
                   if k>100:
                       k=1
                   else:
                       k=0
                   data.append(k)
           with open('dataset.csv', 'a') as f:
               writer = csv.writer(f)
               writer.writerow(data)
   messagebox.showinfo("Result","Generating dataset is completed!!")
   
b2=tk.Button(canvas1,text="2. Generate dataset", font=('Algerian',15),bg="pink",fg="blue",command=generate_dataset)
b2.place(x=5, y=100)
 
def train_save_accuracy():
   import pandas as pd
   from sklearn.utils import shuffle
   data  =pd.read_csv('dataset.csv')
   data=shuffle(data)
   X = data.drop(["label"],axis=1)
   Y= data["label"]
   from sklearn.model_selection import train_test_split
   train_x,test_x,train_y,test_y = train_test_split(X,Y, test_size = 0.2)
   import joblib
   from sklearn.svm import SVC
   classifier=SVC(kernel="linear", random_state=6)
   classifier.fit(train_x,train_y)
   joblib.dump(classifier, "model/digit_recognizer")
   from sklearn import metrics
   prediction=classifier.predict(test_x)
   acc=metrics.accuracy_score(prediction, test_y)
   messagebox.showinfo("Result",f"Your accuracy is {acc}")
   
b3=tk.Button(canvas1,text="3. Train the model and calculate accuracy", font=('Algerian',15),bg="green",fg="white",command=train_save_accuracy)
b3.place(x=5, y=150)
 
def prediction():
   import joblib
   import cv2
   import numpy as np
   import time
   import pyscreenshot as ImageGrab
   
   model=joblib.load("model/digit_recognizer")
   
   img=ImageGrab.grab(bbox=(130,500,500,700))
   img.save("paint.png")
   
   im = cv2.imread("paint.png")
   load = Image.open("paint.png")
   load = load.resize((280,280))
   photo = ImageTk.PhotoImage(load)
   
   #Labels can be text or images
   img = Label(canvas3, image=photo, width=280, height=280)
   img.image=photo
   img.place(x=0,y=0)
   
   im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
   im_gray  =cv2.GaussianBlur(im_gray, (15,15), 0)
 
   #Threshold the image
   ret, im_th = cv2.threshold(im_gray,100, 255, cv2.THRESH_BINARY)
   roi = cv2.resize(im_th, (28,28), interpolation  =cv2.INTER_AREA)
 
   rows,cols=roi.shape
 
   X = []
 
   ## Add pixel one by one into data array
   for i in range(rows):
       for j in range(cols):
           k = roi[i,j]
           if k>100:
               k=1
           else:
               k=0
           X.append(k)
 
   predictions  =model.predict([X])
     
   a1 = tk.Label(canvas3, text="Prediction= ", font=("Algerian",20))
   a1.place(x=5, y=350)
   
   b1 = tk.Label(canvas3, text=predictions[0], font=("Algerian",20))
   b1.place(x=200, y=350)
   
   
       
b4=tk.Button(canvas1,text="4. Live prediction", font=('Algerian',15),bg="white",fg="red",command=prediction)
b4.place(x=5, y=200)
 
 
canvas2 = Canvas(window, width=500, height=270, bg='black')
canvas2.place(x=5, y=380)
 
def activate_paint(e):
   global lastx, lasty
   canvas2.bind('<B1-Motion>', paint)
   lastx, lasty = e.x, e.y
   
def paint(e):
   global lastx, lasty
   x,y = e.x, e.y
   canvas2.create_line((lastx,lasty,x,y), width=40, fill="white")
   lastx, lasty = x,y
 
canvas2.bind('<1>', activate_paint)    
   
def clear():
   canvas2.delete("all")
   
btn = tk.Button(canvas2, text="clear", fg="white", bg="green", command=clear)
btn.place(x=0,y=0)
 
canvas3 = Canvas(window, width=280, height=530, bg="green")
canvas3.place(x=515, y=120)
 
window.geometry("800x680")
window.mainloop()