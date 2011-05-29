import json

class Outputter:
    
    def __init__(self, major, courseTerms, solver):
        self.major = major
        self.courseTerms = courseTerms
        self.solver = solver
        self.terms = []
        self.maxTerm = max([courseTerms[i].get_value(solver) for i in range(len(courseTerms))])
        for i in range(1, self.maxTerm):
            thisTerm = [major.courses[j] for j in range(len(courseTerms)) if (courseTerms[j].get_value(solver) == i)]
            self.terms.append(thisTerm)
        self.startingTermYear = 2011
        self.startingTermTerm = 0  #0 fall, 1 winter, 2 spring, no summer
    
    # printSchedule is a convenient method for outputting the results of the solver        
    def printSchedule(self):
        print "\n\n\n\n#########################################################"
        print "####        PROPOSED SCHEDULE                        ####"
        print "#########################################################"
        max_term = max([self.courseTerms[i].get_value(self.solver) for i in range(len(self.courseTerms))])
        for i in range(1, max_term):
            print "\nTerm " + str(i) + ": "
            coursesForTerm = [str(self.major.courses[j].courseCode) for j in range(len(self.courseTerms)) if (self.courseTerms[j].get_value(self.solver) == i)]
            print coursesForTerm
    
    # writes results as JSON objects to output stream for use by UI
    def outputJSON(self):
        print json.dumps(self.jsonRepresentation())
    
    def jsonRepresentation(self):
        d = dict()
        d['terms_to_complete'] = self.maxTerm
        d['terms'] = []
        for i in range(len(self.terms)):
            term = [course.__dict__ for course in self.terms[i]]
            d['terms'].append(term)
        d['starting_term_year'] = self.startingTermYear
        d['starting_term_quarter'] = self.startingTermTerm 
        return d
        
