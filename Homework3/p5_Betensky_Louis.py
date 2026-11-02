import turtle

# testif module  needed for multiple parts, not editing as it was copy and pasted from provided file

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

def draw_leaf_straight(rec_lvl : int, stem_len : int) -> None:
    '''
    Uses the globally defined t1 and creates a leaf drawing recursively with it
    Turtle moves forward part of the entereed stem len, and then starts drawing the left side of a branch until it reaches the end of the recursion level, then does so for the right side, after it moves a bit more and repeat as many times as the recursion level says
    Takes the recursion level and the length the stem should be as inputs,
    returns nothing as the function affects the turtle output on screen, only using the keywrod to show when to stop running the function
    '''
    if rec_lvl < 0:
        return
    t1.forward(stem_len / (rec_lvl + 1))
    stem_end = t1.pos()
    direct = t1.heading()
    t1.left(45)
    draw_leaf_straight(rec_lvl - 1, stem_len / 3)
    
    t1.goto(stem_end)
    t1.setheading(direct)

    t1.right(45)
    draw_leaf_straight(rec_lvl - 1, stem_len / 3)
    
    t1.goto(stem_end)
    t1.setheading(direct)

    draw_leaf_straight(rec_lvl - 1, stem_len - (stem_len/(rec_lvl + 1)))
    return


def draw_leaf_curved(rec_lvl : int, stem_len : int) -> None:
    '''
    Uses the globally defined t2 and creates a curved leaf drawing recursively with it
    Turtle moves forward part of the entereed stem len, and then starts drawing the left side of a branch until it reaches the end of the recursion level, then does so for the right side, after it moves a bit more and repeat as many times as the recursion level says
    To achieve the curved look, we save the direction the turtle looked at before drawing a branch, returning to that position at the end of a recursion, and then just turning it a bit before it continues
    Takes the recursion level and the length the stem should be as inputs,
    returns nothing as the function affects the turtle output on screen, only using the keywrod to show when to stop running the function
    '''
    if rec_lvl < 0:
        return
    t2.forward(stem_len / (rec_lvl + 1))
    stem_end = t2.pos()
    direct = t2.heading()
    
    t2.left(45)
    draw_leaf_curved(rec_lvl - 1, stem_len / 3)
        
    t2.goto(stem_end)
    t2.setheading(direct)
    
    t2.right(45)
    draw_leaf_curved(rec_lvl - 1, stem_len / 3)
    
    t2.goto(stem_end)
    t2.setheading(direct)
    t2.right(10)
    
    draw_leaf_curved(rec_lvl - 1, stem_len - (stem_len/(rec_lvl + 1)))
    return

'''
Following global mess here is just set up for the turtle that didn't fit in the recursive algo, including starting positions
'''
t1 = turtle.Turtle()
t1_start = t1.pos()
t1.speed(10)
t1.left(90)
turtle.delay(0)
draw_leaf_straight(6, 120)

t2 = turtle.Turtle()
t2.goto(t1_start + (100, 0))
t2.speed(10)
t2.left(90)
draw_leaf_curved(6, 120)


