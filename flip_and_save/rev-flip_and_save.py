import os
import sys
import glob
import torch
import cv2
from PIL import Image
import numpy as np


rootDir = "/data/Dan/ava_v2_1/frames/"
saveDirNorm = "/data/truppr/ava_v2_1/numpy_files/frames/"
saveDirFlip = "/data/truppr/ava_v2_1/numpy_files/flip-frames/"
fileList = "/data/truppr/ava_v2_1/total_files_reverse.txt"

dirs = open(fileList, 'r').readlines()

for dir in dirs:
    # print(saveDirNorm + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5))
    # print(saveDirFlip + "/flip-" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5))
   

    # Root Dirs
    targetDirRootArr = []
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")

    # Save Dirs Normal
    targetDirSaveArrNorm = []
    targetDirSaveArrNorm.append(saveDirNorm + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirSaveArrNorm.append(saveDirNorm + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirSaveArrNorm.append(saveDirNorm + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")

    # Save Dirs Flipped
    targetDirSaveArrFlip = []
    targetDirSaveArrFlip.append(saveDirFlip + "/flip-" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirSaveArrFlip.append(saveDirFlip + "/flip-" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirSaveArrFlip.append(saveDirFlip + "/flip-" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")


    index = 0
    for targetDirRoot in targetDirRootArr:
        print(targetDirRoot)
        print(targetDirSaveArrNorm[index])
        print(targetDirSaveArrFlip[index])
        # index += 1;
        # continue

        # print("Working with " + str(len(glob.glob(targetDirRoot + "*.jpg"))) + " files")
        # for filename in glob.glob(targetDirRoot + "*.jpg"):
        if os.path.exists(targetDirSaveArrNorm[index]):
            print("\tSkipping... ", targetDirSaveArrNorm[index])
            index += 1
            continue
        else:
            if not os.path.exists(saveDirNorm + "/" + dir.split(",")[0] + "/"):
                os.mkdir(saveDirNorm + "/" + dir.split(",")[0] + "/")
            if not os.path.exists(targetDirSaveArrNorm[index]):
                os.mkdir(targetDirSaveArrNorm[index])

        if os.path.exists(targetDirSaveArrFlip[index]):
            print("\tPath exists for ", targetDirSaveArrFlip[index])
        else:
            if not os.path.exists(saveDirFlip + "/flip-" + dir.split(",")[0] + "/"):
                os.mkdir(saveDirFlip + "/flip-" + dir.split(",")[0] + "/")
            if not os.path.exists(targetDirSaveArrFlip[index]):
                os.mkdir(targetDirSaveArrFlip[index])
        
        for filename in sorted(glob.glob(targetDirRoot + "*.jpg")):
            # print(index)
            print("\t" + filename)
            pic = Image.open(filename)
            # print(pic.size)
            img = np.array(pic.getdata()).reshape(pic.size[0], pic.size[1], 3)


            ### Save as numpy file
            save_name = targetDirSaveArrNorm[index] + "/" + filename.split('/')[-1].replace(".jpg",'')
            print("\tSaving to: ", save_name)
            np.save(save_name +'.npy', img)            

            ### Save as flipped numpy files
            img = np.fliplr(img)
            save_name = targetDirSaveArrFlip[index] + "/" + filename.split('/')[-1].replace(".jpg",'')
            print("\tSaving to: ", save_name)
            np.save(save_name +'.npy', img)

        ### Create GT for flipped images...
       
        index += 1;
        
