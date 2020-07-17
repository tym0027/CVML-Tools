import xml.etree.ElementTree as etree
import sys
import json
import numpy as np

# The niave way of computing bounding boxes...s
def niave(a, b):
    _a = np.array(a.strip('][').replace("'",'').split(', '), dtype=float)
    _b = np.array(b.strip('][').replace("'",'').split(', '), dtype=float)

    x = np.array([[_a[0], _a[2]],[_b[0], _b[2]]], dtype=float)
    y = np.array([[_a[1], _a[3]],[_b[1], _b[3]]], dtype=float)

    # print("x: ",x)
    # print("y: ",y)

    IoU = count = 0
    for indexi in range(0,x.shape[0] - 1):
        for indexj in range(indexi, x.shape[0]):
            if indexj == indexi:
                continue
            elif (x[indexi,0] <= x[indexj,0] <= x[indexi,1]) or (x[indexj,0] <= x[indexi,0] <= x[indexj,1]):
                if ((y[indexi,0] <= y[indexj,0] <= y[indexi,1]) or (y[indexj,0] <= y[indexi,0] <=  y[indexj,1])):
                    # print("Rectangle", indexi, "and rectangle", indexj, "intersect...")
                    intersection = (min(x[indexi,1],x[indexj,1]) - max(x[indexi,0],x[indexj,0])) * (min(y[indexi,1],y[indexj,1]) - max(y[indexi,0],y[indexj,0]))
                    union = ((x[indexi,1] - x[indexi,0]) * (y[indexi,1] - y[indexi,0])) + ((x[indexj,1] - x[indexj,0]) * (y[indexj,1] - y[indexj,0])) - intersection
                    area_target = (x[indexj,1] - x[indexj,0]) * (y[indexj,1] - y[indexj,0]) # or??? ((x[indexi,1] - x[indexi,0]) * (y[indexi,1] - y[indexi,0]))

                    IoU = intersection / union
                    IoU = intersection / area_target
                    count = count + 1;
    return IoU



def match_BB(f, a, o):
    ret_dict = {}
    # print()
    # print(a)
    # print(o)

    if a in f.keys():
        input("DUP KEY!!!")
    f[action] = {"human" : '', "bin" : ''}

    for obj in o:
        if o[obj] == "bin":
            f[action]["bin"] = obj
        elif o[obj] == "human":
            f[action]["human"] = obj
        else:
            ret_dict[obj] = o[obj]
    
    # del o[f[action]["bin"]]
    # del o[f[action]["human"]]

    return f, ret_dict

action_list = {"xfr-from" : '2', 
                "xfr-to" : '2', 
                "3d-xfr-to" : '2', 
                "3d-xfr-from" : '2', 
                "background": '3'}

object_list = ["give", "take", "human", "bin"]

object_file = "./" 

cvat_file = sys.argv[1]

object_file += cvat_file.replace(".xml", "-objects.json")

tree = etree.parse(cvat_file)
root = tree.getroot()

# wONG7Vh87B4,1555,0.142,0.024,0.408,0.978,2,404

width = root[1][0][-1][0].text
height = root[1][0][-1][1].text
video_data = root[1][0][1].text

# TODO: CHECK FRAME RATE:
# ffmpeg -i ./original-data/cam20-p2p-1.mp4 2>&1 | sed -n "s/.*, \(.*\) fp.*/\1/p"
FRAME_RATE = 30 # 29.9

obs = {}
acts = {}
for index, entry in enumerate(root):
    if entry.tag != 'track':
        continue
  
    person_id = '0'
    action = root[index].attrib['label']
    frame = root[index][0].attrib['frame']
    bb = [root[index][0].attrib['xtl'], root[index][0].attrib['ytl'], root[index][0].attrib['xbr'], root[index][0].attrib['ybr']]
   
    try:
        obs[frame.zfill(5)]
    except KeyError:
        obs[frame.zfill(5)] = {}
        acts[frame.zfill(5)] = {}

    for i in range(0, len(bb)):
        if i in [0, 2]:
            bb[i] = "%.3f" % (float(bb[i]) / float(width))
        elif i in [1, 3]:
            bb[i] = "%.3f" % (float(bb[i]) / float(height))

    second = str(int((float(frame) * 10) / FRAME_RATE) + 1).zfill(5)

    if action in object_list:
        try:
            obs[frame.zfill(5)][str(bb)]
            input("found duplicate obj key...")
        except KeyError:
            obs[frame.zfill(5)][str(bb)] = action
    else:
        if action in action_list.keys():
            line = [video_data,second,bb[0],bb[1],bb[2],bb[3],action_list[action], person_id]
        else:
            line = [video_data,second,bb[0],bb[1],bb[2],bb[3],'-1', person_id]

        print(",".join(line))
        
        try:
            acts[frame.zfill(5)][str(bb)]
            input("found duplicate act key...")
        except KeyError:
            acts[frame.zfill(5)][str(bb)] = action_list[action]

