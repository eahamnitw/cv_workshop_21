import argparse
import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path

import itertools as it
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image!')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))


def upload():
    ImagePath=easygui.fileopenbox()
    cartoon1 = cartoonify(ImagePath)


def cartoonify(ImagePath):
    # read the image
    originalmage = cv2.imread(ImagePath)
    (width, height, channels) = originalmage.shape
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (height, width))
    #plt.imshow(ReSized1, cmap='gray')


    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (height, width))
    #plt.imshow(ReSized2, cmap='gray')


    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (height, width))
    #plt.imshow(ReSized3, cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 15, 10)

    ReSized4 = cv2.resize(getEdge, (height, width))
    #plt.imshow(ReSized4, cmap='gray')

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (height, width))
    #plt.imshow(ReSized5, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (height, width))
    #plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    # print (axes)
    # print (fig)
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    path1 = os.path.dirname(ImagePath)
    length = len(path1)+1
    extName = (ImagePath)[length:]
    save1 = Button(top,text="Save cartoon image of "+extName,command=lambda: save(ReSized6, ImagePath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
alpha_slider_max = 100
title_window = 'Watch your picture get Cartoonified!'

def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image_"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    length = len(path1)+1
    extName = (ImagePath)[length:]
    path = os.path.join(path1, newName+extName)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
    # print(ImagePath)
    # print(path)
    
    def on_trackbar(val):
        alpha = val / alpha_slider_max
        beta = ( 1.0 - alpha )
        dst = cv2.addWeighted(src1, alpha, src2, beta, 0.0)
        cv2.imshow(title_window, dst)
    
    parser = argparse.ArgumentParser(description='Code for Adding a Trackbar to our applications tutorial.')
    parser.add_argument('--input1', help='Path to the first input image.', default=path)
    parser.add_argument('--input2', help='Path to the second input image.', default=ImagePath)
    args = parser.parse_args()
    src1 = cv2.imread(cv2.samples.findFile(args.input1))
    src2 = cv2.imread(cv2.samples.findFile(args.input2))
    if src1 is None:
        print('Could not open or find the image: ', args.input1)
        exit(0)
    if src2 is None:
        print('Could not open or find the image: ', args.input2)
        exit(0)
    cv2.namedWindow(title_window)
    trackbar_name = 'Alpha x %d' % alpha_slider_max
    cv2.createTrackbar(trackbar_name, title_window , 0, alpha_slider_max, on_trackbar)
    # Show some stuff
    on_trackbar(0)
    # Wait until user press some key
    cv2.waitKey()
    

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

top.mainloop()