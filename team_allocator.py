def allocate_teams(sorted_list):
    group_list = [[] for i in range(10)]

    #add highest gpa 
    for group in group_list:
        next_highest_student = sorted_list.pop()
        group.append(next_highest_student)
    #add lowest gpa
    for group in group_list:
        next_lowest_student = sorted_list.pop(0)
        group.append(next_lowest_student)
    #add highest gpa, check school
    for group in group_list:
        next_highest_student = sorted_list.pop()
        check_if_exceed(group, next_highest_student)
        group.append(next_highest_student)
    # #add lowest gpa, check shool, check gender
    # for group in group_list:
    #     student = sorted_list.pop(0)
    #     check_if_exceed(group, student)
    # #add the rest, check school, check gender


    # print(group_list)
    pprint.pprint(group_list)

def increase_count(dict, key):
    if key not in dict:
        dict[key] = 1
    else:
        dict[key] += 1

def check_if_exceed(group, new_student):
    schools = {}
    genders = {}
    #tally gender and school for existing students in group
    for existing_student in group:
        #student[id, cgpa, gender, name, school]
        school = existing_student[4]
        gender = existing_student[2]
        increase_count(schools, school)
        increase_count(genders, gender)
    #add gender and school for new student
    new_school = new_student[4]
    new_gender = new_student[2]
    increase_count(schools, new_school)
    increase_count(genders, new_gender)
    print(schools)
    print(genders)
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
    sorted_list = []
    for id, data in tutorial_group.items():
        student_data = [id, data['CGPA'], data['Gender'], data['Name'], data['School']]
        cgpa = data['CGPA']
        #first entry
        if sorted_list == []:
            sorted_list.append(student_data)
            continue
        
        #loop through each existing entry to find where to insert current entry based on cgpa
        index = 0
        for entry in sorted_list: 
            entry_cgpa = entry[1]
            if cgpa > entry_cgpa:
                index += 1
                #cgpa higher than any other cgpa, so append to end of list
                if index == len(sorted_list):
                    sorted_list.append(student_data)
                    break
                continue
            elif cgpa <= entry_cgpa:
                sorted_list.insert(index, student_data)
                break


    return sorted_list

from read_to_dict import read_to_dict
import pprint

