#!/usr/bin/env python
#-*- coding: utf-8 -*-
from Tkinter import *
from tkFileDialog import *
import sfml as sf
from PIL import Image
from math import *
import os



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

    while i < imgWidth-level:
        j = 0
        while j < imgHeigth-level:
            moy = [0,0,0]
            for u in range(level):
                x +=1
                for v in range(level):
                    y +=1
                    pixelColor = img.getpixel((i+u,j+v))
                    moy[0] = moy[0]+pixelColor[0]
                    moy[1] = moy[1]+pixelColor[1]
                    moy[2] = moy[2]+pixelColor[2]
            moy[0] = moy[0]/(level*level)
            moy[1] = moy[1]/(level*level)
            moy[2] = moy[2]/(level*level)
            for u in range(level):
                for y in range(level):
                    #print(i+u,j+y)
                    img2.putpixel((i+u,j+y),(int(moy[0]),int(moy[1]),int(moy[2])))
            j += level;
        i += level;
    img2.save("temp.jpg")








#%de pixelisation
level = 8

#la couleur du fond
backgroundColor = sf.Color(255, 255, 255)
#fenetre pour le choix du fichier
root = Tk()
root.withdraw()
# selection du fichier
file = askopenfilename(title='Selectionner un fichier ')
try:
    imagePath = sf.Texture.from_file(file)
except Exception as e:
    raise


#taille de la fenetre
WIDTH = imagePath.size.x
HEIGTH = imagePath.size.y
# create the main window
window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGTH), "pySFML Window")
#rectangle de l'image ( position, taille )
imgRect = sf.Sprite(imagePath)
imgRect.texture_rectangle = sf.Rectangle(sf.Vector2(0, 0), sf.Vector2(WIDTH, HEIGTH))
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
            imagePath = sf.Texture.from_file('temp.jpg')
        except Exception as e:
            raise
        #taille de la fenetre
        WIDTH = imagePath.size.x
        HEIGTH = imagePath.size.y
        # create the main window
        window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGTH), "pySFML Window")
        #rectangle de l'image ( position, taille )
        imgRect = sf.Sprite(imagePath)
        imgRect.texture_rectangle = sf.Rectangle(sf.Vector2(0, 0), sf.Vector2(WIDTH, HEIGTH))

        #on incremente le level
        level += 2

    # clear screen
    window.clear(backgroundColor)
    #on dessine l'image
    window.draw(imgRect)
    # update the window
    window.display()
