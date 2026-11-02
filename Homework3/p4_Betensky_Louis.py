import os

def ed_read(filename : str, fro: int = 0, to : int = -1) -> str:
    '''
    Function reads file passed to it.  Optionally can read parts of it depending on input
    Takes a mandatory input of the name of the file.  Then the user can input either just the beginning position, or the beginning and end characters to be read
    Outputs the message from the selected range, or the whole files content if no range is selected
    '''
    if fro > to and to != -1:
        print('From value needs to be less then the to value to properly search the file')
        raise ValueError('From value needs to be less then the to value to properly search the file')
    if fro < 0:
        print('Starting point must be a positive integer or 0.')
        raise ValueError('Starting point must be a positive integer or 0.')
    with open(filename, 'r', encoding="utf-8") as file:
        if to > len(file.read()):
            raise IndexError("There aren't that many characters in the file")
        else:
            if to != -1:
                file.seek(fro)
                message = file.read(to - fro)
            else:
                file.seek(fro)
                message = file.read()
    return message
    

def ed_find(filename : str, search_str : str) -> list[int]:
    '''
    Finds the location of a substring within a file, by pulling out the full content and finding the location
    Takes the filename and the substring being looked for as input
    Outputs EITHER the STARTING location(s) of the substring within the file in a list  , or an empty list if the substring couldn't be found.
    '''
    hits = []
    if search_str == "":
        raise ValueError("Can't find an empty string within a non-empty file... and if you are trying to search an empty file... why?")
    with open(filename, 'r', encoding="utf-8") as file:
        content = file.read()
        while not content == "":
            hit = content.find(search_str)
            if hit == -1:
                break
            else:
                try:
                    hits.append(hit + hits[-1] + len(search_str))
                except IndexError:
                    hits.append(hit)
                    
                content = content[hit + len(search_str):]
    return hits

def ed_replace(filename : str, search_str : str, replace_with : str, occurrence : int = -1) -> int:
    '''
    Replaces occurances of a substring within a file with another substring by searching the file for either all occurrences, or a singular specified occurrance of the substring being replaced
    Takes a filename, the substring being replaced, and the substring replacing it as input, as well as an optional occurrence variable for when lookinng to replace only a specific occurance
    Returns the amount of replacements that happened, and also actively changes the text in the file as a side effect
    '''
    hits = ed_find(filename, search_str)
    replacements = 0

    with open(filename, 'r', encoding="utf-8") as file:
        file.seek(0)
        message = file.read()
        
        if occurrence == -1:
            shift = 0
            for hit in hits:
                hit = hit + shift
                message = message[:hit] + replace_with + message[hit + len(search_str):]
                replacements += 1
                shift = (len(replace_with) - len(search_str)) * replacements
        elif occurrence >= 0 and occurrence < len(hits):
            message = message[:hits[occurrence]] + replace_with + message[hits[occurrence] + len(search_str):]
            replacements += 1
        else:
            print("Out of bounds, no replacements made")

    with open(filename, 'w', encoding="utf-8") as file:
        file.write(message)
    
    return replacements
            

def ed_append(filename : str, string : str) -> int:
    '''
    Adds a message to a file.  If the file doesn't exist, it will create one
    Takes the filename and the message being added to it as input
    Returns the length of the message added to the file, as well as adding text to the file as a side effect
    '''
    with open(filename, 'a', encoding="utf-8") as file:
        file.write(string)
        return len(string)


