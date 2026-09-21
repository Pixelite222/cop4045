def line_number(read_file : str, write_file : str) -> None:
    '''
    Opens and reads a file, then writes to a different one, a copy of the first, but numbering the lines each line is written on
    Throws raised exceptions for FileNotFoundErrors when trying to read, and type errors when the files don't have strings passed in their place
    '''
    try:
        main_file = open(read_file, "r") 
        target = open(write_file, "w")
    
        i = 1
        for line in  main_file:
            numbered_line = str(i) + '. '
            numbered_line += line
            print(numbered_line, file = target, end="")
            i += 1

        main_file.close()
        target.close()

    except FileNotFoundError:
        print("Error!!! File: ", read_file, "doesn't exist or wasn't found.")
        raise
    except TypeError:
        print("Error!!! One of the two files passed weren't strings, and couldn't be read as a result")
        raise    

    print("line_number complete")
    
#0 - line number
#1 - function name
#2 - member variables as a string
#3 - Function's code (Header and body) with empty lines and comments removed
def parse_functions(file : str) -> tuple:
    '''
    Creates a tuple of tupples, which hold the line number a function is on, the functions name, it's member variables, and the entirity of the function.
    It then sorts it in alphabetical order through the use of reordering the tupple into a new list, using sort(), and finally reordering the tupples back to the way wanted in the assignment
    Exceptions are again thrown for FileNotFound and Type Errors like above
    '''
    try:
        found_file = open(file, "r")

        func_line = 0
        func_name = ""
        func_var = ""
        func_code = ""
        func_arr = []

        i = 1
        func_check = False
        for line in found_file:
            if line.strip().startswith("def "): 
                if func_line != 0:
                    func_tup = func_line, func_name, func_var, func_code #tuple assigning
                    func_arr.append(func_tup)

                func_line = i
                func_name = line[line.find('def ') + 4 : line.find('(')]
                func_var = line[line.find('(') + 1:line.find(')')]
                func_check = True
                func_code = line.strip()
            else:
                if func_check:
                    if line.strip() != "" and not line.strip().startswith("#"): 
                        if not (line.startswith(" ") or line.startswith("\t")):
                            func_check = False
                        else:
                            if "#" in line.strip():
                                func_code += " " + (line[:line.find("#")]).strip() #added a space between lines to try and make it a bit more readable, hopefully won't mark me off for including it.
                            else:
                                func_code += " " + line.strip()
                        



            i += 1

        func_tup = func_line, func_name, func_var, func_code
        if not func_tup in func_arr:
            func_arr.append(func_tup)


        found_file.close()

        func_list = []
        for func in func_arr:
            func_list.append((func[1], func[0], func[2], func[3]))

        func_list.sort()

        final_list = []
        for func in func_list:
            final_list.append((func[1], func[0], func[2], func[3]))
        

        return tuple(final_list)

    except FileNotFoundError:
        print("Error!!! File: ", file, " doesn't exist or isn't found!")
        raise
    except TypeError:
        print("Error!!! File: ", file, " wasn't passed in as a string and can't be read")
        raise


def main() -> None:
    '''
    Simply calls the functions to test them.  Because of this I haven't added exceptions.
    '''
    line_number("p1_Betensky_Louis.py", "copy of p1_Betensky_Louis.py.txt")
    func_tup = parse_functions("p1_Betensky_Louis.py")

    #included for ease of reading, but commenting it out in favor of the one seemingly more in line with the assignment's example
    #for tup in func_tup:
    #    print(tup)
    
    print (func_tup)

    print("Louis Betensky")


main()