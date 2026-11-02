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
    
print("Louis Betensky, Z-Number: Z23542578")