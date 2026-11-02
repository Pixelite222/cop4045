class NVector(object):
    '''
    Class representing a vector of variable dimensions, defined by how many variables
    are passed into the initialization calls.
    Quick note, for the following functions docstrings, I will mostly leave out the self parameter as it is needed for most of them and is simply assigning the instance to the func for it's init values
    '''
    
    
    def __init__(self, *values : int) -> None:
        '''
        Constructor function that take a list or set of values that are passed in when the class is initialized (also takes self as is necissary).
        The values are then placed into a list localized in the class.
        these values will later be used by other functions, but as they are edited directly, the function has nothing to return
        '''
        self.value_list = []
        if len(values) == 1:
            for item in values[0]:
                self.value_list.append(item)
        else:
            for item in values:
                self.value_list.append(item)
        #print(self.value_list) #For debug/checking, don't keep in final
        
    def __len__(self) -> int:
        '''
        Function that simply returns the length of the vector.
        It only takes the self as input as it targets the value list stored on self
        Returns length of list
        '''
        return len(self.value_list)
    
    def __getitem__(self, index : int) -> int:
        '''
        Function to just allow indexing through the list to work as intended
        Reiceves self as needed for variable access, and an index
        Returns the item in the position targeted by the index value
        '''
        try:
            return self.value_list[index]
        except IndexError:
            print("Entered an index out of scope of the current list.  List has " + str(len(self)) + " values, so the minimum index should be " + str(-1 * len(self)) + " and the maximum should be " + str(len(self) - 1))
            raise

    def __setitem__(self, index : int, value) -> None:
        '''
        Function to edit values within the collected list.
        Takes the index needing to be edited, and the value to replace the old one with
        Doesn't output anything, as it just sets the item.  Should call the getter if you want to see the results'
        '''
        try:
            self.value_list[index] = value
        except IndexError:
            print("Entered an index out of scope of the current list.  List has " + str(len(self)) + " values, so the minimum index should be " + str(-1 * len(self)) + " and the maximum should be " + str(len(self) - 1))
            raise
    
    def __str__(self) -> str:
        '''
        Str function to control what prints when trying to print a NVector
        '''
        
        return "NVector, Currently holding a vector with dimensions of: {}\nThe values on each dimension are: {}".format(str(len(self)), str(self.value_list))
        
    def __eq__(self, other : object) -> bool:
        '''
        Function to determine if this instance of a class is equivalent to that of another.
        Takes the necissary self, as well as the other class as input, comparing the values of their lists
        Outputs a boolian telling us if they are equal to each other.
        Includes a check to ensure they are the same dimensionality, before checking the values individually.
        '''
        result : bool
        if isinstance(other, NVector):
            if len(self) == len(other):
                if len(self) != 0:
                    for i in range(self.__len__()):
                        if self[i] == other[i]:
                            result = True
                        else:
                            result = False
                            break
                else:
                    return True
            else:
                result = False
            return result
        else:
            print("Comparing objects of type {} and {}.  Please use two NVectors for a possibility of truth".format(type(self), type(other)))
            return False

    
    def __ne__(self, other : object) -> bool:
        '''
        Function to determine if this instance of a class is not equivalent to that of another.
        Takes the necissary self, as well as the other class as input, comparing the values of their lists
        Outputs a boolian telling us if they are not equal to each other.
        Includes a check to see if they are the same dimensionality, before checking the values individually.
        '''
        result : bool
        if isinstance(other, NVector):
            if len(self) == len(other):
                if len(self) != 0:
                    for i in range(self.__len__()):
                        if self[i] == other[i]:
                            result = False
                        else:
                            result = True
                            break
                else:
                    return False
            else:
                result = True
            return result 
        else:
            print("Comparing objects of type {} and {}.  Please use two NVectors for a possibility of False".format(type(self), type(other)))
            return True   
    
    def __add__(self, other) -> object:
        '''
        Function to control adding between objects of this class and other items
        Specifically with items of this class, or with ints
        If the items share the class but vary in sizes, I have them add what they can and copy over the rest, as opposed to raising an error like ValueError that gives no result
        Recieves itself and the other variable as input
        Returns a new NVector with the resulting values
        '''
        new_vec_list = []
        if isinstance(other, NVector):
            if len(self) <= len(other):
                for i in range(len(self)):
                    new_vec_list.append(self[i] + other[i])
                new_vec_list = new_vec_list + other[len(self):]
            else:
                for i in range(len(other)):
                    new_vec_list.append(self[i] + other[i])
                new_vec_list = new_vec_list + self[len(other):]
        
        elif isinstance(other, int) or isinstance(other, float):
            for item in self.value_list:
                new_vec_list.append(item + other)
        
        else:
            raise TypeError("Cannot add objects of type {} and {}".format(type(self), type(other)))
        
        return NVector(new_vec_list)
                
        
    def __radd__(self, other) -> object:
        '''
        Function to control adding between objects of this class and other items, but when this item is not in the first position
        Compatable with others of this class, and ints
        Recieves itself and another variable as input
        Returns the returned result of __add__ as we simply just pass the inputs into that function
        '''
        return self.__add__(other)
    
    
    def __mul__(self, other) -> float:
        '''
        Function to control multiplication of NVectors of this class and other items
        Compatible with other NVectors, and ints
        Recieves itself and other variables as input
        Returns a value that represents the sum of all the numbers after the values of the two numbers have been multilpied properly
        Unlike addition, I decided to throw a value error if the NVectors are not the same size, as this seems like we are emulating dot product which requires same size vectors
        i.e. NVector([3,0,1, -1]) * NVector([1,2,3,4]) == 3*1+0*2+1*3+(-1)*4 == 2
        or NVector([3,0,1, -1]) * 10 == 3*10+0*10+1*10+(-1)*10 == 30
        '''
        new_vec_list = []
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("NVector instances must be the same size for multiplication.")
            for i in range(len(self)):
                new_vec_list.append(self[i] * other[i])
        elif isinstance(other, int) or isinstance(other, float):
            for item in self.value_list:
                new_vec_list.append(item * other)
        else:
            raise TypeError("Cannot multiply objects of type {} and {}".format(type(self), type(other)))
        
        total = 0
        for num in new_vec_list:
            total += num
        
        return total
    
    def __rmul__(self, other) -> float:
        '''
        Function to control the reverse multiplication between this class object and other variables
        Simply pass them to the normal multiplication function to handle it due to communitative
        because of this, inputs and outputs mirror __mul__
        '''
        return self.__mul__(other)
    
    @classmethod
    def zeros(cls, n : int) -> object:
        '''
        Initializes a new NVector with all 0s
        takes a number as input, which is the dimension of the vector that will be filled with 0s
        returns the new NVector
        '''
        if not isinstance(n, int):
            raise TypeError("n must be an integer, remove the decimal point and try again.")
        if n >= 0:
            zeros = []
            for zero in range(n):
                zeros.append(0)
            return cls(zeros)
        else:
            raise ValueError("Must enter a positive number for size")

    





