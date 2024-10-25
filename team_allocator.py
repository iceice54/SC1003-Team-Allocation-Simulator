def allocate_teams(student_list):
    student_copy = student_list[:]
    group_list = [[] for i in range(10)]
    count = 0
    for i in range(4):
        #1st and 3rd picks take highest cgpa, 2nd and 4th picks take lowest cgpa to balance cgpa
        if i % 2 == 0:
            index = -1
        else:
            index = 0
        #iterate through group 1 to 10
        for group_num in range(len(group_list)):
            next_student = student_list[index]
            #check if selected student will cause group to exceed
            exceed = exceed_check(group_list[group_num], next_student)
            next_student[6] = group_num + 1
            if exceed:
                #swap selected student with another valid student
                swap = swapper(student_list[-1], group_num - 1, group_list, student_copy, student_list)
                if swap == False:
                    student_list[-1][6] = group_num
                    student_list[-1][5] = True
                    group_list[group_num - 1].append(student_list[-1])
                    student_list.pop(-1)
            else:
                #add student to group
                next_student[6] = group_num + 1
                next_student[5] = True
                group_list[group_num].append(next_student)
                student_list.pop(index)
                count += 1
    cgpa = []
    for group in group_list:
        groupcgpa = 0
        groupncgpa = [group_list.index(group)+1]
        for student in group:
            groupcgpa += student[1]
        groupncgpa.append(groupcgpa)
        cgpa.append(groupncgpa)
    sortedcgpa = sort_groups_by_cgpa(cgpa)
    print(sortedcgpa)
    pprint.pprint(student_list)
    print("here")
    i=0
    while i < len(student_list):
        # pprint.pprint(student_list)
        group_num = sortedcgpa[i][0]
        if exceed_check(group_list[group_num - 1], student_list[-1]):
            # print(student_list[-1])
            # print(group_num)
            swap = swapper(student_list[-1], group_num - 1, group_list, student_copy, student_list)
            if swap == False:
                student_list[-1][6] = group_num
                student_list[-1][5] = True
                print(student_list[-1])
                group_list[group_num - 1].append(student_list[-1])
                student_list.pop(-1)
                print(student_list[-1])
        else:
            student_list[-1][6] = group_num
            student_list[-1][5] = True
            group_list[group_num - 1].append(student_list[-1])
            student_list.pop(-1)
        i += 1
        # pprint.pprint(group_list)
        

    cgpa = []
    for group in group_list:
        groupcgpa = 0
        groupncgpa = [group_list.index(group)+1]
        for student in group:
            groupcgpa += student[1]
        groupncgpa.append(groupcgpa)
        cgpa.append(groupncgpa)

    pprint.pprint(group_list)
    return cgpa
    

def exceed_check(group, new_student):
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
            return True
    for gender_count in genders.values():
        if gender_count > 3:
            return True
    return False

#checks if swapping will result in valid group
def swap_validator(student, try_student, group_list):
    student_group_copy = group_list[student[6]-1][:]
    if not exceed_check(student_group_copy, try_student):
        #test student has group assigned, check if student can fit in the group
        try_student_assigned = try_student[5]
        if try_student_assigned:
            try_student_group_copy = group_list[try_student[6]-1][:]
            #compare group assuming test student is swapped out
            try_student_group_copy.pop(try_student_group_copy.index(try_student))
            return not exceed_check(try_student_group_copy, student)
        #test student has no group assigned, no need to check
        else:
            return True
    else:
        return False

def swapper(next_student, group_num, group_list, student_list, student_real):
    # pprint.pprint(student_list)
    #find closest cgpa student
    index = student_list.index(next_student)
    swap = False
    search_up, search_down = True, True
    index_up, index_down = 1, 1
    #loop through every student to check if can swap
    while search_up == True or search_down == True:
        #check if there are still any more students of higher/lower gpa to check
        if index + index_up > len(student_list)-1:
            search_up = False
        if index - index_down < 0:
            search_down = False
        
        if search_up == True:
            try_student = student_list[index + index_up]
            if swap_validator(next_student, try_student, group_list):
                swap = True
                break

        if search_down == True:
            try_student = student_list[index - index_down]
            if swap_validator(next_student, try_student, group_list):
                swap = True
                break

        index_up += 1
        index_down += 1

    if swap == True:
        swap_student = try_student
        student_group_num = group_num + 1
        student_group = group_list[student_group_num-1]
        student_assigned = swap_student[5]
        if not student_assigned:
            # student_group.pop(student_group.index(next_student))
            student_group.append(swap_student)
            swap_student[6] = student_group_num
            swap_student[5] = True
            next_student[6] = 0
            next_student[5] = False
            student_list.pop(student_list.index(swap_student))
            # student_real.pop(student_real.index(swap_student))
            return
        else:
            swap_student_group_num = swap_student[6]
            swap_student_group = group_list[swap_student_group_num-1]
            # student_group.pop(student_group.index(next_student))
            student_group.append(swap_student)
            swap_student_group.pop(swap_student_group.index(swap_student))
            swap_student_group.append(next_student)
            next_student[6] = swap_student_group_num
            next_student[5] = True
            swap_student[6] = student_group_num
            swap_student[5] = True
            student_list.pop(student_list.index(next_student))
            # student_real.pop(student_real.index(swap_student))
            student_list.pop(student_list.index(swap_student))
            return
    else:
        return False

def increase_count(dict, key):
    if key not in dict:
        dict[key] = 1
    else:
        dict[key] += 1

def sort_tg_by_cgpa(tutorial_group):
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

def sort_groups_by_cgpa(groups):
    # [[1, 16.1], [2, 16.3]]
    output = []
    for group in groups:
        cgpa = group[1]

        if output == []:
            output.append(group)
            continue

        index = 0
        for entry in output:
            entry_cgpa = entry[1]
            if cgpa > entry_cgpa:
                #move right in list
                index += 1
                #at end of list
                if index == len(output):
                    output.append(group)
                    break
                continue
            elif cgpa <= entry_cgpa:
                output.insert(index, group)
                break
    return output

from read_to_dict import read_to_dict
import pprint

student_data_dict = read_to_dict("records.csv")
sorted = sort_tg_by_cgpa(student_data_dict['G-1'])
# pprint.pprint(sorted)
pprint.pprint(allocate_teams(sorted))
# for i in student_data_dict:
#     sorted = sort_tg_by_cgpa(student_data_dict[i])
#     pprint.pprint(allocate_teams(sorted))