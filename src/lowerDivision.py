'''
Created on May 9, 2011

@author: will
'''
from datetime import datetime
from Numberjack import *
import Mistral
import DataStructures

major = DataStructures.Major.getMajor('ics')

model = Model()

model.add()

#model.add( Minimise(term[c] for c in range(max_terms)<=max_terms) )

msolver = Mistral.Solver(model)


print "Solving..."
starttime = datetime.now()
msolver.solve()
endtime = datetime.now()
elapsed = endtime - starttime
print "Solution took " + str(elapsed)

print v
