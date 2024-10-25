# l = []
# with open('records.csv','r') as f:
#     xkeys = f.readline().strip().split(',')
#     tg =''
#     for line in f:
#         line = line.strip().split(',')
#         if line[0] != tg:
#             newdict = {}
#             newdict[line[1]] = {xkeys[0]:line[0],xkeys[2]:line[2],xkeys[3]:line[3],xkeys[4]:line[4],xkeys[5]:float(line[5])}
#             l.append(newdict)
#             tg = line[0]
#         else:
#             newdict[line[1]] = {xkeys[0]:line[0],xkeys[2]:line[2],xkeys[3]:line[3],xkeys[4]:line[4],xkeys[5]:float(line[5])}

from read_to_dict import read_to_dict 


data = read_to_dict("records.csv")

def sorter(tg):
    sortedlist = []
    for ID,data in tg.items():
        sortedlist.append([ID,data['CGPA'],data['School'],data['Gender']])
        sortedlist.sort(key = lambda x: x[1])
        low = sortedlist[0:20]
        mid = sortedlist[20:40]
        high = sortedlist[40:50]
    return high,mid,low

def increase_count(dict, key):
    if key not in dict:
        dict[key] = 1
    else:
        dict[key] += 1

def exceed_value(group, new_student):
    # returns 0 if new student satisfies requirement
    # returns is 2 if both gender and schools dont match requirement
    # returns is 1 if one of gender and schools dont match requirement  
    exceed_value = 0
    schools = {}
    genders = {}
    #tally gender and school for existing students in group
    for existing_student in group:
        school = existing_student[2]
        gender = existing_student[3]
        increase_count(schools, school)
        increase_count(genders, gender)
    #add gender and school for new student
    new_school = new_student[2]
    new_gender = new_student[3]
    increase_count(schools, new_school)
    increase_count(genders, new_gender)
    for school_count in schools.values():
        if school_count > 2:
            exceed_value += 1
    for gender_count in genders.values():
        if gender_count > 3:
            exceed_value += 1       
    return exceed_value
    
def finder(group, inputlist):
    # finds best student to add into group
    for i in inputlist:
        if exceed_value(group, i) == 0:
            return i
    for i in inputlist:
        if exceed_value(group, i) == 1:
            return i
    return inputlist[0]

    

def picker(tup):
    high,mid,low = tup[0],tup[1],tup[2]
    tglist = []
    for i in range(10):
        #group = [low.pop(0),low.pop(-1),mid.pop(0),mid.pop(-1),high.pop(-1)]
        group = [low.pop(0), high.pop(-1)]

        student = finder(group,low[::-1])
        low.remove(student)
        group.append(student)

        student = finder(group,mid)
        mid.remove(student)
        group.append(student)

        student = finder(group,mid[::-1])
        mid.remove(student)
        group.append(student)

        tglist.append(group)
    return tglist

def grouper(tg):
    return picker(sorter(tg))

sucess = 0
half_sucess = 0
fail = 0

def findsucess(tg):
    sucess = 0
    half_sucess = 0
    fail = 0
    for i in grouper(data[tg]): #e.g for first tg
        error = 0
        schools ={}
        genders = {}
        for student in i:
            increase_count(schools, student[2])
            increase_count(genders, student[3])
        for schoolnum in schools.values():
            if schoolnum > 2:
                error += 1
        for gendersnum in genders.values():
            if gendersnum > 3:
                error += 1
        if error == 2:
            fail += 1
        elif error == 1:
            half_sucess += 1
        else:
            sucess += 1
    return(sucess,half_sucess,fail)
 
for tg in data.keys():
    a,b,c = findsucess(tg)
    sucess += a
    half_sucess += b
    fail += c

print(f'sucess: {sucess}, half_sucess: {half_sucess}, fail: {fail}')
 
# gpatotal_list = []
# for i in grouper(data['G-1']): #total gpas for each group in first tg
#     total = 0
#     for student in i:
#         total += student[1]
#     gpatotal_list.append(round(total,2))
# print(gpatotal_list)

# from statistics import stdev
# print(stdev(gpatotal_list))

#edit the main dictionary to include the teams of the students
for tgname,tg in data.items():  
    groupedtg = grouper(tg)
    for count,group in enumerate(groupedtg):
        for student in group:
            studentid = student[0]
            data[tgname][studentid]['Team Assigned'] = 'Team ' + str(count+1)





import pprint

#pprint.pprint(data['G-1'])



