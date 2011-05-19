'''
Created on May 9, 2011

@author: will
'''

from Numberjack import *
import Mistral

max_terms = 3

lastTerm = Variable(0, max_terms)
term = VarArray(12, 0, max_terms)
courses_a = range(0, 7)
courses_b = range(7, 12)
#courses_c1 = range(12, 15)
#courses_c2 = range(15, 18)
#courses_c3 = range(18, 21)
#courses_c4 = range(21, 24)
#courses_c5 = range(24, 27)
    
model = Model()

model.add([ term[c] <= max_terms for c in term ])
model.add([ sum((term[c]>0) for c in courses_a)>=7 ])
model.add([ sum((term[c]>0) for c in courses_b)>=5 ])
#model.add([ (sum((term[c]>0) for c in courses_c1)>=3) | (sum((term[c]>0) for c in courses_c2)>=3) | 
#    (sum((term[c]>0) for c in courses_c3)>=3) | (sum((term[c]>0) for c in courses_c4)>=3) | 
#    (sum((term[c]>0) for c in courses_c5)>=3) ])
model.add([ sum((term[c] == 1) for c in range(12))<=4 ])
model.add([ sum((term[c] == 2) for c in range(12))<=4 ])
model.add([ sum((term[c] == 3) for c in range(12))<=4 ])
model.add([ sum((term[c] == 4) for c in range(12))<=4 ])

#model.add( Minimise(term[c] for c in range(max_terms)<=max_terms) )

msolver = Mistral.Solver(model)
msolver.solve()

print term

#def cs_lower_model(max_terms):
#    courses_a = VarArray(7, 0, max_terms+1),
#    courses_b = VarArray(5, 0, max_terms+1)
#    courses_c1 = VarArray(3, 0, max_terms+1)
#    courses_c2 = VarArray(3, 0, max_terms+1)
#    courses_c3 = VarArray(3, 0, max_terms+1)
#    courses_c4 = VarArray(3, 0, max_terms+1)
#    courses_c5 = VarArray(3, 0, max_terms+1)
#    terms = [max_terms]
    
#    model = Model([
#        sum(courses_a)>=7, 
#        sum(courses_b)>=5,
#        (sum(courses_c1)>=3) | (sum(courses_c2)>=3) | (sum(courses_c3)>=3) | 
#        (sum(courses_c4)>=3) | (sum(courses_c5)>=3)
#    ])