object_file = {}
for entry in sorted(acts.keys()):
    if entry not in obs.keys():
        continue
    
    # print(entry, acts[entry])
    for act in acts[entry]:
        # print(act)
        if acts[entry][act] == '3':
            continue
        elif acts[entry][act] == '2':
            # object_file[act] = {"bin" : '', "human" : ''}
            h = b = ''
            for o in obs[entry]:
                # print(obs[entry][o])
                # print(niave(act, o))
                iou = niave(act, o)
                #if iou > .1 and (obs[entry][o] == "give" or obs[entry][o] == "take"):
                #    input("ALERT Found give take stuff")
                if iou > .1 and obs[entry][o] == "bin":
                    b = o
                elif iou > .1 and obs[entry][o] == "human":
                    h = o
                    '''
                    if act not in object_file.keys():
                        print("2 FOUND HUMAN")
                        object_file[act] = {obs[entry][o] : o}
                    else:
                        print("1 FOUND HUMAN")
                        object_file[act][obs[entry][o]] = o
                    '''
                else:
                    pass # print("else")    

        if b != '' and h != '':
            object_file[act] = {"bin" : b, "human" : h}

        # print("cull obs")
        # print(obs[entry])
        if act in object_file.keys():
            for thing in object_file[act]:
                # print(thing, object_file[act])
                obs[entry].pop(object_file[act][thing])
        # print(obs[entry], len(obs[entry]))

   
    giver = taker = ''
    # print(obs[entry].values())
    if len(obs[entry].values()) == 2:
        for o in obs[entry]:
            if obs[entry][o] == "give" and giver == '':
                giver = o
            elif obs[entry][o] == "take" and taker == '':
                taker = o
            else:
                pass
                # print(obs[entry])
                # input("ALERT: Found some bullshit")
        
        if giver != '' and taker  != '':
            # print(giver, taker)
            # input("ALERT: Found P2P")
            g = giver.strip('][').replace("'",'').split(', ')
            t = taker.strip('][').replace("'",'').split(', ')
            # print(g, t)
            # print(min(g[0], t[0]), min(g[1], t[1]), max(g[2], t[2]), max(g[3], t[3]))

            line = [video_data, entry, min(g[0], t[0]), min(g[1], t[1]), max(g[2], t[2]), max(g[3], t[3]),'1', '0']
            print(",".join(line))

            # input("ALERT: Found P2P")
            
            # print([min(g[0], t[0]), min(g[1], t[1]), max(g[2], t[2]), max(g[3], t[3])])
            # input("ALERT: Found P2P")

            object_file[str([min(g[0], t[0]), min(g[1], t[1]), max(g[2], t[2]), max(g[3], t[3])])] = {"give" : g, "take" : t}
    else:
        # print(obs[entry])
        pass # input("ALERT: EDGE CASE")

    ''' 
        pass # object_file, give_take = match_BB(object_file, act, obs[entry])
    else:
        print("skipping...")
        '''


'''
for entry in sorted(acts.keys()):
    print(entry)
    for item in acts[entry]:
        if acts[entry][item] != "background":
            print("\n\t", item, acts[entry][item])

            act_BB = item
        else:
            continue

        give = take = bin = human = []
        for item in obs[entry]:
            if obs[entry][item] == "bin":
                bin.append(item)
            elif obs[entry][item] == "human":
                human.append(item)
            elif obs[entry][item] == "give":
                give.append(item)
            elif obs[entry][item] == "take":
                take.append(item)

         
        try:
            object_file[act_BB]
        except KeyError:
            object_file[act_BB] = {""}

        if len(take) == len(give) == 1:
            object_file[act_BB]["give"] = give[0]
            object_file[act_BB]["take"] = take[0]

        if len(bin) == len(human) == 1:
            object_file[act_BB]["human"] = human[0]
            object_file[act_BB]["bin"] = bin[0]
'''
print(object_file)
print(len(object_file.keys()))
