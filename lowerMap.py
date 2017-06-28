#import json
import math

min_height=9999.0
max_height=-9999.0
mylines=[]
with open('tq02m.asc', 'r') as f:
    lines = f.readlines()
    for i in xrange(len(lines)):
        listnb = map(float, lines[i].split())
        for fg in listnb:
            if ((fg<min_height) and ( fg!=-9999.0)):
                min_height = fg
            if ((fg>max_height) and ( fg!=9999.0)):
                max_height = fg
        mylines.append(listnb)
min_height = math.floor(min_height)
print min_height
max_height = math.ceil(max_height)
print max_height
margin_floor=10.0
additional_height=10.0

h_scale = 1.0#(max_height - min_height + margin_floor+additional_height)/(max_height-(-9999.0))

with open('tq-hmp.asc', 'w') as outfile:
    #    json.dump(mylines, outfile)
    for i in xrange(len(mylines)):
        for j in xrange(len(mylines[i])):
            if mylines[i][j]==-9999.0:
                mylines[i][j]=min_height-margin_floor
            else:
                mylines[i][j]-=1
        ln = " ".join(str(s) for s in mylines[i])
        ln = ln+"\n"
        outfile.write("".join(ln))

# with open('tq02m_WDraster_43200.asc', 'r') as f:
#    # lines = f.readlines()
#    # for i in xrange(len(lines)):
#        # listnb = map(float, lines[i].split())
#        # for j in xrange(len(mylines[i])):
#            # if listnb[j]>0.0:
#                # mylines[i][j]=mylines[i][j]+(listnb[j]*h_scale)+1#+2.0
#            # #else:
#            # #    mylines[i][j]=min_height-margin_floor
# #print mylines[108]
# #with open('WDraster_43200.json', 'w') as outfile:
# #    json.dump(mylines, outfile)
# with open('WH_43200.asc', 'w') as outfile:
#    # #    json.dump(mylines, outfile)
#    # for i in xrange(len(mylines)):
#        # #ln = "".join(str(mylines[i]))
#        # #ln = "".join(str(mylines[i])for item in mylines[i])
#        # ln = " ".join(str(s) for s in mylines[i])
#        # ln = ln+"\n"
#        # outfile.write("".join(ln))
