import sys

originalTruth = sys.argv[1]
additionalTruth = './withFlippedData-' + sys.argv[1]
# print "taking ", originalTruth, " and dumping into ", additionalTruth

data = open(originalTruth, 'r').readlines()
for d in data:
    parsed = d.split(",")
    # print d
    new_data = ["flip-" + parsed[0], parsed[1], str(1 - float(parsed[4])), parsed[3], str(1 - float(parsed[2])), parsed[5], parsed[6], parsed[7].replace("\n", '').replace("\r",'')]
    print ",".join(new_data)
