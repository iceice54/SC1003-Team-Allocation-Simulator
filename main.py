from read_to_dict import read_to_dict
from team_allocator import sort_by_cgpa

student_data_dict = read_to_dict("records.csv")
print(sort_by_cgpa(student_data_dict['G-1']))
# print(student_data_dict['G-1'])