def read_file_create_dictionary(file_path):

    data = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines[1:]:
            values = line.strip().split(',')

            student_data = {
                'Tutorial Group': values[0],
                'Student ID': values[1],
                'Name': values[3],
                'School': values[2],
                'Gender': values[4],
                'CGPA': float(values[5])
            }

            data.append(student_data)

    # Dictionary to store the output
    output_dict = {}

    # creating the dictionary
    for record in data:
        tutorial_group = record['Tutorial Group']
        student_id = record['Student ID']

        # create dictionary for each tutorial group
        if tutorial_group not in output_dict:
            output_dict[tutorial_group] = {}

        # Add student data to the dictionary
        output_dict[tutorial_group][student_id] = {
            'Name': record['Name'],
            'School': record['School'],
            'Gender': record['Gender'],
            'CGPA': record['CGPA']
        }

    # Print the output
    import pprint

    pprint.pprint(output_dict)

    return output_dict


# read_file_create_dictionary(file_path="records.csv")
