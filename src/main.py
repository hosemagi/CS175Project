###########################
# main.py
# Group 6: Academic Planner
###########################

from datetime import datetime
from Numberjack import *
import Mistral
import DataStructures

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    return original[:pos] + new + original[pos:]



# creates and solves a model for a given major
def generateSchedule(majorName):
    major = DataStructures.Major.getMajor(majorName)
    print "Major: " + major.title
    print "Minimum units: " + str(major.minUnits)
    print "Total # of classes: " + str(len(major.courses))

    # Maximum unit load per term
    # @TODO: change term unit load constraint to use this variable
    max_term_units = 16
    
    # A Numberjack array of Variables
    #    - the index of an element in the array represents a course (as its index in major.courses)
    #    - the value of element 'i' in the array is an int representing the term course 'i' was scheduled for
    courseTerms = VarArray(len(major.courses), 0, len(major.courses))
    masterCourseTerms = range(1, len(major.courses))
    
    # Z is a Numberjack Variable that represents the maximum number of terms
    # Ultimate goal is to produce solutions that minimize Z 
    Z = Variable(1, len(major.courses))
    
    # declare the Numberjack Constraint Model
    model = Model()
    
    # SEE page 14 fig. 4 of paper for mathematical constraints:
    #     http://www.csun.edu/~vcmgt0j3/Publications/CP05%20Paper.pdf
    
    # OBJECTIVE FUNCTION: minimize Z
    # @TODO: currently this makes the solver take forever to run, investigate!
    # for i in range(len(courseTerms)):
    #    model.add(courseTerms[i] <= Z)
    # model.add(Minimize(Z))
    
    # CONSTRAINT: REQUIREMENTS MET FOR EACH COURSE GROUP
    # for each course group
    for i in range(len(major.courseGroups)):
        # get an easy reference to the current courseGroup
        courseGroup = major.courseGroups[i]
        
        # get the start and end indices of this course group in the master 'courses' array
        startIndex = courseGroup.startIndex
        endIndex = startIndex + len(courseGroup.courses)
        
        # add a constraint for this course group
        # the sum of all of the taken courses in this group must be
        #    at least the minimum number required from this group
        # course[i] taken is defined by courseTerms[i] > 0
        model.add(sum([courseTerms[k] > 0 for k in range(startIndex, endIndex)]) >= int(courseGroup.numCoursesRequired))
        
    # CONSTRAINT: PREREQUISITE REQUIREMENTS ARE SATISFIED FOR SELECTED COURSES
    # for each course in the full list of courses
    for i in range(len(courseTerms)):
        # get an easy reference for the current course
        course = major.courses[i]
    
        # get an easy reference for the prerequisites for the current course
        prereqs = course.prereqs
        offerings = course.offerings
        invalidTerms = []
        for j in masterCourseTerms:
            if j not in offerings:
                invalidTerms.append(j)
        for k in invalidTerms:
            model.add(courseTerms[i] != k)
        #list = ''
        #for j in offerings:
        #    list += ('(courseTerms[i] = ' + str(j) + ') | ')
        #list = list[:-3]
        #begin = 'model.add('
        #list = begin + list
        #list += ')'
        #print course.courseCode + ': ' + list
        
        
        # for each prerequisite (String course code of prereq course)
        for prereq in prereqs:
            # get the index of the prerequisite course in the master course array
            prereqIndex = major.getCourseIndex(prereq)
            
            # make sure prerequisite constraint is satisfied:
            #    (1) course is taken AND the current prerequisite is satisfied
            #    (2) OR course was not taken (therefore prereqs don't have to be)
            #    NOTE: & and | logical operators are required for numberjack
            #         'and' and 'or' won't work... we had lots of early bugs from this
            model.add((courseTerms[i] > 0) & (0 < courseTerms[prereqIndex] < courseTerms[i]) | (courseTerms[i] == 0))
    
    # CONSTRAINT: MAX UNIT LOAD IS ENFORCED FOR EACH TERM
    # for each possible term
    for term in range(1, len(courseTerms)):
        # the sum of courses scheduled for the current term must be <= the max allowed in a single term
        # 'i' represents the index of the course in the master course array
        # 'courseTerms[i]' is the term course i is scheduled for
        # 'term' is the current term we are adding the constraint for 
        model.add(sum([(courseTerms[i] == term) for i in range(len(courseTerms))]) <= 4 )
    
    
    #@TODO: Constraints to be added:
    # "course offering" constraints
    # min units for major constraint
    
    # Solve the Model
    msolver = model.load('Mistral', courseTerms)
    print "Solving..."
    starttime = datetime.now()
    msolver.solve()
    endtime = datetime.now()
    elapsed = endtime - starttime
    print "Solution took " + str(elapsed)
     
    # print final solution
    #@TODO: this will eventually be formatted output for the php ui script to read       
    printSchedule(major, courseTerms, msolver)



# printSchedule is a convenient method for outputting the results of the solver        
def printSchedule(major, courseTerms, solver):
    print "\n\n\n\n#########################################################"
    print "####        PROPOSED SCHEDULE                        ####"
    print "#########################################################"
    max_term = max([courseTerms[i].get_value(solver) for i in range(len(courseTerms))])
    # added print for debugging
    print max_term
    for i in range(1, max_term):
        print "\nTerm " + str(i) + ": "
        coursesForTerm = [str(major.courses[j].courseCode) for j in range(len(courseTerms)) if (courseTerms[j].get_value(solver) == i)]
        print coursesForTerm

# Generate a proposed schedule for ICS Major
generateSchedule('ics')



# DONT LOOK HERE -- THIS IS WHERE CODE GOES TO DIE

    #print "\n\nDISPLAYING COURSE SELECTION FOR MAJOR " + major.title
    #for i in range(len(major.courseGroups)):
    #    print "\n############################"
    #    courseGroup = major.courseGroups[i]
    #    print "Classes for course group: " + courseGroup.title
    #    startIndex = courseGroup.startIndex
    #    endIndex = startIndex + len(courseGroup.courses)
    #    for j in range(len(courseGroup.courses)):
    #        print courseGroup.courses[j].courseCode + ": " + str(courseTerms[startIndex + j].get_value(msolver))