def main() -> None:
    '''
    Main function to call the testif to test parts a - i, which is the begining of the assignment to the multiplication functions
    As such, takes no conditions, and returns nothing as all of these are printed
    '''
    #part a test
    v = NVector([1, 2, 3, 4])
    testif(v[1] == 2, "List constructor initialize", "Constructor Working", "Constructor Failed") #part a test
    print("\n") #New line for readability
    
    #part b test
    v = NVector(1, 2, 3, 4)
    testif(v[1] == 2, "Multi-value constructor initialize", "Constructor Working", "Constructor Failed")
    print("\n") #New line for readability
    
    #part c test
    testif(len(v) == 4, "len test", "__len__ working as intended", "__len__ not working as intended")
    print("\n") #New line for readability
    
    #part d test
    testif(v[0] == 1, "getitem test", "getitem correctly recalling number", "getitem incorrectly recalling number")
    print("\n") #New line for readability
    testif(v[-1] == 4, "getitem negative index test", "getitem correctly recalling negative index number", "getitem incorrectly recalling negative index number")
    print("\n")
    
    #part e test
    v[3] = 10
    testif(v[3] == 10, "setitem test", "setitem correctly setting numbers in proper index", "set item not correctly setting number")
    print("\n") #New line for readability
    v[-2] = 10
    testif(v[-2] == 10, "setitem test", "setitem correctly setting numbers in proper negative index", "set item not correctly setting number in negative index")
    print("\n") #New line for readability

    
    #part f test
    testif(str(v) == "NVector, Currently holding a vector with dimensions of: 4\nThe values on each dimension are: [1, 2, 10, 10]", "str test", "NVector prints a message", "NVector fails to print the correct message")
    print("\n") #New line for readability
    
    #part g test
    testif(v == NVector(1, 2, 10, 10), "equal test", "equality function working as intended", "equality function failing to correctly identify equal vectors")
    print("\n")
    testif(v != NVector(1, 2, 3, 4), "notequal test", "inequality function working as intended", "inequality function failing to correctly recognize non-equal vectors")
    print("\n") #New line for readability
    
    #part h test
    testif(v + NVector(1, 1, 1, 1) == NVector(2, 3, 11, 11), "add function test (NVector)", "add function working as intended", "add function failing to add values correctly")
    print("\n")
    testif(v + 10 == NVector(11, 12, 20, 20), "add fucntion test (int)", "add function working as intended", "add function failing to add values correctly")
    print("\n")
    testif(10 + v == NVector(11, 12, 20, 20), "radd function test", "radd function working as intended", "radd function failing to add values correctly")
    print("\n") #New line for readability
    
    #part i test
    testif(v * NVector(2, 2, 2, 2) == 46, "Mult function test(NVector)", "multiply function working as intended", "multiply function failing to return correct value")
    print("\n")
    testif(v * 10 == 230, "Mult function test(int)", "multiply function working as intended", "multiply function failing to return correct value")
    print("\n")
    testif(10 * v == 230, "rMult function test", "rmultiply function working as intended", "rmultiply function failing to return correct value")
    
    #Extra test myself to ensure zeroes works, not part of the assignment as it only wants a - i and this is j
    print(NVector.zeros(5))
    
    

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