#!/usr/bin/env python
#-*- coding: utf-8 -*-
from Tkinter import *
from PIL import ImageTk
from math import *
from tkFileDialog import *
from Tkinter import *
import os
import PIL.Image

#Class principale
class App:
    #constructeur 
    def __init__(self, master):

        frame = Frame(master)
        frame.pack()
        #le panel pour l'affichage de l'image 
        self.panel = Label(root)
        #%de pixelisation
        self.type = "Fuzzy"
        self.level = 1
        self.file = None
        self.image = None
        #les boutons 
        self.select = Button(frame, text="Select File", command=self.pathSelector)
        self.select.pack(side=RIGHT)
        self.go = Button(frame, text="Go", command=self.fuzzy)
        self.go.pack(side=LEFT)
        self.red = Button(frame, text="Red", command=lambda: self.setType("red"))
        self.red.pack(side=LEFT)
        self.blue = Button(frame, text="Blue", command=lambda: self.setType("blue"))
        self.blue.pack(side=LEFT)
        self.green = Button(frame, text="Green", command=lambda: self.setType("green"))
        self.green.pack(side=LEFT)
        self.fuzzy = Button(frame, text="Fuzzy", command=lambda: self.setType("white"))
        self.fuzzy.pack(side=LEFT)
        self.scale = Scale(orient='horizontal', from_=1, to=10, command=self.changeFuzzyPurcent)
        self.scale.pack()
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    #methode pour changer le pourcentage de floutage (int valeur)
    def changeFuzzyPurcent(self, val):
        self.level = val
        
    #methode pour selectionner une image qui est affichee dans le panel    
    def pathSelector(self):
        self.file = askopenfilename(title='Selectionner un fichier ')
        self.displayImage(self.file)
    
    #methode pour "actualiser" l'image du panel  
    def displayImage(self, path):
        self.image = ImageTk.PhotoImage(PIL.Image.open(path))
        self.panel.configure(image = self.image)
        self.panel.image = self.image
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    #methode pour changer le type de floutage rouge, bleu, vert, normal
    def setType(self,newType):
        self.type = newType
    
    #methode pour le floutage 
    def fuzzy(self):
        #ouverture de l'image
        type = self.type
        img = PIL.Image.open(self.file)
        #niveau de pixelisation
        level = int(self.level)
        #nouvelle image avec une taille specifique ( éviter les bords noirs )
        img2 = PIL.Image.new("RGB",(int((floor(img.size[0]/level))*level),int((floor(img.size[1]/level))*level)),type)
        imgWidth = img.size[0]
        imgHeigth = img.size[1]
        i = 0
        x = 0
        y = 0
        #boucle pour parcourir les pixels de l'image 
        #les lignes 
        while i < imgWidth-level:
            j = 0
            #les colones
            while j < imgHeigth-level:
                moy = [0,0,0]
                #parcourir les sous tableaux (level*level) level pixels de l'image 
                for u in range(level):
                    x +=1
                    for v in range(level):
                        y +=1
                        #la moyenne de la composants RGB de chaque pixel 
                        pixelColor = img.getpixel((i+u,j+v))
                        if(type=="white"): 
                            moy[0] = moy[0]+pixelColor[0]
                            moy[1] = moy[1]+pixelColor[1]
                            moy[2] = moy[2]+pixelColor[2]
                        elif(type=="green"):
                            moy[0] = moy[0]+pixelColor[0]
                            moy[1] = moy[1]+pixelColor[1]+255-pixelColor[0]
                            moy[2] = moy[2]+pixelColor[2]
                        elif(type=="blue"):
                            moy[0] = moy[0]+pixelColor[0]
                            moy[1] = moy[1]+pixelColor[1]
                            moy[2] = moy[2]+pixelColor[2]+255-pixelColor[0]
                        elif(type=="red"):
                            moy[0] = moy[0]+pixelColor[0]+255-pixelColor[0]
                            moy[1] = moy[1]+pixelColor[1]
                            moy[2] = moy[2]+pixelColor[2]
                        
                moy[0] = moy[0]/(level*level)
                moy[1] = moy[1]/(level*level)
                moy[2] = moy[2]/(level*level)
                #remplacement de chaque composantes RGB du pixel par la moyenne des pixels du mini tableau  
                for u in range(level):
                    for y in range(level):
                        img2.putpixel((i+u,j+y),(int(moy[0]),int(moy[1]),int(moy[2])))
                j += level;
            i += level;
        #sauvegarde de l'image 
        img2.save("temp/temp.png")
        self.displayImage("temp/temp.png")      
  
    

root = Tk()
app = App(root)
root.mainloop()
root.destroy()