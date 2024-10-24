def allocate_teams(sorted_list):
    list_copy = sorted_list[:]
    group_list = [[] for i in range(10)]

    for i in range(4):
        if i % 2 == 0:
            index = -1
        else:
            index = 0
        for group_num in range(len(group_list)):
            next_student = list_copy[index]
            exceeded = check_if_exceed(group_list[group_num], next_student)
            if exceeded:
                a,b = swapper(next_student, group_list, sorted_list)
                if a != 0:
                    list_copy.pop(a)
                list_copy.pop(b)
            else:
                next_student[6] = group_num + 1
                next_student[5] = True
                group_list[group_num].append(next_student)
                list_copy.pop(index)
        pprint.pprint(group_list)
    pprint.pprint(group_list)

#checks if swapping will result in valid group
def swap_validator(student, test_student, group_list):
    student_group_num = student[6]
    test_student_group_num = test_student[6]
    student_group = group_list[student_group_num-1][:]
    #compare group assuming student is swapped out
    student_group.pop(student_group.index(student))
    if check_if_exceed(student_group, test_student) == False:
        #test student has group assigned, check if student can fit in the group
        if test_student_group_num != 0:
            test_student_group = group_list[test_student_group_num-1][:]
            #compare group assuming test student is swapped out
            test_student_group.pop(test_student_group.index(test_student))
            return not check_if_exceed(test_student_group, student)
        #test student has no group assigned, no need to check
        elif test_student_group_num == 0:
            return True
    else:
        return False


def swapper(student, group_list, student_list):
    #find closest cgpa student
    index = student_list.index(student)
    swap = False
    search_up, search_down = True, True
    index_up, index_down = 1, 1
    while search_up == True or search_down == True:
        if index + index_up > 49:
            search_up = False
        if index - index_down < 0:
            search_down = False
        
        if search_up == True:
            test_student = student_list[index + index_up]
            if swap_validator(student, test_student, group_list) == True:
                swap = True
                break
            else:
                continue

        if search_down == True:
            test_student = student_list[index - index_down]
            if swap_validator(student, test_student, group_list) == True:
                swap = True
                break
            else:
                continue

        index_up += 1
        index_down += 1

    if swap == True:
        student_group_num = student[6]
        student_group = group_list[student_group_num-1]
        if test_student[6] == 0:
            student_group.pop(student_group.index(student))
            student_group.append(test_student)
            test_student[6] = student_group_num
            student[6] = 0
            return 0, test_student
        else:
            test_student_group_num = test_student[6]
            test_student_group = group_list[test_student_group_num-1]
            student_group.pop(student_group.index(student))
            student_group.append(test_student)
            test_student_group.pop(test_student_group.index(test_student))
            test_student_group.append(student)
            student[6] = test_student_group_num
            test_student[6] = student_group_num
            return student, test_student
            

    #check if that student still exceeds in group
    #if not, set as student
    #if still exceeds, find next closest cgpa student


def increase_count(dict, key):
    if key not in dict:
        dict[key] = 1
    else:
        dict[key] += 1

def check_if_exceed(group, new_student):
    schools = {}
    genders = {}
    #tally current genders and schools for each group
    for existing_student in group:
        #student[id, cgpa, gender, name, school, assigned, group number]
        school = existing_student[4]
        gender = existing_student[2]
        increase_count(schools, school)
        increase_count(genders, gender)
    #add gender and school of new student
    new_school = new_student[4]
    new_gender = new_student[2]
    increase_count(schools, new_school)
    increase_count(genders, new_gender)
    for school_count in schools.values():
        if school_count > 2:
            print("School exceed")
            return True
    for gender_count in genders.values():
        if gender_count > 3:
            print("Gender exceed")
            return True
    return False

def sort_by_cgpa(tutorial_group):
    output = []
    for id, data in tutorial_group.items():
        student_data = [id, data['CGPA'], data['Gender'], data['Name'], data['School'], data['Assigned'], data['Group Number']]
        cgpa = data['CGPA']
        #first entry
        if output == []:
            output.append(student_data)
            continue
        
        #loop through each existing entry to find where to insert current entry based on cgpa
        index = 0
        for entry in output: 
            entry_cgpa = entry[1]
            if cgpa > entry_cgpa:
                #move right in list
                index += 1
                #at end of list
                if index == len(output):
                    output.append(student_data)
                    break
                continue
            elif cgpa <= entry_cgpa:
                output.insert(index, student_data)
                break

    return output

from read_to_dict import read_to_dict
import pprint

student_data_dict = read_to_dict("records.csv")
sorted = sort_by_cgpa(student_data_dict['G-1'])
pprint.pprint(sorted)
allocate_teams(sorted)
# pprint.pprint(sorted)
