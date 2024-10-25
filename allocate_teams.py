def allocate_teams(student_list):
    all_students = student_list[:]
    remaining_students = student_list[:]
    group_list = [[] for i in range(10)]
    #picks 1 to 4
    for i in range(4):
        if i % 2 == 0:
            index = -1
        else:
            index = 0
    
        for group_num in range(len(group_list)):
            next_student = remaining_students[index]
            group = group_list[group_num]
            if exceed_check(group, next_student):
                if swapper(next_student, all_students, remaining_students, group_list, group_num, group):
                    pass
                else:
                    print("error 2")
            else:
                next_student[5] = True
                next_student[6] = group_num
                group.append(next_student)
                pprint.pprint(remaining_students)
                print(next_student)
                remaining_students.remove(next_student)
    
    groupcgpa = []
    for groupnum in range(len(group_list)):
        cgpa = 0
        for student in group_list[groupnum]:
            cgpa += student[1]
        groupcgpa.append([groupnum, cgpa])
    # pprint.pprint(groupcgpa)

    sorted = []
    for group in groupcgpa:
        sort_by_cgpa(group, group[1], sorted)
    groupcgpa = []
    pprint.pprint(sorted)

    # pprint.pprint(remaining_students)
    for i in range(len(remaining_students)):
        group_num = sorted[i][0]
        group = group_list[group_num]
        student = remaining_students[-1]
        if exceed_check(group, student):
            if swapper(student, all_students, remaining_students, group_list, group_num, group):
                    pass
            else:
                student[6] = group_num
                student[5] = True
                group.append(student)
                remaining_students.remove(student)
        else:
            student[6] = group_num
            student[5] = True
            group.append(student)
            remaining_students.remove(student)

    for groupnum in range(len(group_list)):
        cgpa = 0
        for student in group_list[groupnum]:
            cgpa += student[1]
        groupcgpa.append([groupnum, cgpa])
    pprint.pprint(groupcgpa)

    sorted = []
    for group in groupcgpa:
        sort_by_cgpa(group, group[1], sorted)
    groupcgpa = []
    # pprint.pprint(sorted)

    pprint.pprint(group_list)

def swap_validator(student, try_student, group_list, group_num, group):
    if not exceed_check(group, try_student):
        #try student has group assigned
        if try_student[5] == True:
            try_student_group_copy = group_list[try_student[6]][:]
            try_student_group_copy.remove(try_student)
            if not exceed_check(try_student_group_copy, student):
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def swapper(student, all_students, remaining_students, group_list, group_num, group):
    index = find_index(student, all_students)
    swap = False
    search_up, search_down = True, True
    index_up, index_down = 1, 1
    #loop through every student to check if can swap
    while search_up == True or search_down == True:
        #check if there are still any more students of higher/lower gpa to check
        if index + index_up > len(all_students) - 1:
            search_up = False
        if index - index_down < 0:
            search_down = False
        
        if search_up == True:
            try_student = all_students[index + index_up]
            if swap_validator(student, try_student, group_list, group_num, group):
                swap = True
                swap_student = try_student
                break

        if search_down == True:
            try_student = all_students[index - index_down]
            if swap_validator(student, try_student, group_list, group_num, group):
                swap = True
                swap_student = try_student
                break

        index_up += 1
        index_down += 1

    if swap == True:
        perform_swap(student, swap_student, remaining_students, group_num, group_list, group)
        return True
    else:
        return False

def perform_swap(student, swap_student, remaining_students, group_num, group_list, group):
    #swap student already assigned group
    if swap_student[5] == True:
        swap_student_group_num = swap_student[6]
        swap_student_group = group_list[swap_student_group_num]
        #put student into swap group
        student[5] = True
        student[6] = swap_student_group_num
        swap_student_group.remove(swap_student)
        swap_student_group.append(student)
        if student in remaining_students:
            remaining_students.remove(student)

        #put swap student into group
        swap_student[5] = True
        swap_student[6] = group_num
        group.append(swap_student)
        if swap_student in remaining_students:
            remaining_students.remove(swap_student)
    #swap student not assigned group
    else:
        swap_student[5] = True
        swap_student[6] = group_num
        group.append(swap_student)
        if swap_student in remaining_students:
            remaining_students.remove(swap_student)

def find_index(value, list):
    for index in range(len(list)):
        if list[index] == value:
            return index

def increase_count(dict, key):
    if key not in dict:
        dict[key] = 1
    else:
        dict[key] += 1

def exceed_check(group, new_student):
    schools = {}
    genders = {}
    #tally current genders and schools for each group
    for existing_student in group:
        #student[id, cgpa, gender, name, school, assigned, group number]
        increase_count(schools, existing_student[4])
        increase_count(genders, existing_student[2])
    #add gender and school of new student
    increase_count(schools, new_student[4])
    increase_count(genders, new_student[2])
    for school_count in schools.values():
        if school_count > 2:
            return True
    for gender_count in genders.values():
        if gender_count > 3:
            return True
    return False

def sort_by_cgpa(to_sort, cgpa, output):
    if output == []:
        output.append(to_sort)
        return
        
    #loop through each existing entry to find where to insert current entry based on cgpa
    index = 0
    for entry in output: 
        entry_cgpa = entry[1]
        if cgpa > entry_cgpa:
            #move right in list
            index += 1
            #at end of list
            if index == len(output):
                output.append(to_sort)
                return
            continue
        elif cgpa <= entry_cgpa:
            output.insert(index, to_sort)
            return
        



from read_to_dict import read_to_dict
import pprint

student_data = read_to_dict("records.csv")
tutorial_group = student_data["G-31"]

output = []
for id, data in tutorial_group.items():
    student_data = [id, data['CGPA'], data['Gender'], data['Name'], data['School'], data['Assigned'], data['Group Number']]
    cgpa = student_data[1]
    sort_by_cgpa(student_data, cgpa, output)
# pprint.pprint(output)
allocate_teams(output)