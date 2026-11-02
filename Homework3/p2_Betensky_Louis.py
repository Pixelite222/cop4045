class ParkingPermit:
    '''
    Base class for Parking Permits that will be used for the two subclasses later
    '''
    def __init__(self, name : str = "", mon_ctr : int = 0, fee_sched : dict = None) -> None:
        '''
        Basic initialization function the two subclasses will be using.
        Takes the class instance itself, a string that serves as the permit holders name, an int that serves as the months they have the permit, and a dictionary meant to be used as a schedule for the fees
        Each of the listed variables above have a default incase they haven't been set by whatever calls it.
        Returns None because this function instead sets internal variables
        '''
        self.name = name
        self.mon_ctr = mon_ctr
        if fee_sched is None or fee_sched == {}:
            raise ValueError("Dictionary is empty or not supplied.  This is neccissary for cost, and a basic dictionary according to the assignment is 25 a month for a student and 40 a month for a faculty member")
        else:
            self.fee_sched = fee_sched
    
    def cost(self) -> int:
        '''
        Base cost function
        Only takes the class instance as an input
        Returns the total, which in this base class is just set to 0, as the subclasses have their own logic and this is essntially unused outside of being a super()
        '''
        total = 0
        return total
    
    def __str__(self) -> str:
        '''
        String dunder function for the class, giving a basic message when trying to print or access the class instance as a string
        Takes the class instance itself as input
        Returns the string allowing for easeier understanding of the class
        '''
        return "Base level Parking Permit class.for accurate pricing, please declare and print either a StudentPermit or FacultyPermir for a student or faculty respectively. \nCurrent variables are name: {}, months : {}, fee schedule: {}".format(self.name, str(self.mon_ctr), str(self.fee_sched))
    
    def __repr__(self) -> str:
        '''
        Representation dunder function for the base class.  Similar to __str__ but with more info, meant for developer or programmer access
        Like __str__, takes the class instance as input
        Returns the string displaying the message needed
        '''
        return "Base Level Parking Permit\nName: {}\nMonths: {}\nFee Schedule{}\nTo recreate, copy and paste the following: ParkingPermit(\"{}\", {}, {})".format(self.name, str(self.mon_ctr), str(self.fee_sched), self.name, str(self.mon_ctr), str(self.fee_sched))
    

class StudentPermit(ParkingPermit):
    '''
    First required subclass
    This subclass is used for the students, using ParkingPermit as it's parent class
    The main addition this class has from the basic class (outside of more detailed functions) is the car_reg variable which is used to increase the price dependent on the amount of cars the student has registered
    '''
    def __init__(self, name : str = "", mon_ctr : int = 0, fee_sched : dict = None, car_reg : int = 0) -> None:
        '''
        Initializer for the student permit subclass.
        As such it takes the same inputs as the parent parking permit class, with the edition of one new one, car_reg, which is used to represent the amount of cars the student has registered
        Outputs nothing as this is the initializer and only sets the internal variables
        '''
        if fee_sched == None or fee_sched == {}:
            raise ValueError("Due to the wording of the assignment, we cannot hard code the monthly values.  Because of this we need the fee_sched dictionary to have the monthly prices despite knowing the default.  Student Permit hasn't recieved one and therefore can't be run")
        super().__init__(name, mon_ctr, fee_sched)
        self.car_reg = car_reg
    
    def cost(self) -> int:
        '''
        Student edition of the cost function
        Calculates student cost based on the parameters in the assignment, namely adding 10 dollars to the total for every car besides the first the student registered, and then adding monthly fee from the dict
        Takes the same input as the base class
        Returns the total cost for the student
        '''
        total = 0
        #Calculates Total
        for month in self.fee_sched.keys():
            total += self.fee_sched[month]
        if self.car_reg > 1:
            total += (self.car_reg - 1) * 10
        
        
        return total
                
    def __str__(self) -> str:
        '''
        Str dunder function for student
        While the message is more detailed, allowing for easier understanding to a reader, this is practically the same as the base classes __str__
        Main changes are showing actually values to the reader
        Input is the same as the base class
        Outputs the string for users to read.
        '''
        return "Student Parking Pass for {}.  Has a parking pass for {} months, with {} car's registered, costing them {} in total".format(self.name, str(self.mon_ctr), str(self.car_reg), str(self.cost()))
    
    def __repr__(self) -> str:
        '''
        repr dunder function for student
        Very similar to the base classes, showing details of the class instance, for programmers to view.
        Even adds a section allowing a dev to copy and paste a recreation of the class so they can use it in their program
        input is the same as the base class
        Outputs the string
        '''
        return "Student Parking Pass\nName: {}\nMonths: {}\nFee Schedule: {}\nCar's registered: {}\nThe cost function will return the total cost of the permit to be {} by adding up the fees per month in the dictionary, and adding 10 more dollars for each additional car registered.\nOther functions are fairly self explanatory\nTo recreate, copy and paste the following: StudentPermit(\"{}\", {}, {}, {})".format(self.name, str(self.mon_ctr), str(self.fee_sched), str(self.car_reg), self.cost(), self.name, str(self.mon_ctr), str(self.fee_sched), str(self.car_reg))

