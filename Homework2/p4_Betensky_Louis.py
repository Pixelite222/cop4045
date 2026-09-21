import csv

#Top casts don't have a header, the others do

def create_title_list(reader : csv.reader) -> list:
    '''
    Creates a list of titles of movies from the relavent reader passed in.
    Returns the list to where it was called.
    '''
    try:
        title_list = []
        for row in reader:
            if row[0].isdigit():
                title_list.append(row[1])

        return title_list

    except TypeError:
        print("Type Error. The reader input was not passed in correctly, check if the file was passed instead.")
        raise

def get_actors(row) -> list:
    '''
    Takes in a row from the cast file and sorts it into a list of actors.
    Due to how the file is formatted, we pop the first three lines to delete the title, year, and director.
    returns list.
    '''
    actors = []

    for name in row:
        actors.append(name)
    actors.pop(0)
    actors.pop(0)
    actors.pop(0)

    return actors

def rank_sorting(actor_dict: dict) -> list:
    '''
    Takes a dictionary of actors, and the values given to them (total gross or collaberations with a given director) and sorts them highest to lowest.
    Returns list of tuples with the actor and values, to be properly reformatted by the original function.
    '''
    dict_list = []
    for actor in actor_dict:
        dict_list.append((actor_dict[actor], actor))

    dict_list.sort(reverse=True)
    return dict_list

def cutoff_handleing(list, cutoff) -> None:
    '''
    This simply handles cutoffs if entered.
    It recieves a list and a cutoff value, and prints the list up to the given cutoff.
    If there was no cutoff value, it prints the entire list.
    If the cutoff is too high, it raises a ValueError and lets the user know.    
    '''
    if cutoff > len(list):
        print("Your desired cutoff is too big!  The list is smaller then that.  Try again with a smaller number.")
        raise ValueError("Cutoff is too high.")
    if cutoff > 0:
        i = 0
        while i <= cutoff - 1:
            print(list[i])
            i += 1
    else:
        print(list)

def display_top_collaborations(cast_file : str, top_rated_file : str, cutoff = -1) -> None:
    '''
    Takes two files, one containing the cast data, the other containing the top rated movies.  Also takes an optional cutoff value.
    Eventually prints a list of the top collaborations between actors in the top rated movies and the directors that directed them.  List is sorted from highest to lowest.
    Throws exceptions for FileNotFound and Type Errors.
    '''
    try:    
        ratings = open(top_rated_file, 'r', encoding = 'utf-8')
        rate_read = csv.reader(ratings)

        temp_dict = {}
        
        title_list = create_title_list(rate_read)

        ratings.close()


        cast = open(cast_file, 'r', encoding = 'utf-8')
        cast_read = csv.reader(cast)

        for row in cast_read:
            if row[0] in title_list:
                actors = get_actors(row)

                for actor in actors:
                    try:
                        temp_dict[row[2], actor] += 1
                    except KeyError:
                        temp_dict[row[2], actor] = 1

        #dict_list = []
        #for key in temp_dict:
        #    dict_list.append((temp_dict[key], key[0], key[1]))

        #dict_list.sort(reverse=True)

        dict_list = rank_sorting(temp_dict)

        final_list = []
        for tup in dict_list:
            final_list.append((tup[1][0], tup[1][1], tup[0]))

        cutoff_handleing(final_list, cutoff)

        cast.close()
    except FileNotFoundError:
        print("One of or both of the files were not found!!!  Please try again after checking file names.")
        raise FileNotFoundError("One of the files weren't found.  Please check your file names and try again.")
    except TypeError:
        print("Type Error.  One of the inputs did not match the needed type!")
        raise TypeError("Type Error.  Please change the types of the variables being passed in and try agin")

def display_top_actors(cast_file : str, gross_file : str, cutoff = -1) -> None:
    '''
    Function takes two files, one containing the cast data, the other taking the gross money made of the top grossing movies.  Also takes an optional cutoff value.
    Creates and prints out a dictionary of the top grossing actors, or more so actors whos movies grossed the most alltogether.  List is sorted from highest to lowest.
    Throws exceptions for FileNotFound and Type Errors.
    '''
    try:

        gross = open(gross_file, 'r', encoding = 'utf-8')
        gross_read = csv.reader(gross)

        temp_dict = {}
        
        title_and_gross_dict = {}
        for row in gross_read:
            if row[0].isdigit():
                title_and_gross_dict[row[1]] = row[3]

        gross.close()

        cast = open(cast_file, 'r', encoding = 'utf-8')
        cast_read = csv.reader(cast)

        for row in cast_read:
            if row[0] in title_and_gross_dict:
                actors = get_actors(row)

                for actor in actors:
                    try:
                        temp_dict[actor] += int(title_and_gross_dict[row[0]])
                    except KeyError:
                        temp_dict[actor] = int(title_and_gross_dict[row[0]])

        cast.close()

        dict_list = rank_sorting(temp_dict)
        
        final_list = []
        for tup in dict_list:
            final_list.append((tup[1], tup[0]))

        cutoff_handleing(final_list, cutoff)

    except FileNotFoundError:
        print("One of or both of the files were not found!!!  Please try again after checking file names.")
        raise FileNotFoundError("One of the files weren't found.  Please check your file names and try again.")
    except TypeError:
        print("Type Error.  One of the inputs did not match the needed type!")
        raise TypeError("Type Error.  Please change the types of the variables being passed in and try agin")

        
def main() -> None:
    '''
    Main function.  Simply runs the programs.  Added my name to show up in output like other assignments
    '''
    #No cutoff tests
    #print("Top collaborations:")
    #display_top_collaborations("imdb-top-casts.csv", "imdb-top-rated.csv")

    #print("Top actors:")
    #display_top_actors("imdb-top-casts.csv", "imdb-top-grossing.csv")

    #cutoff tests
    print("Top collaborations:")
    display_top_collaborations("imdb-top-casts.csv", "imdb-top-rated.csv", 10)

    print("Top actors:")
    display_top_actors("imdb-top-casts.csv", "imdb-top-grossing.csv", 10)

    print("Louis Betensky")
main()