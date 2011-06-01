import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation

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
        for i in range(1, max_term+1):
            print "\nTerm " + str(i) + ": "
            coursesForTerm = [str(self.major.courses[j].courseCode) for j in range(len(self.courseTerms)) if (self.courseTerms[j].get_value(self.solver) == i)]
            print coursesForTerm
    
    # writes results as XML objects to output stream for use by UI
    def outputXML(self):
        impl = getDOMImplementation()
        
        # create xml doc
        xmldoc = impl.createDocument(None, "results", None)
        resultsElement = xmldoc.documentElement
        
        # write number of terms node
        numTermsElement = xmldoc.createElementNS(None, "num_terms")
        text = xmldoc.createTextNode(str(self.maxTerm))
        numTermsElement.appendChild(text)
        resultsElement.appendChild(numTermsElement)
        
        # write the terms list
        for i in range(len(self.terms)):
            # create a new term node for each item in list
            termElement = xmldoc.createElementNS(None, "term")
            
            termNumberElement = xmldoc.createElementNS(None, "term_number")
            text = xmldoc.createTextNode(str(i))
            termNumberElement.appendChild(text)
            termElement.appendChild(termNumberElement)
            
            coursesElement = xmldoc.createElementNS(None, "courses")
            termElement.appendChild(coursesElement)
            
            # create a new course node for each item in term
            for j in range(len(self.terms[i])):
                course = self.terms[i][j]
                
                courseElement = xmldoc.createElementNS(None, "course")
                codeElement = xmldoc.createElementNS(None, "course_code")
                text = xmldoc.createTextNode(course.courseCode)
                codeElement.appendChild(text)
                courseElement.appendChild(codeElement)
                
                coursesElement.appendChild(courseElement)
                
                
                
            
            resultsElement.appendChild(termElement)
        
        print xmldoc.toprettyxml()
     
    #def jsonRepresentation(self):
    #    d = dict()
    #    d['terms_to_complete'] = self.maxTerm
    #    d['terms'] = []
    #    for i in range(len(self.terms)):
    #        term = [course.__dict__ for course in self.terms[i]]
    #        d['terms'].append(term)
    #    d['starting_term_year'] = self.startingTermYear
    #    d['starting_term_quarter'] = self.startingTermTerm 
    #    return d
        
