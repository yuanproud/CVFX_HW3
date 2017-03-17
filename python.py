# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 12:11:25 2017

@author: nvlab
"""

import cv2
import sys
import numpy as np

#Image Loading and initializations
#Target = str(sys.argv[1])
#Texture = str(sys.argv[2])
texture = cv2.imread("texture1.bmp")
target = cv2.imread("target.jpg")
img_height = target.shape[0]
img_width  = target.shape[1]
texture_width = texture.shape[1]
texture_height = texture.shape[0]
#img = np.zeros((img_height,img_width,3), np.uint8)
PatchSize = int(sys.argv[1])
OverlapWidth = int(sys.argv[2])
InitialThresConstant = float(sys.argv[3])

#target = np.zeros((img_height,img_width),int)
#texture = np.zeros((texture_height,texture_width),int)


def find_mindelta(texture, target, targeth,targetw, PatchSize, InitialThresConstant):
        
    ssdarr = np.zeros((texture_height-PatchSize+1,texture_width-PatchSize+1),int)        
    for i in range(texture_height-PatchSize):
        for j in range(texture_width-PatchSize):
            textureh = i
            texturew = j
            temp = get_ssd(texture, textureh, texturew, target, targeth,targetw, PatchSize)
            if temp == 0:
                ssdarr[i][j] = 10000000000000
            else:
                ssdarr[i][j] = temp
                
    min_index = np.argmin(ssdarr)
    posh = min_index/texture_width
    posw = min_index%texture_width - 1
    
    return posh,posw
        
def get_ssd(texture, textureh, texturew, target, targeth,targetw, PatchSize):
    
    temparr = np.zeros((PatchSize,PatchSize,3),int)
    for i in range(PatchSize-1):
        for j in range(PatchSize-1):
            temparr[i][j][0] = target[targeth*PatchSize+i][targetw*PatchSize+j][0] - texture[targeth+i][targetw+j][0]
            temparr[i][j][1] = target[targeth*PatchSize+i][targetw*PatchSize+j][1] - texture[targeth+i][targetw+j][1]
            temparr[i][j][2] = target[targeth*PatchSize+i][targetw*PatchSize+j][2] - texture[targeth+i][targetw+j][2]

    temparr =np.multiply(temparr,temparr)
    tempar = np.sum(temparr)

    return tempar        
    
result = np.zeros((img_height,img_width,3),int)
for i in range(img_height/PatchSize-1):
    for j in range(img_width/PatchSize-1):
        posh,posw = find_mindelta(texture,target,i,j,PatchSize,InitialThresConstant)
                
        for k in range(PatchSize-1):
            for g in range(PatchSize-1):        
                result[i*PatchSize+k][j*PatchSize+g][0] = texture[posh+k][posw+g][0]
                result[i*PatchSize+k][j*PatchSize+g][1] = texture[posh+k][posw+g][1]
                result[i*PatchSize+k][j*PatchSize+g][2] = texture[posh+k][posw+g][2]

cv2.imshow("img_result",result)