def main() -> None:
    '''
    Main function that walks the user through all functions, editing/creating a real file along the way
    No inputs are taken as this is the showcase that creates all the variables to be used by other functions, and as the assignment said this is non interactable no input is taken from user
    No outputs as well but it does print statements out for the user to read
    '''
    unit_tests()
    print("\n")
    fn = "file1.txt"
    new = "ABCDEF"
    try:
        print("To create or add to a file, we call ed_append with the filename as the first argument and the content to be added as the second: ed_append(filename, content_added)")
        print("We are going to use the file named: " + fn + " and the message: " + new)
        print("PLEASE NOTE: If you already have a file named " + fn + " at the location of this program file, it will not create a new file and instead just add the message " + new + "to it two times!")
        print("If you run this after running it once, or another students who used the same name, please delete the file1.txt file in the same directory as this program file")
        ed_append(fn, new) # this will create a new file
        ed_append(fn, new) # the file content is doubled
    except FileNotFoundError:
        print("Error creating or finding file when trying to add content")
    else:
        print("We also called the function twice for easier showing of functions later on.  This will make the file contents: ")
        try:
            print(ed_read(fn, 0))
        except FileNotFoundError:
            print("Unable to find file when showing content to user")

    print("\n")
    try:
        print("To read from a given position to another given position, call ed_read with the filename, first position you want the program to read from, and final position to stop reading at.  ed_read(fn, start, end)")
        start = 2
        end = 5
        print("For this non-interactive example, we have selected to start at 2, which is the first occurance of C, and 5, the first occurance of F")
        print(ed_read(fn, start, end))
        print("Alternatively, we can read the entire file from a given position by calling it with just the filename and the first position, meaning in this case we can go from the first C to the end of the file.")
        print(ed_read(fn, start))
    except FileNotFoundError:
        print("Error finding entered file when trying to read out the content")
    
    print("\n")
    try:
        print("To find the location of a given set of information, use ed_find, entering the filename and the string you are looking for.  ed_find(fn, string_searched)")
        print("For this example, we are going to look for the string DE, which appears 2 times")
        loc = "DE"
        print(ed_find(fn, loc))
        print("If the content isn't in the file, it will print an empty list")
        print("To show this, we are now going to try and find AF, which while the letters appear, are never next to each other in that order, and therefore won't be found")
        bad_loc = "AF"
        print(ed_find(fn, bad_loc))
    except FileNotFoundError:
        print("File not found when trying to find the location of info")
    except IndexError:
        print("Entered place is not within the file's content, try program again to test this")

    print("\n")
    try:
        print("We can even replace information in the file.  Just call ed_replace with the filename, the portion of string to be replaced, and the new string to insert in it's place.  ed_replace(fn, original_string, string_replacing_it)")
        print("Let's replace all A's with lowercase a's")
        og = "A"
        replaced = "a"
        print(ed_replace(fn, og, replaced))
        print(ed_read(fn, 0))
        ed_replace(fn, replaced, og)
        print("Alternatively, we can also replace a specific appearence of it, by inserting which occurance as an extra argument.  To do this we reset the file back to the original setting, and will only replace the second appearence")
        print(ed_replace(fn, og, replaced, 1))
        print(ed_read(fn, 0))
    except FileNotFoundError:
        print("File not found when trying to replace portions of string")


def unit_tests() -> None:
    '''
    Function to call the unit test functions
    no input or return
    '''
    test_ed_replace()
    test_ed_find()

def test_ed_replace() -> None:
    '''
    Handles unit tests for ed_replace
    As they are hardcoded in, no inputs
    As they display the results to the screen, no return
    '''
    test_file = "Test_Replace_Check.txt"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    ed_append(test_file, "First: Used to test ed_replace(): Replace Me")
    print(testif(ed_replace(test_file, "Replace Me", "Replaced!") == 1, "test_replace phrase", "ed_replace is working as intended and replaced the string correctly", "ed_replace failed to replace the string correctly and isn't working as intedned"))
    ed_append(test_file, "Second: Used to test ed_replace(): Replace Me")
    print(testif(ed_replace(test_file, "e", "E", 1) == 1, "test_replace single letter", "ed_replace is working as intended and replaced the string correctly", "ed_replace failed to replace the string correctly and isn't working as intedned"))
    print(testif(ed_replace(test_file, "e", "E") == 15, "test_replace all occurances", "ed_replace is working as intended and replaced all e's", "ed_replace failed to replace all e's and is working incorrectly"))

def test_ed_find() -> None:
    '''
    Handles unit tests for ed_find
    As they are hardcoded in, no inputs
    As they display the results to the screen, no return
    '''
    test_file = "Test_Find_Check.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    ed_append(test_file, "Used to test ed_find()")
    print(testif(ed_find(test_file, "test") == [8], "test_find", "ed_find is working as intended and found the string passed to it", "ed_find failed to find the string passed to it and isn't working as intedned"))
    print(testif(ed_find(test_file, "e") == [2, 9, 13], "test_find_mult", "ed_find is working as intended and found the string passed to it multiple times", "ed_find failed to find the string passed to it multiple times"))
    print(testif(ed_find(test_file, "Not in File") == [], "test_find_none", "ed_find is working as intended and didn't find any occurences of the string passed to it", "ed_find is not working as intended, and somehow found an occurance of the string passed to it"))



# testif module that was copy and pasted.  Not editing it because of this

def testif(b, testname, msgOK="", msgFailed=""):
    """Function used for testing. 
    param b: boolean, normally a tested condition: true if test passed, false otherwise
    param testname: the test name
    param msgOK: string to be printed if param b==True  ( test condition true)
    param msgFailed: string to be printed if param b==False
    returns b
    """
    if b:
        print("Success: "+ testname + "; " + msgOK)
    else:
        print("Failed: "+ testname + "; " + msgFailed)
    return b

main()

print("Louis Betensky, Z-Number: Z23542578")