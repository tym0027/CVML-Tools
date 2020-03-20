import xml.etree.ElementTree as etree
import sys

action_list = {"give" : '1', "take" : '2', "background": '3', "xfr-from" : '-1', "xfr-to" : '-1', "3d-xfr-to" : '-1', "3d-xfr-from" : '-1'}

cvat_file = sys.argv[1]
tree = etree.parse(cvat_file)
root = tree.getroot()

# wONG7Vh87B4,1555,0.142,0.024,0.408,0.978,2,404

width = root[1][0][-1][0].text
height = root[1][0][-1][1].text
video_data = root[1][0][1].text

# TODO: CHECK FRAME RATE:
# ffmpeg -i ./original-data/cam20-p2p-1.mp4 2>&1 | sed -n "s/.*, \(.*\) fp.*/\1/p"
FRAME_RATE = 30 # 29.9

for index, entry in enumerate(root):
    if entry.tag != 'track':
        continue
  
    person_id = 'X'
    action = root[index].attrib['label']
    frame = root[index][0].attrib['frame']
    bb = [root[index][0].attrib['xtl'], root[index][0].attrib['ytl'], root[index][0].attrib['xbr'], root[index][0].attrib['ybr']]
    for i in range(0, len(bb)):
        if i in [0, 2]:
            bb[i] = "%.3f" % (float(bb[i]) / float(width))
        elif i in [1, 3]:
            bb[i] = "%.3f" % (float(bb[i]) / float(height))

    second = str(int((float(frame) * 10) / FRAME_RATE) + 1)

    if action in action_list.keys():
        line = [video_data,second,bb[0],bb[1],bb[2],bb[3],action_list[action], person_id]
    else:
        line = [video_data,second,bb[0],bb[1],bb[2],bb[3],'-1', person_id]

    print(",".join(line))

