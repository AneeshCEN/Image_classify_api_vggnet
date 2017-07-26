'''
Created on Jul 20, 2017

@author: aneesh.c
'''
import re
import base64

def convert_to_image(img_data):
    imgstr = re.search(r'base64,(.*)',img_data).group(1)
    x = base64.decodestring(imgstr)
    with open('output.png','wb') as output:
        output.write(x)
    return 1