def strB(n : int, base : int = 10) -> str:
    '''
    Converts a decimal (base 10) number into the corresponding number in the desired base
    takes the decimal number, n, and the base value, base, as inputs
    outputs the corresponding number as a STRING
    '''
    new_num = ''
    if n > 0 and 2 <= base <= 26:
        if n > 0:
            rem = n % base

            if n//base != 0:
                new_num += strB(n // base, base)

            if rem >= 10:
                new_num += let_num_conv(rem)
            else:
                new_num += str(rem)
            
            return new_num
    elif n == 0:
        return str(n)
    else:
        if n < 0:
            print("Number passed to strB was negative")
            raise ValueError
        else:
            print("Base was passed an invalid value")
            raise ValueError

    
def let_num_conv(n : int) -> str:
    '''
    Helper Function for strB that converts numbers between 10 and 35 to letters A-Z, useful for bases greater then 10
    Takes the number needing conversion, n, as input
    Returns corresponding letter AS STRING
    '''
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters[n - 10]

def unit_tests_strB() -> None:
    '''
    Unit tests for the StrB function
    Tests various bases for value 200
    Recieves no input and returns no value
    prints results to screen
    '''
    print("\nstrB unit tests:")
    print(testif(strB(200) == "200", "Decimal Test", "StrB is correctly returning decimal", "StrB is incorrectly returning decimal"))
    print(testif(strB(200, 2) == "11001000", "Binary Test", "StrB is converting numbers to binary correctly", "StrB is incorrectly converting numbers to binary"))
    print(testif(strB(200, 8) == "310", "Octal Test", "StrB is converting numbers to octal correctly", "StrB is incorrectly converting numbers to octal"))
    print(testif(strB(200, 16) == "C8", "Hexidecimal Test", "StrB is converting numbers to hexidecimal correctly", "StrB is incorrectly converting numbers to hexadecimal"))

def display_strB() -> None:
    '''
    Result displays for the StrB function, so user can see the actual conversion
    Tests various bases for value 200
    Recieves no input and returns no value
    prints results to screen
    '''
    print("\nstrB result displays")
    print("200 in decimal is: " + strB(200))
    print("200 in binary is: " + strB(200, 2))
    print("200 in octal is: " + strB(200, 8))
    print("200 in hexidecimal is: " + strB(200, 16))

def strB_results() -> None:
    '''Simply here to easily call the two print functions'''
    unit_tests_strB()
    display_strB()

strB_results()

#n is total amount, k is amount you want to choose
#C(n, k) = C(n-1, k-1) + C(n-1, k)
repeat_dict = {}

def Cnk_m(n : int, k : int) -> int:
    '''
    Put in simple terms, calculates how many unique combinations can be made within a total set
    Recieves the total set size, n, and the size each unique combination should be, k
    Returns the amount of unique combination
    '''
    if n >= k:
        if n == k or k == 0:
            result = 1
            repeat_dict[(n, k)] = result
        elif (n, k) in repeat_dict.keys():
            result = repeat_dict[(n, k)]
        else:
            var1 = Cnk_m(n - 1, k - 1)
            repeat_dict[(n - 1, k - 1)] = var1
            var2 = Cnk_m(n - 1, k)
            repeat_dict[(n - 1, k)] = var2
            result = var1 + var2
    else:
        raise ValueError("Can't have any amount of combinations if the set of items being combined is larger then the total set")
    return result
    
def unit_tests_Cnk_m() -> None:
    '''
    Unit tests for the cnk_m function
    Tests various possible total values and combination sizes
    Recieves no input and returns no value
    prints results to screen
    '''
    print("\ncnk_m unit tests:")
    print(testif(Cnk_m(3, 2) == 3, "Basic Test", "Correctly finds the result for 2 item combos in a set of 3", "Fails to find correct amount of 2 item combos in a set of 3"))
    print(testif(Cnk_m(50, 2) == 1225, "2 in 50", "Correctly finds the result for 2 item combos in a set of 50", "Fails to find correct amount of 2 item combos in a set of 50"))
    print(testif(Cnk_m(50, 25) == 126410606437752, "25 in 50", "Correctly finds the result for 25 item combos in a set of 50", "Fails to find correct amount of 25 item combos in a set of 50"))
    print(testif(Cnk_m(10, 7) == 120, "7 in 10", "Correctly finds the result for 7 item combos in a set of 10", "Fails to find correct amount of 7 item combos in a set of 10"))

def display_Cnk_m() -> None:
    '''
    Display for the cnk_m function
    Shows results for the various unit tests for the user to see
    Recieves no input and returns no value
    prints results to screen
    '''    
    print("\ncnk_m result displays: ")
    print("Possible unique combinations of 2 items in a group of 3 is: " + str(Cnk_m(3, 2)))
    print("Possible unique combinations of 2 items in a group of 50 is: " + str(Cnk_m(50, 2)))
    print("Possible unique combinations of 25 items in a group of 50 is: " + str(Cnk_m(50, 25)))
    print("Possible unique combinations of 7 items in a group of 10 is: " + str(Cnk_m(10, 7)))

def Cnk_m_results() -> None:
    '''Simply here to easier call the display functions'''
    unit_tests_Cnk_m()
    display_Cnk_m()

Cnk_m_results()

def make_pairs(seq1 : list, seq2 : list, accum = None) -> list:
    '''
    Recursively makes pairs of numbers from two seperate lists using an accumulator
    Matches them by position i.e. the value in seq1 at position 0 is paired to position 0's value in seq 2, and goes through the list
    recieves two lists as input, as well as an accumulator for recursive building, initializing it as an empty list to start, then builds as the recursions execute
    outputs the final list of tuples for the pairs at the end, but each seperate output is one step in building the final one.
    '''
    if accum is None:
        accum = []
    if not seq1 or not seq2:
        return accum
    else:
        accum.append((seq1[0], seq2[0]))
        return make_pairs(seq1[1:], seq2[1:], accum)


def unit_tests_pairs() -> None:
    '''
    Unit tests for the make_pairs function
    Tests various edge cases and odd possibilities to ensure the function runs as intended
    Recieves no input and returns no value
    prints results to screen
    '''

    print("\nmake_pairs unit tests:")
    print(testif(make_pairs([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) == [(1, 6), (2, 7), (3, 8), (4, 9), (5, 10)], "Basic", "Correctly making pairs when both lists are the same size", "Incorrectly making pairs when both lists are the same length"))
    print(testif(make_pairs([17, 18], [19, 20, 21]) == [(17, 19), (18, 20)], "Mismatched length", "Correctly making pairs when lists are different sizes", "Incorrectly making pairs when lists are different sizes"))
    print(testif(make_pairs([], []) == [], "2 Empty Sets", "Correctly returns an empty list when both lists are empty", "Incorrectly making pairs when both lists are empty"))
    print(testif(make_pairs([4, 5, 6], []) == [], "Right Side Empty", "Correctly returns an empty list when the second list is empty", "Incorrectly making pairs when one list is empty"))
    print(testif(make_pairs([], [15, 25, 26, 50]) == [], "Left Side Empty", "Correctly returns an empty list when the first list is empty", "Incorrectly making pairs when one list is empty"))

def display_pairs() -> None:
    '''
    Display function for the make_pairs function
    Displays the results of the cases used in the unit_test function for the user to see
    Recieves no input and returns no value
    prints results to screen
    '''

    print("\nmake_pairs result displays: ")
    print("List 1: [1, 2, 3, 4, 5], List 2: [6, 7, 8, 9, 10], pairs: " + str(make_pairs([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])))
    print("List 1: [17, 18], List 2: [19, 20, 21], pairs: " + str(make_pairs([17, 18], [19, 20, 21])))
    print("List 1: [], List 2: [], pairs: " + str(make_pairs([], [])))
    print("List 1: [4, 5, 6], List 2: [], pairs: " + str(make_pairs([4, 5, 6], [])))
    print("List 1: [], List 2: [15, 25, 26, 50], pairs: " + str(make_pairs([], [15, 25, 26, 50])))

def pairs_results() -> None:
    '''As the previous 2, here to make calling the functions easier'''
    unit_tests_pairs()
    display_pairs()

pairs_results()
turtle.done()

print("Louis Betensky, Z-Number: Z23542578")