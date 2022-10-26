

git_path = '/Users/benjaminmoran/Documents/GitHub/RenText'
file = 'tcp_ids_and_dates.txt'
file_path = f'{git_path}/{file}'

with open(file_path, 'r') as f:
    contents = f.read()
    row = str(contents, sep= '', end='\n')
    row    # Trying to 
    # - identify a space and replace it with a comma
    # - identify a "row" (end of line)
    # - repeat process for each new line


        # string = char
        # new_line = string.replace(' ', ',')
        # print("New line: ", new_line, end='', flush=True)

# with open(f'{git_path}/tcp_ids_and_dates.csv', 'w') as n:
#     n.write()

    
