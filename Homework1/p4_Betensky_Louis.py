import math
import matplotlib.pyplot as pylab


func = input("Please tpye in the function you wish to see graphed: ")
mini = input("Please enter functions minimum domain value: ")
maxi = input("Please enter the functions maximum domain value: ")
samples = int(input("Please enter how many samples you would like to see: "))

mini = float(mini)
maxi = float(maxi)

def plot_function(fun_str : str, domain: tuple, ns : int):
    domain_size = domain[1] - domain[0]
    xlist = []
    ylist = []
    
    for point in range(ns):
        x = domain_size * (point / ns)
        xlist.append(x)
        ylist.append(eval(fun_str))
    
    print(" x  |  y ")
    print("----|----")
    for i in range(len(xlist)):
        print(" {}  |  {} ".format(xlist[i], ylist[i]))
    
    pylab.plot(xlist, ylist)
    pylab.plot(xlist, ylist, "ro")
        

plot_function(func, [mini, maxi], samples)