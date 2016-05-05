#!/usr/bin/env python
#-*- coding: utf-8 -*-
from Tkinter import *
import threading
from tkFileDialog import *
import sfml as sf
from PIL import Image
from math import *
import os
import time

#%de pixelisation
level = 8

#fonction de floutage
def fuzzy(path, fuzzyPurcent):
    #ouverture de l'image
    img = Image.open(path)
    #niveau de pixelisation
    level = fuzzyPurcent
    #nouvelle image avec une taille specifique ( éviter les bords noirs )
    img2 = Image.new("RGB",(int((floor(img.size[0]/level))*level),int((floor(img.size[1]/level))*level)),"black")
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
                    moy[0] = moy[0]+pixelColor[0]
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
    img2.save("temp.png")

#class de la fenetre pysfml 
def sfmlWindow():
    """Code à exécuter pendant l'exécution du thread."""
    #la couleur du fond
    backgroundColor = sf.Color(255, 255, 255)
    #fenetre pour le choix du fichier
    root = Tk()
    root.withdraw()
    # selection du fichier
    file = askopenfilename(title='Selectionner un fichier ')
    try:
        imagePath = sf.Texture.from_file(file)
    except IOError, e:
        im = Image.open(file)
        im.save('temp.png')
        imagePath = sf.Texture.from_file("temp.png")
        
    #taille de la fenetre
    width = imagePath.size.x
    height = imagePath.size.y
    # create the main window
    window = sf.RenderWindow(sf.VideoMode(width, height), "pySFML Window")
    #rectangle de l'image ( position, taille )
    imgRect = sf.Sprite(imagePath)
    imgRect.texture_rectangle = sf.Rectangle(sf.Vector2(0, 0), sf.Vector2(width, height))
    #loop
    while window.is_open:
        #boucle evenementiels
        for event in window.events:
        #si on quitte
            if type(event) is sf.CloseEvent:
                window.close()
        if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
            # left click...
            fuzzy(file,level)
            try:
                imagePath = sf.Texture.from_file('temp.png')
            except Exception as e:
                raise
            #taille de la fenetre
            width = imagePath.size.x
            height = imagePath.size.y
            # create the main window
            window = sf.RenderWindow(sf.VideoMode(width, height), "pySFML Window")
            #rectangle de l'image ( position, taille )
            imgRect = sf.Sprite(imagePath)
            imgRect.texture_rectangle = sf.Rectangle(sf.Vector2(0, 0), sf.Vector2(width, height))
            #on incremente le level
            #level += 2

        # clear screen
        window.clear(backgroundColor)
        #on dessine l'image
        window.draw(imgRect)
        #update the window
        window.display()
            

#class de la fenetre pysfml 
def tkinterWindow():
    """Code à exécuter pendant l'exécution du thread."""
    fenetre = Tk()
    label = Label(fenetre, text="Hello World")
    label.pack()
    fenetre.mainloop()
    time.sleep(0.2)
       

#les threads des deux fenetre


if __name__ == '__main__':
    try:
        th1=threading.Thread(None,target=tkinterWindow)
        th2=threading.Thread(None,target=sfmlWindow)
        th1.start()
        th2.start()
        th1.join()
        th2.join()
    except Exception, errtxt:
        print errtxt
    time.sleep(5)