class FacultyPermit(ParkingPermit):
    '''
    Second required subclass
    Subclass of Parking Permit for Faculty to use.
    As such it is similar to both the base and student subclass
    Main difference is the garage variable that allows for garage access at a cost, as opposed to the students car_reg and the bases... nothing
    '''
    def __init__(self, name : str = "", mon_ctr : int = 0, fee_sched : dict = None, garage : bool = False) -> None:
        '''
        Initialization for the faculty subclass
        does the same thing as base, with the addition of the garage access bool variable which is set here
        Same inputs as base, with the exception of the addition garage
        Outputs none as it sets variables and nothing else
        '''
        if fee_sched == None or fee_sched == {}:
                    raise ValueError("Due to the wording of the assignment, we cannot hard code the monthly values.  Because of this we need the fee_sched dictionary to have the monthly prices despite knowing the default.  Faculty Permit hasn't recieved one and therefore can't be run")
        super().__init__(name, mon_ctr, fee_sched)
        self.garage = garage

        
        
    def cost(self) -> int:
        '''
        The cost function for the faculty subclass
        This version of cost works by checking garage access, and if it is active, adding an exta 15 dollars to the monthly payments.  These monthly payments are more expensive then students, starting at 40 dollars
        Outside of this, the structure is similar to the student subclass.  
        Input recieved is the same as the base, being the class instance
        Outputs the total, an int as we aren't dealing with floats
        '''
        total = 0
        #Calculates Total
        for month in self.fee_sched:
            total += self.fee_sched[month]
            if self.garage:
                total += 15
        
        return total
    
    def __str__(self) -> str:
        '''
        Str dunder for faculty pass
        With the exception of changing the car registration info to displaying if garage access is true or false and changing the word student to faculty, this is practically the same as the student one
        input is the same as base class
        Output is the string for easier reading
        '''
        return "Faculty Parking Pass for {}.  Has a parking pass for {} months.  Garage access set to: {}.  This costs a total of {}.".format(self.name, str(self.mon_ctr), str(self.garage), str(self.cost()))
        
    
    def __repr__(self) -> str:
        '''
        repr dunder for faculty pass
        Similarly to str, pretty much the same as the student edition outside of the change in student to faculty and car_reg to garage access
        input same as base
        output is the string for devs, copy and paste included
        '''
        return "Faculty Parking Pass\nName: {}\nMonths: {}\nFee Schedule: {}\nGarage Access: {}\nThe cost function will return the total cost of the permit to be {} by adding up the fees per month in the dictionary, and adding 15 more dollars if garage access is true.\nOther functions are fairly self explanatory\nTo recreate, copy and paste the following: FacultyPermit(\"{}\", {}, {}, {})".format(self.name, str(self.mon_ctr), str(self.fee_sched), str(self.garage), self.cost(), self.name, str(self.mon_ctr), str(self.fee_sched), str(self.garage))
    
    
def summarize_list(permit_list : list[ParkingPermit]) -> int:
    '''
    Finds the total revenue from a list of permits, no matter if the permits are student, faculty, or somehow the base class
    input is a mixed list of permit class instances
    output is the int found after adding the total cost of all permits together
    '''
    tot_rev = 0
    for permit in permit_list:
        permit_cost = permit.cost()
        #print(permit.__repr__(), "\n")
        print(str(permit), "\n")
        #print(permit.name, ", ", str(permit_cost))
        tot_rev += permit_cost
    
    return tot_rev

def main() -> None:
    '''
    Main function showcasing the classes working as intended
    Creates 2 permits, one student and one faculty, prints them both to show them working as intended, then prints the total between the two permits
    takes no input, nor does it return anything as the entire program happens here
    '''

    SP2 = StudentPermit("Louie B Custom", 5, {1 : 15, 2 : 20, 3 : 25, 4 : 30, 5 : 35}, 3) #Should be 145
    FP2 = FacultyPermit("Mr. Louie Custom", 5, {1 : 35, 2 : 40, 3 : 45, 4 : 50, 5 : 55}, True) #Should be 300
    SPA = StudentPermit("Louie B Correct", 5, {1 : 25, 2 : 25, 3 : 25, 4 : 25, 5 : 25}, 3) #Should be 145
    FPA = FacultyPermit("Mr. Louie Correct", 5, {1 : 40, 2 : 40, 3 : 40, 4 : 40, 5 : 40}, True) #Should be 275

    #To "Show how the classes and functions are used", going to print repr here
    print(repr(SP2), "\n")
    print(repr(FP2), "\n")
    print(repr(SPA), "\n")
    print(repr(FPA), "\n")
    
    print("Total cost of mixed list is: ", str(summarize_list([SP2, FP2, SPA, FPA])))

main()

print("Louis Betensky, Z-Number: Z23542578")