### README ###
# usage file for T. A. Rupprecht's CVML-tool's dataset maker 03/23/2020
#
# NOTE: Both CVAT annotations and the described scripts are needed to parse original data 
# into an ava formatted dataset

### USEGAGEs ###

# 1. create_ava_formated_gt,py
#
# 	This script takes an cvat annotation file in the CVAT csv video format (version 1.1) 
# 	and converts it into a groundtruth file using formatting used by the AVA dataset


# print ground truth to screen
python ./create_ava_formated_gt.py cam20-p2p-2.xml

# create ground truth file named clasp_datatset_20200227.txt
python ./create_ava_formated_gt.py cam20-p2p-2.xml > ./clasp_datatset_20200227.txt

# append to ground truth file names clasp_datatset_20200227.txt 
python ./create_ava_formated_gt.py cam20-p2p-2.xml >> ./clasp_datatset_20200227.txt


# 2. videoSnip.py
#
#	This script takes a text file (detailed below) listing filenames of .mp4 data in	
#	the ./original-data/ subdirectory and chops it up into .jpg frames in the 
# 	./dataset/ subdirectory.
#
#	Here is the resulting directory tree structure:
#	./datatset/->
#		->/VIDEO_NAME/
#			->/0000/-> ...
#			->/0001/-> ...
#			->/0002/-> ...
#				->/01.jpg
#				->/02.jpg
#				    ...
#				->/30.jpg 		# assuming 30 FPS
#
#	NOTE: some seconds have extra frames, or/and repeated frames in it's output.
#	This can be the result of ffmpeg using an 'inconvenient keyframe' in determining
#	the encoded time stamp, repeated frames in the original recorded data, or other because
#	of other encoding flaws. These errors do not propogate into future seconds. As in,
#	subdirectory ./datatset/VIDEO_NAME/2000/ will include events from the 2000th second of
#	the video data. One does not need to account for these errors for future frames.

# the only way to call the script, see originalData.txt for input file formatting
python ./videoSnip.py ./originalData.txt


# 3. ./originalData.txt
#
#	This is a plain textfile. Each line is the name of a mp4 file in the ./original-data subdirectory.
# 
# 	bellow is the output of my call to cat on the originalData.txt file. 
#	The resulting files are in my ./original-data subdirectory directory.

(base) truppr@server:~$ cat ./originalData.txt
cam20-p2p-1.mp4
cam20-p2p-2.mp4
cam20-xfr-1.mp4
cam20-xfr-2.mp4

