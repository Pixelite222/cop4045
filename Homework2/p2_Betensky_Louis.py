def math_comp():
    '''
    Checks all numbers between 1 and 10, returning only non repeating numbers where a^2 + b^2 = c^2 + d^2
    '''
    return [(a, b, c, d) for a in range(1, 11) for b in range(1, 11) for c in range(1, 11) for d in range(1, 11) if ((a**2 + b**2 == c**2 + d**2) and (len(set([a, b, c, d])) == 4))]

def word_comp(words = ['One', 'SEVEN', 'three', 'two', 'Ten']):
    '''
    return tuple of
    0 - lowercase word
    1 - length of word
    Returned list should only include words with length of 3 or less
    '''
    return [(word.lower(), len(word)) for word in words if len(word) <= 3]

def name_comp(names = ['Christopher Ashton Kutcher', 'Elizabeth Stamatina Fey']):
    '''change first middle last to first m. last'''
    return [(name.split()[0] + " " + name.split()[1][:1] + "." + " " + name.split()[2]) for name in names]

def anagram_comp(list1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"], list2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]):
    '''Checks if a word from list one is an anagram of a word from list two by checking each word in each list against each other, sorting them so the letters are in the same order'''
    return [(w1, w2) for w1 in list1 for w2 in list2 if sorted(w1.lower()) == sorted(w2.lower())]

def word_len_comp(words = ['one', 'two', 'three']):
    '''Dictionary comp this time, creating a dictionary that has a word as the key and the length of the word as the value'''
    return {element : len(element) for element in words}
#{(element : len(element)) for element in list}

def vowel_comp(text = "Hello World"):
    '''Another dictionary comp, counting how many times a value appears in a given string.'''
    vowel = ["a","e","i","o","u"]
    return {i : c for i, c in enumerate(text.lower()) if c in vowel}

part_a = math_comp()
part_b = word_comp()
part_c = name_comp()
part_d = anagram_comp()
part_e = word_len_comp()
part_f = vowel_comp()
print(part_a)
print(part_b)
print(part_c)
print(part_d)
print(part_e)
print(part_f)
print("Louis Betensky")