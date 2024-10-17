# get the cgpa from the output_dict
#创建一个空字典用来储存cgpa
cgpa_list_dict={}

#把原字典里的key和value储存用来之后loop，否则loop的只是value
output_items = output_dict.items()

for tutorial_group ,students in output_items:
    students = output_dict[tutorial_group]
    students_items = students.items()
    cgpa_list = []
    for student_id , student_info in students_items:
        student_info = students[student_id]
        cgpa_list.append(student_info['CGPA'])
    cgpa_list_dict[tutorial_group] = cgpa_list

#现在有了一个字典，其中有50组，每组的key是tutorial_group，value是一个list，里面有50个gpa

#seperate the cgpa into 3 different dictionaries
cgpah_list_dict={}
cgpam_list_dict={}
cgpal_list_dict={}
for tutorial_group in cgpa_list_dict:
    cgpa_lists = cgpa_list_dict[tutorial_group]
    cgpa_lists.sort()

    cgpal_list = cgpa_lists[:20]
    cgpam_list = cgpa_lists[20:40]
    cgpah_list = cgpa_lists[40:]

    cgpah_list_dict[tutorial_group] = cgpah_list
    cgpam_list_dict[tutorial_group] = cgpam_list
    cgpal_list_dict[tutorial_group] = cgpal_list
#现在有3个dictionaries，分别是高中低，每个里面有50组，key是tutorial_group，value是一个list，里面有10个或者20个gpa
#here we get 3 dictionaries ,keys are tutorial_group,values are lists ,including 10 or 20 cgpas

# I'm not sure if we need to put the studentid into a list or just cgpa is enough ,here is the dictionies of studentid lists
student_idh_dict={}
student_idm_dict={}
student_idl_dict={}
student_idh_list=[]
student_idm_list=[]
student_idl_list=[]
for tutorial_group ,students in output_items:
    students = output_dict[tutorial_group]
    students_items=students.items()
    for student_id , student_info in students_items:
        student_info = students[student_id]
        if student_info['CGPA'] in cgpah_list_dict[tutorial_group]:
            student_idh_list.append(student_id)
        elif student_info['CGPA'] in cgpam_list_dict[tutorial_group]:
            student_idm_list.append(student_id)
        else :
            student_idl_list.append(student_id)
    student_idh_dict[tutorial_group]=student_idh_dict
    student_idm_dict[tutorial_group]=student_idm_dict
    student_idl_dict[tutorial_group]=student_idl_dict
#here we get 3 dictionaries ,the keys are tutorial_group,values are lists,which contains 20 or 10 cgaps

