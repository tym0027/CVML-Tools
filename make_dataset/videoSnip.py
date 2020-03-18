import os
import urllib.request
import subprocess
import glob
import cv2
import math
import numpy as np

from config import get_args

def load_txt(file_path, mode='trainval'):
    filename = 'ava_file_names_{}_v2.1.txt'.format(mode)
    filename = os.path.join(file_path, filename)
    with open(filename, 'r') as f:
        video_names = f.readlines()
    return video_names


