import cv2
import numpy as np

import os
from subprocess import run



SGL_IP = '192.168.0.111'

# Images that will be compared with a reference
# to check is SGL in the only program open and maixmized
# in the server
IMGS_TO_COMPARE = {
        "max": {
            "filename": "maximize_icon",
            "screen_region": "16x16+983+0"
            },
        
        "start": {
            "filename": "start_menu",
            "screen_region": "230x1+0+1267"
        },        

        "pcs-ml": {
            "filename": "logged_pcs_margin_left",
            "screen_region": "3x1022+0+0"
        },

        "pcs-mr": {
            "filename": "logged_pcs_margin_right",
            "screen_region": "1x1022+22+0"
        },

        "pcs-mt": {
            "filename": "logged_pcs_margin_top",
            "screen_region": "50x1+0+110"
        },

        "pcs-mb": {
            "filename": "logged_pcs_margin_bottom",
            "screen_region": "370x1+0+1023"
        },


}

# Screenshot with the list of PCs, and their logged status
# it will be analized, but not compared with a reference img
IMGS_TO_ANALIZE= {
        "pcs": {
            "filename": "pcs_list",
            "screen_region": "1x900+17+122"
        }           
}


# All Imgs
IMGS = dict()
IMGS.update(IMGS_TO_COMPARE)
IMGS.update(IMGS_TO_ANALIZE)

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


def is_imgs_equal(img1, img2):
    # got from: https://pysource.com/2018/07/19/check-if-two-images-are-equal-with-opencv-and-python/
    original = img1 if not isinstance(img1, str) else cv2.imread(img1)
    duplicate = img2 if not isinstance(img2, str) else cv2.imread(img2)

    if original.shape == duplicate.shape:
    #    print("The images have same size and channels")
        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
    #        print("The images are completely Equal")
            return True
    return False

def is_sgl_ready():
    # the server is ready to take more screenshots
    # of SGL if:
    # + SGL is Maximized
    # + SGL is the only program open (in the start menu)
    # + Start Menu is closed
    #
    # TODO: "returns falses" should send error msgs back to loginsv
    

    for img in IMGS_TO_COMPARE.keys():
        try:
            tmp = take_ss(img)
            ref = get_img_path('ref', img)
            if not is_imgs_equal(tmp, ref):
                return False
        except Exception as e:
            print(e)
            return False

    return True

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
        
    if not is_sgl_ready():
        return False # TODO: replace with error msg

    ss = take_ss('pcs')
    indexes = get_pixels_indexes(PIXELS['start'], PIXELS['step_size'], ss.shape[0]) # shape0 = img's height
    return tuple( (is_logged(pixel) for pixel in indexes) ) 

print(list_pcs_logged_status())
