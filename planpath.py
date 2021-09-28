import argparse as apimport itertoolsimport reimport platform######## RUNNING THE CODE #####################################################   You can run this code from terminal by executing the following command#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag>#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA################################################################################################# YOUR CODE GOES HERE ########################################class Node():    counter = itertools.count()    def __init__(self, parent=None, position=None):        self.parent = parent        self.position = position        self.g = 0        self.h = 0        self.f = 0        self.id = "N" + str(next(self.counter))        self.move = ""        self.expansion_order = 0    # def __str__(self):    #     return str(self.id)    def __str__(self):        if self.move == "S":            return "S"        else:            path = self.get_path()            return path[2:]    def __eq__(self, other):        return self.position == other.position    def get_path(self):        path = []        temp_node = self        while temp_node is not None:            path.append(temp_node.move)            temp_node = temp_node.parent        return "-".join(path[::-1])def getDirection(new_position):    # (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)    if new_position == (0, -1):        return "L"    elif new_position == (0, 1):        return "R"    elif new_position == (-1, 0):        return "UP"    elif new_position == (1, 0):        return "D"    elif new_position == (-1, -1):        return "LU"    elif new_position == (-1, 1):        return "RU"    elif new_position == (1, -1):        return "LD"    elif new_position == (1, 1):        return "RD"def get_current_map_position(cleaned_map, current):    map_str = []    for tile_row in cleaned_map:        tile_row_str = [str(tile) for tile in tile_row]        map_str.append(tile_row_str)    map_str[current.position[0]][current.position[1]] = "*"    return "".join(["".join(tile_str_row) + "\n" for tile_str_row in map_str]) + "\n"def get_final_string(cleaned_map, current_node):    map = []    move_list = []    path = []    g_score = []    temp = ""    current = current_node    while current is not None:        map.append(get_current_map_position(cleaned_map, current))        move_list.append(current.move)        g_score.append(current.g)        current = current.parent    for move, g in zip(move_list[::-1], g_score[::-1]):        if move == "S":            path.append(move + " " + str(g) + "\n")            temp += move        else:            temp += "-" + move            path.append(temp + " " + str(g) + "\n")    final = [i + j + "\n" for i, j in zip(map[::-1], path)]    return final  # Return reversed pathdef get_all_node_info(node):    return get_node_path_and_move(node) + " " + str(node.expansion_order) + " " + str(node.g) + " " + str(        round(node.h, 2)) + " " + str(round(node.f, 2))def get_node_path_and_move(node):    move = node.move    if move == "S":        move = ""    else:        move = " " + move    return node.id + ": " + str(node) + movedef print_console(current_node, open_list, closed_list, children):    print(get_all_node_info(current_node))    print("Children: {" + ", ".join([get_node_path_and_move(node) for node in children]) + "}")    print("OPEN: {" + ", ".join([get_all_node_info(node) for node in open_list]) + "}")    print("CLOSED: {" + ", ".join([get_all_node_info(node) for node in closed_list]) + "}")    print("\n")def graphsearch(map, flag):    dimension = map.pop(0)[0]    cleaned_map = []    mountain_tiles = []    start = (0, 0)    # used to clean the map and find start and end tile    for i, rows in enumerate(map):        rows.pop()        for j, tile in enumerate(rows):            if tile == "S":                start = (i, j)            elif tile == "G":                end = (i, j)            elif tile == "X":                mountain_tiles.append((i, j))        cleaned_map.append(rows)    # start node    start_node = Node(None, start)    start_node.g = start_node.h = start_node.f = 0    start_node.move = "S"    end_node = Node(None, end)    end_node.g = end_node.h = end_node.f = 0    end_node.move = "G"    # Initialize open and closed list    open_list = []    closed_list = []    expansion = 1    # Adding starting node to open list    open_list.append(start_node)    # Loop until you find the goal node or no node left to travel too    while len(open_list) > 0:        # get current node        current_node = open_list[0]        current_index = 0        for index, item in enumerate(open_list):            if item.f < current_node.f:                current_node = item                current_index = index        # Pop current off open list, add to closed list        # Update expansion order also        current_node.expansion_order = expansion        open_list.pop(current_index)        closed_list.append(current_node)        # Check for goal state        if current_node == end_node:            return get_final_string(cleaned_map, current_node)        # Generate children        children = []        children_to_remove = []        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares            # Get node position            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])            # Make sure within range            if node_position[0] > (len(cleaned_map) - 1) or node_position[0] < 0 or node_position[1] > (                    len(cleaned_map[len(cleaned_map) - 1]) - 1) or node_position[1] < 0:                continue            # Make sure walkable terrain            if new_position in [(0, 1), (1, 0), (-1, 0), (0, -1)]:  # 4 direction                if node_position in mountain_tiles:                    children_to_remove.append(node_position)                    if new_position == (0, 1):                        # check for edge conditions                        children_to_remove.append((node_position[0] + 1, node_position[1]))                        children_to_remove.append((node_position[0] - 1, node_position[1]))                    elif new_position == (1, 0):                        children_to_remove.append((node_position[0], node_position[1] - 1))                        children_to_remove.append((node_position[0], node_position[1] + 1))                    elif new_position == (-1, 0):                        children_to_remove.append((node_position[0], node_position[1] + 1))                        children_to_remove.append((node_position[0], node_position[1] - 1))                    elif new_position == (0, -1):                        children_to_remove.append((node_position[0] + 1, node_position[1]))                        children_to_remove.append((node_position[0] - 1, node_position[1]))            elif new_position in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Diagonals                if node_position in mountain_tiles:                    continue            direction = getDirection(new_position)            new_node = Node(current_node, node_position)            new_node.move = direction            if len(children_to_remove) > 0:                if (new_node.position[0], new_node.position[1]) not in children_to_remove:                    children.append(new_node)                    continue            else:                children.append(new_node)        for child in children:            # Create the f, g, and h values            if child.move in ["L", "R", "UP", "D"]:                child.g = current_node.g + 2            elif child.move in ["LU", "RU", "LD", "RD"]:                child.g = current_node.g + 1            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (                    (child.position[1] - end_node.position[1]) ** 2)            child.f = child.g + child.h            open_list.append(child)            # Child is on the closed list            for closed_child in closed_list:                if child == closed_child:                    open_list.remove(child)            # Child is already in the open list            for open_node in open_list:                if child == open_node and child.g > open_node.g:                    open_list.remove(child)        if flag > 0:            flag -= 1            print_console(current_node, open_list, closed_list, children)        expansion += 1    return "NO-PATH"def read_from_file(file_name):    # You can change the file reading function to suit the way    # you want to parse the file    file_handle = open(file_name)    map = []    rows = file_handle.readlines()    for i, item in enumerate(rows):        map.append(list(item))    return map########################################################################################## DO NOT CHANGE ANYTHING BELOW #####################################################################################################################def write_to_file(file_name, solution):    file_handle = open(file_name, 'w')    for item in solution:        file_handle.write(item)def main():    # create a parser object    parser = ap.ArgumentParser()    # specify what arguments will be coming from the terminal/commandline    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)    # get all the arguments    arguments = parser.parse_args()    ##############################################################################    # these print statements are here to check if the arguments are correct.    #    print("The input_file_name is " + arguments.input_file_name)    #    print("The output_file_name is " + arguments.output_file_name)    #    print("The flag is " + str(arguments.flag))    #    print("The procedure_name is " + arguments.procedure_name)    ##############################################################################    # Extract the required arguments    operating_system = platform.system()    if operating_system == "Windows":        input_file_name = arguments.input_file_name        input_tokens = input_file_name.split("\\")        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):            print("Error: input path should be of the format INPUT\input#.txt")            return -1        output_file_name = arguments.output_file_name        output_tokens = output_file_name.split("\\")        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):            print("Error: output path should be of the format OUTPUT\output#.txt")            return -1    else:        input_file_name = arguments.input_file_name        input_tokens = input_file_name.split("/")        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):            print("Error: input path should be of the format INPUT/input#.txt")            return -1        output_file_name = arguments.output_file_name        output_tokens = output_file_name.split("/")        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):            print("Error: output path should be of the format OUTPUT/output#.txt")            return -1    flag = arguments.flag    # procedure_name = arguments.procedure_name    try:        map = read_from_file(input_file_name)  # get the map    except FileNotFoundError:        print("input file is not present")        return -1    # print(map)    solution_string = ""  # contains solution    solution_string = graphsearch(map, flag)    write_flag = 1    # call function write to file only in case we have a solution    if write_flag == 1:        write_to_file(output_file_name, solution_string)if __name__ == "__main__":    main()