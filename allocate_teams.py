import matplotlib.pyplot as plt
import ipywidgets as widgets
import math as math
def allocate_teams(student_list, students_per_group):
    num_of_groups = math.ceil(50 / students_per_group) 
    print(num_of_groups)
    all_students = student_list[:]
    remaining_students = student_list[:]
    group_list = [[] for i in range(num_of_groups)]

    
    num_to_pick = students_per_group - 1
    #assign 4 students to each group
    for i in range(num_to_pick):
        #1st and 3rd pick take highest cgpa
        if i % 2 == 0:
            index = -1
        #2nd and 4th pick take lowest cgpa
        else:
            index = 0
    
        for group_num in range(len(group_list)):
            next_student = remaining_students[index]
            group = group_list[group_num]
            if not exceed_gender_or_school(group, next_student, students_per_group):
                assign_group(next_student, group_num, group, remaining_students)
            else:
                if swapper(next_student, all_students, remaining_students, group_list, group_num, group):
                    pass
                else:
                    #if swapper cant find any valid target, just assign
                    assign_group(next_student, group_num, group, remaining_students)


    group_cgpa = []
    for group_num in range(len(group_list)):
        total_cgpa = 0
        for student in group_list[group_num]:
            total_cgpa += student[1]
        group_cgpa.append([group_num, cgpa])

    sorted_output = []
    for group in group_cgpa:
        add_and_sort_by_ascending_cgpa(group, group[1], sorted_output)
    #sorted_output[[0, 16.4], [1, 16.5], [7, 16.7], ...]

    #each group left 1 slot, assign based on gpa e.g. lowest gpa group picks highest gpa student
    i = 0
    while len(remaining_students) > 0:
        group_num = sorted_output[i][0]
        group = group_list[group_num]
        student = remaining_students[-1]
        if not exceed_gender_or_school(group, student, students_per_group):
            assign_group(student, group_num, group, remaining_students)
        else:
            if swapper(student, all_students, remaining_students, group_list, group_num, group):
                pass
            else:
                #if swapper cant find any valid target, just assign
                assign_group(student, group_num, group, remaining_students)    
        i+=1     

    return group_list

def assign_group(student, group_num, group, remaining_students):
    student[6] = group_num
    student[5] = True
    group.append(student)
    if student in remaining_students:
        remaining_students.remove(student)

def swap_validator(student, try_student, group_list, group, students_per_group):
    if exceed_gender_or_school(group, try_student, students_per_group):
        return False
    
    if try_student[5]:
        #create copy of try student group and remove try student to see 
        #if student will fit in try student group after swap
        try_student_group_copy = group_list[try_student[6]][:]
        try_student_group_copy.remove(try_student)
        return not exceed_gender_or_school(try_student_group_copy, student, students_per_group)
    else:
        return True

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
            if swap_validator(student, try_student, group_list, group, students_per_group):
                swap = True
                swap_student = try_student
                break

        if search_down == True:
            try_student = all_students[index - index_down]
            if swap_validator(student, try_student, group_list, group, students_per_group):
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
    if swap_student[5] == True:
        swap_student_group_num = swap_student[6]
        swap_student_group = group_list[swap_student_group_num]
        swap_student_group.remove(swap_student)
        assign_group(student, swap_student_group_num, swap_student_group, remaining_students)
        assign_group(swap_student, group_num, group, remaining_students)
    else:
        assign_group(swap_student, group_num, group, remaining_students)

def find_index(value, list):
    for index in range(len(list)):
        if list[index] == value:
            return index

def increase_count(dict, key):
    if key not in dict:
        dict[key] = 1
    else:
        dict[key] += 1

def exceed_gender_or_school(group, new_student, students_per_group):
    schools = {}
    genders = {}
    max_schools = students_per_group // 2
    max_genders = math.ceil(students_per_group / 2)

    #tally current genders and schools for each group
    for existing_student in group:
        #student[id, cgpa, gender, name, school, assigned, group number]
        increase_count(schools, existing_student[4])
        increase_count(genders, existing_student[2])
    #add gender and school of new student
    increase_count(schools, new_student[4])
    increase_count(genders, new_student[2])
    for school_count in schools.values():
        if school_count > max_schools:
            return True
    for gender_count in genders.values():
        if gender_count > max_genders:
            return True
    return False

def add_and_sort_by_ascending_cgpa(to_sort, cgpa, output):
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
        
#BELOW IS TO RUN AND ANALYSE

from read_to_dict import read_to_dict
import pprint

student_data_dict = read_to_dict("records.csv")

successful = 0
unsuccessful = 0
half = 0
stdevs = []
final_data = []
schoolfail = 0
genderfail = 0
totalcgpa = 0
mean_cgpas_per_tutorial_group = []
failedtg = []
gender_counts_failed_tg = {}
schoolnum=[]
numschool={}

