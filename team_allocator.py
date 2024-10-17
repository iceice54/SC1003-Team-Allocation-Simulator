def allocate_teams(tutorial_group):
    g1,g2,g3,g4,g5,g6,g7,g8,g9,g10 = [],[],[],[],[],[],[],[],[],[]

    

        
    # make sorted list with gpa and id

def sort_by_cgpa(tutorial_group):
    sorted_list = []
    for id, data in tutorial_group.items():
        data_list = [id, data['CGPA'], data['Gender'], data['Name'], data['School']]
        cgpa = data['CGPA']
        #first entry
        if sorted_list == []:
            sorted_list.append(data_list)
            continue
        
        #loop through each existing entry to find where to insert current entry based on cgpa
        index = 0
        for entry in sorted_list: 
            entry_cgpa = entry[1]
            if cgpa > entry_cgpa:
                index += 1
                #cgpa higher than any other cgpa, so append to end of list
                if index == len(sorted_list):
                    sorted_list.append(data_list)
                    break
                continue
            elif cgpa <= entry_cgpa:
                sorted_list.insert(index, data_list)
                break


    return sorted_list