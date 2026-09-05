import math
import matplotlib.pyplot as pylab

stop = False

while not stop:
    #Need to add the exit strat for pressing enter
    a = input("Enter Variable 'a' here (or alternatively hit the enter button without entering anything to quit) ")

    if a == "":
        stop = True
        break

    b = input("Enter Variable 'b' here: ")
    c = input("Enter Variable 'c' here: ")

    roots = 0

    a = float(a)
    b = float(b)
    c = float(c)

    comp = ((b * b) - 4 * a * c)

    if comp < 0:
        print("no real solution")
        roots = 0

    elif comp > 0:
        root1 = (-b + math.sqrt(comp)) / (2 * a)
        root2 = (-b - math.sqrt(comp)) / (2 * a)
        print("two solutions:", root1, root2)
        roots = 2


    else:
        root = (-b + math.sqrt(comp)) / (2 * a)
        print("one solution:", root)
        roots = 1
  
    xvalues = []
    yvalues = []
    for x in range(-75, 75): #Create a range of 150 points, evenly distributed between negative and positive numbers
        xvalues.append(x)
        y = (a * (x ** 2)) + (b * x) + c
        yvalues.append(y)

    #PDF says we need to show the values on the graph, but i think it might also be asking for showing all points
    #So the first uncommented below is for just the line, and the commented out one shows all points in blue
    pylab.plot(xvalues, yvalues)
    #pylab.plot(xvalues, yvalues, "bo")
    if roots == 2:
        pylab.plot(root1, 0, 'ro')
        pylab.plot(root2, 0, 'ro')
    elif roots == 1:
        pylab.plot(root, 0, 'ro')
    else:
        center = -b / (2 * a)
        pylab.plot(center, 0, 'ro')
        print("Setting center to domains max / minimum: " + str(center))

    pylab.plot()
    pylab.show()