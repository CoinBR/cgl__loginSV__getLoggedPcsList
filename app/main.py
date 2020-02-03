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


    # raise NotImplementedError()
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


def list_pcs_n_loggedstatus():
    
    # raise NotImplementedError()
    return tuple(False for i in range(50))



######################################



# imgs are stored in two folders
# "ref" represents the way the screenshot should Look if SGL is open
# "tmp" is where the current screenshot will be saved
#    it will then be compared with the one in "ref" folder
##IMGS_DIR = ["ref", "tmp"]


# "is_sgl_open" lists the screenshots (subsections of the screen)
#     that are checked to see if SGL is open
# "loggedin_list" is the image that will be analized to determine
#     the PCs that currently have customers logged in
##IMGS_NAMES = {
#        "is_sgl_open": ['start_menu', 'maximize_icon'],
#        "loggedin_list": "loggedin_list"
#        }
#
#def get_image_path(folder, img_name):
#
#    def check_params():
#        if folder == 0 or folder == 1:
#            return get_image_path(IMGS_DIR[folder])
#
#        if folder not in IMGS_DIR:
#            raise Exception("Invalid image folder name: <{}>".format(folder))
#        
#        if img_name not in IMGS_NAMES.keys and img_name not in IMGS.values:
#            raise Exception("Invalid image name: <{}>".format(img_name))
#
#    if img_name 
#    
#
#original = cv2.imread("imaoriginal_golden_bridge.jpg")
#duplicate = cv2.imread("images/duplicate.jpg")
