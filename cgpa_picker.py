l = []
with open('records.csv','r') as f:
    xkeys = f.readline().strip().split(',')
    tg =''
    for line in f:
        line = line.strip().split(',')
        if line[0] != tg:
            newdict = {}
            newdict[line[1]] = {xkeys[0]:line[0],xkeys[2]:line[2],xkeys[3]:line[3],xkeys[4]:line[4],xkeys[5]:line[5]}
            l.append(newdict)
            tg = line[0]
        else:
            newdict[line[1]] = {xkeys[0]:line[0],xkeys[2]:line[2],xkeys[3]:line[3],xkeys[4]:line[4],xkeys[5]:line[5]}

    

def sorter(tg):
    sortedlist = []
    for ID,data in tg.items():
        sortedlist.append([ID,data['CGPA'],data['School'],data['Gender']])
        sortedlist.sort(key = lambda x: x[1])
        low = sortedlist[0:20]
        mid = sortedlist[20:40]
        high = sortedlist[40:50]
    return high,mid,low
        
def picker(tup):
    high,mid,low = tup[0],tup[1],tup[2]
    tglist = []
    for i in range(10):
        group = [low.pop(0),low.pop(-1),mid.pop(0),mid.pop(-1),high.pop(-1)]
        tglist.append(group)
    return tglist
        
for i in picker(sorter(l[0])): #e.g for first tg
    print(i)
