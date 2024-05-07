def print_communication_cost(table_str):
    # Split the table into lines
    lines = table_str.split('\n')

    # Initialize a list to hold the titles
    filtered_lines = lines[0:4]

    # Search for rows that contain the keyword 'AllReduce'
    for line in lines[4:]:
        if 'all_reduce' in line:
            filtered_lines.append(line)

    for line in filtered_lines:
        print(line)
