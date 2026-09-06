n = input("Please enter the highest number to look at to find the Pythagorean Triples: ")

n = int(n)

def find_Pythagorean(n : int):
    tuples = []
    #Went with a pretty simple function of for every number between 0 and the chosen number
    #and checks for every possible combination
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if (a ** 2 + b** 2 == c ** 2):
                    tuples.append((a, b, c))
                return tuples

print(find_Pythagorean(n))