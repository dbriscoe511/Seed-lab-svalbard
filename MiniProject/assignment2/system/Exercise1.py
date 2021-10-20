import statistics
from statistics import mode
import numpy as np

with open('datafile.txt','r') as f:
    b = eval(f.read())


print('Max: ' + str(max(b)) 
    + '\nMin: ' + str(min(b)) 
    + '\nIndex: ' + str(b.index(38)) 
    + '\nMost Repeated: ' + str(mode(b))
    + '\nTimes Repeated: ' + str(b.count(mode(b))) 
    + '\nArray: ' + str(np.sort(b)) 
    + '\n Evens: ' + str([x for x in np.sort(b) if not x%2]))