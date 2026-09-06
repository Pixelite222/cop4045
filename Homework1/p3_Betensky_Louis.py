full_string = input("Please enter string here: ") #"abcdefbcdgh"
l = int(input("Please enter length of substring here: "))
half = len(full_string) / 2

def find_dup_str(s : str , n : int):
    for letter in range(len(s) - (n-1)): #Loop through entire word
        end = letter + n #correctly set an end point in relation to letter
        substring = s[letter:end] #string slice the target
        remainder = s[end:] #then look at the remainder, as anything before it is either already seen or is currently in substring
        
        for new_let in range(len(remainder)): #now loop through remainder of word
            new_let *= -1 #backwards
            new_end = new_let - n #backwords end point (or start)
            if substring == remainder[new_end:new_let]: #if the sub and current observered part of remaindrer match
                return substring #return the dup
    
dup_string = find_dup_str(full_string, l)
print("The first duplicate string of length " + str(l) + " found was: " + dup_string)

def find_max_dup(s):
    end = len(s) // 2 #set the first end point to the halfway point, as can't dup a substring over half the size
    curr_large_sub = ""
    for start_letter in range(len(s) - (end-1)): #loop start over string
        for end_letter in range(len(s) - (end - 1)): #and end over string for each start letter
            substring = s[start_letter:start_letter + end_letter] #set substring to the correct positions (end is start letter plus end)
            remainder = s[start_letter + end_letter:] #set remainder correctly
            for r_let in range(len(remainder)): #loop the remainder word
                check = remainder[r_let:(r_let + len(substring))] #and a portion of it equal to the size of the substring
                if substring == check: #and if match
                    if len(substring) > len(curr_large_sub): #ensure we aren't overwriting with a smaller one
                        curr_large_sub = substring #set the current largest
        
    return curr_large_sub #return
        

max_dup = find_max_dup(full_string)
print("The max dup string is: " + max_dup)
            