students_per_group = 5

for tgnum in student_data_dict:
    output = []
    tutorial_group = student_data_dict[tgnum]
    cgpas = []
    for id, data in tutorial_group.items():
        student_data = [id, data['CGPA'], data['Gender'], data['Name'], data['School'], data['Assigned'], data['Group Number']]
        cgpa = student_data[1]
        add_and_sort_by_ascending_cgpa(student_data, cgpa, output)
        school = data['School']
        # Increment the count for the school
        numschool[school] = numschool.get(school, 0) + 1
        
    groupz = (allocate_teams(output, students_per_group))
    for group in groupz:
        for student in group:
            final_student_data = [tgnum, student[0],student[4],student[3],student[2],str(student[1]),str(student[6]+1)] #“Tutorial Group”, “Student ID”, “School”, “Name”, “Gender”, “CGPA”, "Team Assigned"
            final_data.append(final_student_data)
    
    for group in groupz:
        schoolpass = True
        genderpass = True
        cgpa = 0
        schools = {}
        genders = {}
        max_schools = students_per_group // 2
        max_genders = math.ceil(students_per_group / 2)
        print(max_schools, "school")
        print(max_genders)
        
        #tally current genders and schools for each group
        for student in group:
            cgpa += student[1]
            #student[id, cgpa, gender, name, school, assigned, group number]
            increase_count(schools, student[4])
            increase_count(genders, student[2])
        #add gender and school of new student 
        for school_count in schools.values():
            if school_count > max_schools:
                schoolpass = False
        for gender_count in genders.values():
            if gender_count > max_genders:
                genderpass = False 
        if not schoolpass and not genderpass:
            unsuccessful += 1
        elif not schoolpass:
            half += 1
            schoolfail += 1
        elif not genderpass:
            half += 1
            genderfail += 1
            #print(genders)
            #print(tgnum)
            failedtg.append(tgnum)# add the tutorial number with the failed group into a list
            failedtg = list(set(failedtg))# Ensures that if there are multiple groups with a tutorial group that fails the criteria, print the turtorial group number once
        else:
            successful += 1

        cgpas.append(cgpa)
      
    # Step 1: Compute the mean
    mean = sum(cgpas) / 10
    mean_cgpas_per_tutorial_group.append(mean)# Storing the mean of each tutorial group together in to a list
    # Step 2: Calculate squared differences
    squared_diffs = [(x - mean) ** 2 for x in cgpas]

    # Step 3: Calculate variance
    variance = sum(squared_diffs) / len(cgpas)

    # Step 4: Calculate standard deviation
    stdev = variance ** 0.5
    stdevs.append(stdev)   
with open('new_records.csv','w') as f:
    f.write('Tutorial Group,Student ID,School,Name,Gender,CGPA,Team Assigned\n')
    for i in final_data:
        f.writelines(','.join(i))
        f.write('\n')

# Data Analysis Part
    


print(f"{successful} are successful, {unsuccessful} are unsuccessful and {half} are half successful")

labels = ['Successful', 'Half Successful', 'Not Successful']
sizes = [successful,half,unsuccessful ]
colors = ['#99ff99', '#FFA500', '#C30000']

# Filter out segments with non-zero values for plotting
filtered_labels = [label for i, label in enumerate(labels) if sizes[i] > 0]
filtered_sizes = [size for size in sizes if size > 0]

# Calculate percentages, ensuring they sum to exactly 100%
total = sum(sizes)
percentages = [size / total * 100 for size in sizes]
percentages[-1] = 100 - sum(percentages[:-1])  # Adjust last percentage to ensure total is 100%

# Create the formatted labels with percentages for the legend
legend_labels = [f'{label}: {percentage:.1f}%' for label, percentage in zip(labels, percentages)]

# Define explode, colors, and start angle
explode = [0.5 if size > 0 else 0 for size in sizes]  # Explode the first non-zero segment
startangle = 140  # Rotate the chart so the first slice starts at 90 degrees

# Plot the pie chart with explode, colors, and startangle
fig, ax = plt.subplots()
wedges, _ = ax.pie(filtered_sizes,labels=filtered_labels,explode=[explode[i] for i, size in enumerate(sizes) if size > 0],colors=colors, startangle=140)

# Add the legend with percentage labels
ax.legend(wedges, legend_labels, title="Distribution of Success Cases", loc="best")
plt.axis('equal')
plt.show()

Barfig, Barax = plt.subplots()

failedcriteria = ['Failed the gender cases', 'Failed the school criteria']
counts = [genderfail, schoolfail]
bar_labels = ['red', 'red']
bar_colors = ['tab:red', 'tab:red']

