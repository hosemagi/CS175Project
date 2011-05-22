'''
Created on May 9, 2011

@author: will
'''
from datetime import datetime
from Numberjack import *
import Mistral

max_terms = 4
total_classes = 27

lastTerm = Variable(0, max_terms)
term = VarArray(total_classes, 0, max_terms)
courses_a = range(0, 7)
courses_b = range(7, 12)
courses_c1 = range(12, 15)
courses_c2 = range(15, 18)
courses_c3 = range(18, 21)
courses_c4 = range(21, 24)
courses_c5 = range(24, 27)
    
model = Model()

model.add([ term[c] <= max_terms for c in term ])
model.add([ sum((term[c]>0) for c in courses_a)>=7 ])
model.add([ sum((term[c]>0) for c in courses_b)>=5 ])
model.add([ (sum((term[c]>0) for c in courses_c1)>=3) | (sum((term[c]>0) for c in courses_c2)>=3) | 
    (sum((term[c]>0) for c in courses_c3)>=3) | (sum((term[c]>0) for c in courses_c4)>=3) | 
    (sum((term[c]>0) for c in courses_c5)>=3) ])
model.add([ sum((term[c] == 1) for c in range(total_classes))<=4 ])
model.add([ sum((term[c] == 2) for c in range(total_classes))<=4 ])
model.add([ sum((term[c] == 3) for c in range(total_classes))<=4 ])
model.add([ sum((term[c] == 4) for c in range(total_classes))<=4 ])

#model.add( Minimise(term[c] for c in range(max_terms)<=max_terms) )

msolver = Mistral.Solver(model)


print "Solving..."
starttime = datetime.now()
msolver.solve()
endtime = datetime.now()
elapsed = endtime - starttime
print "Solution took " + str(elapsed)

print term
