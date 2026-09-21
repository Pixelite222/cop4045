import csv

friend_dict = {'alice': ('Alice Smith', ['maria']),
'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
'joe': ('Joseph Adams', ['maria', 'eve']),
'eve': ('Evelyn Cooper', ['joe']),
'david': ('David Benson', ['maria'])}

def add_user(sn : dict, username : str, fullname : str) -> bool:
    '''
    Takes dictionary, and adds a username as the key, and the user's full name as the initial value
    Returns bool that is true if the name was added, and false otherwise, as well as a print message confirming
    '''
    try:
        if not username in sn:
            sn[username] = fullname, []
            print("User added to the dictionary!")
            return True
        else:
            print("User already in the dictionary!")
            return False
    except TypeError:
        print("One of the values passed in was not of the expected variable type")
        raise

def add_friend(sn : dict, user1 : str, user2 : str) -> bool:
    '''
    Takes dictionary, checks if user1 and user2 are in it, and then makes them friends as per the dictionary's planned structure
    Returns Bool that is true if they were friended, and false otherwise, as well as printing a message saying if a fail occured
    Checks for type errors to make sure an incorrect value type didn't slip through the function.
    '''
    try:
        #Thought of any error possible but only could think of three
        #Check one: Making sure both are in the dictionary (though this may be redundent due to except KeyError)
        #Check two: Making sure they aren't already friends
        #Check three: Making sure we aren't trying to add themselves to their own friendlist
        if (user1 in sn and user2 in sn) and ((user1 not in sn[user2][1]) or (user2 not in sn[user1][1])) and (user1 != user2):
            sn[user1][1].append(user2)
            sn[user2][1].append(user1)
            return True
        else:
            print("One or both entered users: ", user1, " and ", user2, " were not successfully friended.  This is most likely due them already being friends, but could also be due to them being the same person, or one not existing in the dictionary.")
            return False
    except TypeError:
        print("One of the values passed in was not of the expected variable type!")
        raise
        

def get_friends(sn : dict, user1 : str, distance : int) -> list:
    '''
    Takes Dictionary, a user, and a positive int to represent distance.
    Checks the friends of user1, within however far a distance is entered, 
    returning a list with all of the friends in it.
    An exception is raised if the value of distance is negative, and if a keyError would happen, meaning a user isn't found, we return an empty list.
    Like previous functions in the program, we reraise type errors. 
    '''
    try:
        if distance <= 0:
            print("Sorry!  Distance can't be negative.  Please enter a positive integer value!")
            raise ValueError("Distance can't be negative.")
        friend_list = [user1]
        next_level = []
        while distance > 0:
            for user in friend_list:
                for friend in sn[user][1]:
                    if friend not in next_level:
                        next_level.append(friend)

            distance -= 1
            for user in next_level:
                if user not in friend_list:
                    friend_list.append(user)

        friend_list.pop(0)
        return friend_list
    except KeyError:
        print("User: ", user1, " not found in dictionary.")
        return []
    except TypeError:
        print("One of the values passed into the function is the incorrect type!")
        raise

def save_network(filename : str, sn : dict) -> None:
    '''
    Takes the name of a file and a dictionary.  Saves dictionary to a .csv
    I included a try except for FileNotFound as the assignment does call it out specifically, but noramly I believe this code would just make the file
    TypeError exception also included like functions before
    Included a custom raise to ensure the file has a .csv
    '''
    try:
        if ".csv" not in filename:
            print("Please try again, make sure to add .csv to the end of the filename text")
            raise ValueError("filename must include .csv")

        save_file = open(filename, "w", newline="")
        target = csv.writer(save_file)

        for key, value in sn.items():
            row = [key, value[0]]
            for name in value[1]:
                row.append(name)
            target.writerow(row)

        save_file.close()
        
    except TypeError:
        print("Either the file or the dictionary were entered as the wrong values, file should be a string ending in .csv, dictionary should be a dictionary object")
        raise
    except FileNotFoundError:
        print("Can't find file: ", filename, ".  Please try again.  Check spelling and make sure to end the file string with .csv")
        raise
    except AttributeError:
        print("Can't seem to read the dictionary, are you sure you passed it in correctly?")
        raise

def load_network(filename : str) -> dict:
    '''
    Recieves the name of the .csv file with stored network data on it, and loads it into a new dictionary.
    Expected to recieve a file formated like I do in save network, which is the first item being the un, second being fullname, and anything else on the row being the friends, in seperate cells
    Reraises FileNotFoundErrors when file isn't named, TypeErrors when value passed isn't correct
    Raises a ValueError if the string doesn't include .csv, as that is needed.  (Though this could have been fixed by this function, wanted to show the concept of raising as this assignment seems more focused on that)
    '''
    try:
        if ".csv" not in filename:
            print("File name does not include .csv")
            raise ValueError("Needs to be a file ending in .csv") 
           
        dict_file = (open(filename, "r"))
        target = csv.reader(dict_file)
        new_friend_dict = {}

        for row in target:
            list_of_friends = []
           
            for item in row:
                list_of_friends.append(item.strip())

            list_of_friends.pop(0)
            list_of_friends.pop(0)

            new_friend_dict[row[0]] = row[1], list_of_friends

        dict_file.close()

        return new_friend_dict

    except FileNotFoundError:
        print("File: ", filename, " not found.  Maybe check the spelling.  Don't forget to add .csv at the end!")
        raise
    except TypeError:
        print("Didn't recieve a string, try again and pass in the name of the file.  Don't forget to add .csv at the end!")
        raise

def main() -> None:
    '''Main function to test various cases for each function, commenting out ones that stop the program'''
    #add_user tests, ones that cause the program to break are commented out
    user_added = add_user(friend_dict, "louie", "Louis Betensky")
    print(user_added)
    user_added = add_user(friend_dict, "eve", "Evelyn Cooper")
    print(user_added)
    #user_added = add_user(None, "eve", "Evelyn Cooper")
    #print(user_added)

    #add_friend tests, like before program breaking lines are commented out
    user_friend = add_friend(friend_dict, "louie", "eve")
    print(user_friend)
    user_friend = add_friend(friend_dict, "eve", "eve")
    print(user_friend)
    user_friend = add_friend(friend_dict, "louis", "eve")
    print(user_friend)
    #user_friend = add_friend(None, "louie", "eve")
    #print(user_friend)

    #get_friends tests, same drill as before
    friend_list = get_friends(friend_dict, "alice", 1) 
    print(friend_list)
    friend_list = get_friends(friend_dict, "alice", 2)
    print(friend_list)
    friend_list = get_friends(friend_dict, "alice", 3) 
    print(friend_list)
    friend_list = get_friends(friend_dict, "idunno", 3)
    print(friend_list)
    #friend_list = get_friends(None, "alice", 1) 
    #print(friend_list)
    
    save_network("network.csv", friend_dict)
    print(friend_dict)

    new_friend_dict = load_network("network.csv")
    print(new_friend_dict)
    
    print("Louis Betensky")


main()