bars = Barax.bar(failedcriteria, counts, label=bar_labels, color=bar_colors)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval}', ha='center', va='center')
    
Barax.set_ylabel('Number of failed cases')
Barax.set_title('Analysis of failed cases')

plt.show()# print bar graph for school fail and gender fail

# Iterate through the failed tutorial groups
for tgnum in failedtg:  # failedtg is the list of failed tutorial groups
    boys_count = 0
    girls_count = 0
    
    # Access the tutorial group's data
    tutorial_group = student_data_dict[tgnum]
    
    # Count boys and girls in the failed tutorial group
    for id, data in tutorial_group.items():
        gender = data['Gender']
        if gender in ['M', 'Male']:
            boys_count += 1
        elif gender in ['F', 'Female']:
            girls_count += 1
    
    # Store the counts for this tutorial group
    gender_counts_failed_tg[tgnum] = {'Boys': boys_count, 'Girls': girls_count}

sorted_failed_tgs = sorted(gender_counts_failed_tg.items(), key=lambda x: x[0])# Uses lambda function as temporary way to read x as the key without defining the function
band1 = 0
band2 = 0
band3 = 0
band4 = 0
numoftgfailed = 0
gcounth = 0 # Number of tutorial groups with more girls
bcounth = 0 # Number of turtorial groups with more girls
# Print the sorted results
print("Total gender counts for tutorial groups that failed the gender case (sorted by tutorial group number):")
for tg, counts in sorted_failed_tgs:
    numoftgfailed +=1
    if counts['Girls'] > counts['Boys']:
        gcounth += 1
    else:
        bcounth += 1
    
    if counts['Girls'] == 31:
        band1 += 1 
    elif counts['Girls'] == 32:
        band2 += 1
    elif counts['Girls'] == 33:
        band3 += 1
    elif counts['Girls'] == 34:
        band4 += 1
    print(f"Tutorial Group {tg}: Boys = {counts['Boys']}, Girls = {counts['Girls']}")

print(f"The total number of tutorial classes with failed groups is {numoftgfailed}.")

bar3fig, bar3ax = plt.subplots()

genderbalance = ['Classes with more girls', 'Classes with more boys']
counts = [gcounth, bcounth]
bar_labels = ['pink', 'blue']
bar_colors = ['tab:pink', 'tab:blue']

bars3 = bar3ax.bar(genderbalance, counts, label=bar_labels, color=bar_colors)

for bar in bars3:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval}', ha='center', va='bottom')

bar3ax.set_ylabel('Number of tutorial groups')
bar3ax.set_title('Distribution of failed tutorial groups')

plt.show()

Bar2fig, Bar2ax = plt.subplots()

Bands = ['31 girls', '32 girls', '33 girls', '34 girls']
counts = [band1, band2, band3, band4]
bar_labels = ['red', 'blue', 'green', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']

bars2= Bar2ax.bar(Bands, counts, label=bar_labels, color=bar_colors)

for bar in bars2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval}', ha='center', va='baseline')

Bar2ax.set_ylabel('Number of tutorial groups')
Bar2ax.set_title('Distribution of the number of girls in failed tutorial groups')

plt.show()

#Average SD Analysis

averageSD= sum(stdevs)/len(stdevs)
#print(averageSD)
#print(cgpas)
mean_of_means = sum(mean_cgpas_per_tutorial_group) / len(mean_cgpas_per_tutorial_group)
print(f"Mean of the Mean CGPAs across all tutorial groups: {mean_of_means:.2f}")
percentofAvSDovermeanmean= (averageSD/mean_of_means)*100  #Average SD over mean of the mean as a percentage.
print(f"{percentofAvSDovermeanmean:.2f}%")
fig, axes = plt.subplots()

# Set the x labels
axes.set_xlabel('Standard Deviation of 120 tutorial groups')
plt.violinplot(stdevs,vert = False,showmeans=True)
axes.get_yaxis().set_visible(False)
plt.show()

#Analyse the different number of different schools

Bar4fig, Bar4ax = plt.subplots()

Bands = numschool.keys()
counts = numschool.values()

bars4 = Bar4ax.bar(Bands, counts)

# Add text above bars
for bar in bars4:
    yval = bar.get_height()
    Bar4ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval}', ha='center', va='baseline')

# Adjust x-axis labels
Bar4ax.set_xticks(range(len(Bands)))  # Set the nunmber of x axis variable to the number of schools, otherwise there will be a warning
Bar4ax.set_xticklabels(Bands, rotation=45, ha='right')  # Rotate labels for better readability

Bar4ax.set_ylabel('Number of students')
Bar4ax.set_title('Distribution of the students across the different schools')

plt.tight_layout()  # Adjust layout to avoid clipping
plt.show()
