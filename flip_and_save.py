import os
import sys
import glob
import torch
import numpy as np
from skimage import io, exposure, img_as_uint, img_as_float

rootDir = "/data/Dan/ava_v2_1/frames/"
saveDirNormNUM = "/data/truppr/ava_v2_1/numpy_files/frames/"
saveDirFlipNUM = "/data/truppr/ava_v2_1/numpy_files/flip-frames/"
saveDirFlipRGB = "/data/truppr/ava_v2_1/flipped_frames/"
fileList = "/data/truppr/ava_v2_1/total_files1.txt"

dirs = open(fileList, 'r').readlines()

for dir in dirs:
    # print(saveDirNorm + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5))
    # print(saveDirFlip + "/flip-" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5))
   
    # Root Dirs
    targetDirRootArr = []
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirRootArr.append(rootDir + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")

    # Save Dirs Normal - NUMPY
    targetDirSaveArrNormNUM = []
    targetDirSaveArrNormNUM.append(saveDirNormNUM + "/" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirSaveArrNormNUM.append(saveDirNormNUM + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirSaveArrNormNUM.append(saveDirNormNUM + "/" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")

    # Save Dirs Flipped - NUMPY
    targetDirSaveArrFlipNUM = []
    targetDirSaveArrFlipNUM.append(saveDirFlipNUM + "/flip-" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirSaveArrFlipNUM.append(saveDirFlipNUM + "/flip-" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirSaveArrFlipNUM.append(saveDirFlipNUM + "/flip-" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")

    # Save Dirs Flipped - RGB
    targetDirSaveArrFlipRGB = []
    targetDirSaveArrFlipRGB.append(saveDirFlipRGB + "/flip-" + dir.split(",")[0] + "/" +  str(dir.split(",")[1]).zfill(5) + "/")
    targetDirSaveArrFlipRGB.append(saveDirFlipRGB + "/flip-" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) - 1).zfill(5) + "/")
    targetDirSaveArrFlipRGB.append(saveDirFlipRGB + "/flip-" + dir.split(",")[0] + "/" +  str(int(dir.split(",")[1]) + 1).zfill(5) + "/")


    index = 0
    for targetDirRoot in targetDirRootArr:
        print(targetDirRoot)
        print(targetDirSaveArrNormNUM[index])
        print(targetDirSaveArrFlipNUM[index])

        print(targetDirSaveArrFlipRGB[index])

        ### MAKE SURE file system is prepared
        if os.path.exists(targetDirSaveArrNormNUM[index]):
            print "\tSkipping... ", targetDirSaveArrNormNUM[index]
            index += 1
            continue
        else:
            if not os.path.exists(saveDirNormNUM + "/" + dir.split(",")[0] + "/"):
                os.mkdir(saveDirNormNUM + "/" + dir.split(",")[0] + "/")
            if not os.path.exists(targetDirSaveArrNormNUM[index]):
                os.mkdir(targetDirSaveArrNormNUM[index])
        
        if os.path.exists(targetDirSaveArrFlipNUM[index]):
            print "\tSkipping: path exists for ", targetDirSaveArrFlipNUM[index]
        else:
            if not os.path.exists(saveDirFlipNUM + "/flip-" + dir.split(",")[0] + "/"):
                os.mkdir(saveDirFlipNUM + "/flip-" + dir.split(",")[0] + "/")
            if not os.path.exists(targetDirSaveArrFlipNUM[index]):
                os.mkdir(targetDirSaveArrFlipNUM[index])
       
        if os.path.exists(targetDirSaveArrFlipRGB[index]):
            print "\tSkipping: path exists for ", targetDirSaveArrFlipRGB[index]
        else:
            if not os.path.exists(saveDirFlipRGB + "/flip-" + dir.split(",")[0] + "/"):
                os.mkdir(saveDirFlipRGB + "/flip-" + dir.split(",")[0] + "/")
            if not os.path.exists(targetDirSaveArrFlipRGB[index]):
                os.mkdir(targetDirSaveArrFlipRGB[index])

        for filename in sorted(glob.glob(targetDirRoot + "*.jpg")):
            ### OPEN Image
            orig = io.imread(filename) 
            img = io.imread(filename)
            img = np.fliplr(np.flipud(img))


            ### Save original as numpy file
            save_name = targetDirSaveArrNormNUM[index] + "/" + filename.split('/')[-1].replace(".jpg",'')
            print "\tSaving to: ", save_name
            np.save(save_name +'.npy', img)            
            
            ### Save as flipped numpy files
            img = np.flipud(img)
            save_name = targetDirSaveArrFlipNUM[index] + "/" + filename.split('/')[-1].replace(".jpg",'')
            np.save(save_name +'.npy', img)
            
            ### Save flipped RGB as jpg file
            save_name = targetDirSaveArrFlipRGB[index] + "/" + filename.split('/')[-1].replace(".jpg",'')
            io.imsave(save_name +'.jpg', img)


        index += 1;
        
