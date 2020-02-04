import cv2
import numpy as np

import os
from subprocess import run



SGL_IP = '192.168.0.111'

IMGS = {
        "max": {
            "filename": "maximize_icon",
            "screen_region": "16x16+983+0"
            },
        
        "start": {
            "filename": "start_menu",
            "screen_region": "230x1+0+1267"
        },
        "pcs": {
            "filename": "pcs_list",
            "screen_region": "1x900+17+122"
        }
    }

FOLDERS = ('ref', 'tmp', )

# Guiding for checking which PCs are on and off
PIXELS = {
        "start": 8,
        "step_size": 21
        }

# PC is logged if pixel has this color
LOGGEDPC_PIXEL_COLOR = [44, 199, 90]

def check_img_arg(img_name: str):
    if img_name not in IMGS.keys():
        raise ValueError("Invalid folder name. Valid names are: {}".format(IMGS.keys()))

def get_img_path(folder: str, img_name: str) -> str:
    if folder not in FOLDERS: #or img_name not in IMGS.keys:
        raise ValueError("Invalid folder name. Valid names are: {}".format(FOLDERS))

    check_img_arg(img_name)

    return 'img/{}/{}.jpg'.format(folder, IMGS[img_name]['filename'])


def take_ss(img_name: str):

    def delete_old_ss(img_path):
        if (os.path.exists(img_path)):
            os.remove(img_path)

    check_img_arg(img_name)

    img_path = get_img_path('tmp', img_name)
    delete_old_ss(img_path)

    prcs = run([(
        'bin/vncsnapshot/vncsnapshot' +
        ' -passwd {0}'.format('bin/vncsnapshot/credentials') +
        ' -rect {0}'.format(IMGS[img_name]['screen_region']) +
        ' -nocursor' + 
        ' -ignoreblank' + 
        ' -vncQuality 9' +
        ' -quality 1000' +
        ' ' + SGL_IP + 
        ' ' + img_path
        )], shell=True, check=True)

    return cv2.imread(img_path)


def list_pcs_logged_status():
    # raise NotImplementedError()
    # TODO: it should check if SGL is maximized and only program running b4 taking ss

  
    def get_pixels_indexes(start: int, step_size: int, end: int) -> tuple:
        return tuple( ((i * step_size) + start for i in range(int( (end - start) / step_size)) ) )

    def is_logged(pixel: int):
        for i in range(3):
            if ss[pixel, 0][i] != LOGGEDPC_PIXEL_COLOR[i]:
                return False
        return True
        

    ss = take_ss('pcs')
    indexes = get_pixels_indexes(PIXELS['start'], PIXELS['step_size'], ss.shape[0]) # shape0 = img's height
    return tuple( (is_logged(pixel) for pixel in indexes) ) 

print(list_pcs_logged_status())
