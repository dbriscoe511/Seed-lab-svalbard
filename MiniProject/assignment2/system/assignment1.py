import numpy


'''
THis code performs two fuctions,
list_excersize takes in a text file contiaing a list of numbers, and it is parsed for a number of charecteristics. 
the result is printed in the console

state_machine_ex is a practice excersize that uses a state machine to see if a string contains 'abcd' 
in python " 'abcd' is in string' can be used, but this excersize was teaching state machine use.

each letter corresponds to a state, with the ability to move to the next letters state, back to a, or back to none.
s
To run: run assignment1.py in the console. make sure numpy is installed 
use 0/enter/False to skip or 1/True to run each function when prompted. 

'''
def list_excersize():
    with open ('datafile.txt','r') as file:
        b = eval(file.read()) # eval makes this a list 
        print(max(b)) #max in list
        print(min(b)) # min in list
        print(b.index(38)) # index of 38
        
        '''
        prints out the maimum amount of repeats for an element 
        '''
        repeats = {i:b.count(i)for i in b} # creates a dict of each element, and its number of repeats. 
        rep = sorted(repeats, key=repeats.get) #sorts by number of repeats
        for i in reversed(rep): # goes through the list backwards because it is sorted low to high by default.
            if int(repeats[i]) >= repeats[rep[-1]]: 
                #checks if there are multiple numbers that have the same amount of repeats
                print("The list contains "+ str(repeats[i]) + " of "+str(i))

        bsort = numpy.sort(b)
        print(bsort) #sorted list 
        even = [i for i in bsort if i%2 == 0] #list comprehension for even numbers
        print(even)

def state_machine_ex():
    userstr = input("give me a string: ")
    state = 0
    for char in userstr:
        #print(state)

        if state == 0:
            if char == 'a':
                state = 'a'
            else:
                state = 0

        elif state == 'a':
            if char == 'b':
                state = 'b'
            elif char == 'a':
                state = 'a'
            else:
                state = 0
            
        elif state == 'b':
            if char == 'c':
                state = 'c'
            elif char == 'a':
                state = 'a'
            else:
                state = 0
            
        elif state == 'c':
            if char == 'd':
                state = 0
                print('abcd is in string')
            elif char == 'a':
                state = 'a'
            else:
                state = 0


#asks the user if they would like to run the exercises
if(bool(input('run file excersize?'))):
    list_excersize()
if(bool(input('run state excersize?'))):
    state_machine_ex()



    