student_data_dict = read_to_dict("records.csv")
testdata = {'1075': {'CGPA': 4.08,
          'Gender': 'Male',
          'Name': 'Felix Yip',
          'School': 'CoB (NBS)'},
 '1271': {'CGPA': 4.17,
          'Gender': 'Female',
          'Name': 'Priya Singh',
          'School': 'SSS'},
 '1329': {'CGPA': 3.85,
          'Gender': 'Male',
          'Name': 'Nguyen Van Sam',
          'School': 'ASE'},
 '1383': {'CGPA': 4.19,
          'Gender': 'Female',
          'Name': 'Areeba Khan',
          'School': 'CoB (NBS)'},
 '1417': {'CGPA': 4.12,
          'Gender': 'Male',
          'Name': 'Darren Lee',
          'School': 'CoE'},
 '1555': {'CGPA': 4.04,
          'Gender': 'Female',
          'Name': 'Prerna Gupta',
          'School': 'MAE'},
 '162': {'CGPA': 4.07,
         'Gender': 'Female',
         'Name': 'Lila Patel',
         'School': 'SSS'},
 '1645': {'CGPA': 3.93,
          'Gender': 'Male',
          'Name': 'Zachary Wu',
          'School': 'CoE'},
 '1841': {'CGPA': 4.12,
          'Gender': 'Male',
          'Name': 'Jett Morales',
          'School': 'MAE'},
 '2069': {'CGPA': 4.48,
          'Gender': 'Female',
          'Name': 'Kathy Lau',
          'School': 'SSS'},
 '2091': {'CGPA': 4.2,
          'Gender': 'Male',
          'Name': 'Adlan Bin Rahman',
          'School': 'EEE'},
 '2115': {'CGPA': 4.03,
          'Gender': 'Female',
          'Name': 'Anya Kumar',
          'School': 'EEE'},
 '2151': {'CGPA': 4.02,
          'Gender': 'Female',
          'Name': 'Mei Hong',
          'School': 'EEE'},
 '2230': {'CGPA': 4.18,
          'Gender': 'Female',
          'Name': 'Harlow Wang',
          'School': 'ASE'},
 '2326': {'CGPA': 3.95,
          'Gender': 'Female',
          'Name': 'Vivi Dwi',
          'School': 'CoB (NBS)'},
 '235': {'CGPA': 4.06,
         'Gender': 'Male',
         'Name': 'Ming Zhang',
         'School': 'CCDS'},
 '2353': {'CGPA': 3.95,
          'Gender': 'Female',
          'Name': 'Karen Wong',
          'School': 'SBS'},
 '2417': {'CGPA': 3.88,
          'Gender': 'Female',
          'Name': 'Truong Minh Chau',
          'School': 'SSS'},
 '2650': {'CGPA': 4.09,
          'Gender': 'Female',
          'Name': 'Nurul Shafika',
          'School': 'SoH'},
 '2776': {'CGPA': 4.14,
          'Gender': 'Male',
          'Name': 'Siddharth Nair',
          'School': 'CCEB'},
 '2818': {'CGPA': 4.09,
          'Gender': 'Male',
          'Name': 'Oliver Tan',
          'School': 'CoB (NBS)'},
 '288': {'CGPA': 4.01,
         'Gender': 'Male',
         'Name': 'Ajay Verma',
         'School': 'CoB (NBS)'},
 '3148': {'CGPA': 3.88,
          'Gender': 'Male',
          'Name': 'Gabriel Young',
          'School': 'EEE'},
 '3628': {'CGPA': 4.06,
          'Gender': 'Male',
          'Name': 'Omer Ahmed',
          'School': 'EEE'},
 '3838': {'CGPA': 4.05,
          'Gender': 'Female',
          'Name': 'Aarti Nair',
          'School': 'EEE'},
 '3861': {'CGPA': 4.52,
          'Gender': 'Female',
          'Name': 'Layla Torres',
          'School': 'ASE'},
 '3930': {'CGPA': 4.18, 'Gender': 'Female', 'Name': 'Xun Wei', 'School': 'EEE'},
 '3989': {'CGPA': 4.15,
          'Gender': 'Male',
          'Name': 'Anthony Liu',
          'School': 'WKW SCI'},
 '4338': {'CGPA': 4.22,
          'Gender': 'Female',
          'Name': 'Sana Jain',
          'School': 'SPMS'},
 '4402': {'CGPA': 4.08,
          'Gender': 'Female',
          'Name': 'Grace Turner',
          'School': 'CCDS'},
 '4479': {'CGPA': 4.11,
          'Gender': 'Female',
          'Name': 'Amelia Kim',
          'School': 'CCDS'},
 '4520': {'CGPA': 4.11,
          'Gender': 'Male',
          'Name': 'Henry Foster',
          'School': 'EEE'},
 '4563': {'CGPA': 4.01,
          'Gender': 'Female',
          'Name': 'Anjali Patel',
          'School': 'WKW SCI'},
 '4576': {'CGPA': 4.03, 'Gender': 'Male', 'Name': 'Jie Zhang', 'School': 'EEE'},
 '4657': {'CGPA': 4.0,
          'Gender': 'Male',
          'Name': 'Oleg Petrovich',
          'School': 'SoH'},
 '4820': {'CGPA': 4.22,
          'Gender': 'Female',
          'Name': 'Meera Singh',
          'School': 'CoE'},
 '5002': {'CGPA': 4.02,
          'Gender': 'Male',
          'Name': 'Aarav Singh',
          'School': 'CCDS'},
 '5119': {'CGPA': 4.04,
          'Gender': 'Female',
          'Name': 'Nhung Vu',
          'School': 'ADM'},
 '527': {'CGPA': 4.06,
         'Gender': 'Male',
         'Name': 'Mohit Desai',
         'School': 'EEE'},
 '5477': {'CGPA': 4.09,
          'Gender': 'Male',
          'Name': 'Vikram Desai',
          'School': 'SoH'},
 '567': {'CGPA': 4.03,
         'Gender': 'Female',
         'Name': 'Isabella Thompson',
         'School': 'CoB (NBS)'},
 '5703': {'CGPA': 4.12,
          'Gender': 'Female',
          'Name': 'Karen Lee',
          'School': 'SPMS'},
 '5708': {'CGPA': 4.2,
          'Gender': 'Male',
          'Name': 'Ananya Ramesh',
          'School': 'SoH'},
 '588': {'CGPA': 4.06,
         'Gender': 'Male',
         'Name': 'Lucas Walker',
         'School': 'MAE'},
 '592': {'CGPA': 4.11,
         'Gender': 'Female',
         'Name': 'Zara Chang',
         'School': 'MSE'},
 '659': {'CGPA': 4.2,
         'Gender': 'Female',
         'Name': 'Maria Ivanovna',
         'School': 'SSS'},
 '71': {'CGPA': 4.19,
        'Gender': 'Female',
        'Name': 'Savannah Taylor',
        'School': 'SoH'},
 '75': {'CGPA': 4.03,
        'Gender': 'Female',
        'Name': 'Sakina Ahmed',
        'School': 'CCDS'},
 '809': {'CGPA': 4.26,
         'Gender': 'Female',
         'Name': 'Nisha Das',
         'School': 'CoB (NBS)'},
 '945': {'CGPA': 4.1, 'Gender': 'Female', 'Name': 'Han Li', 'School': 'MAE'}}
sorted = sort_by_cgpa(testdata)
allocate_teams(sorted)
