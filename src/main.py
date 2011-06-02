###########################
# main.py
# Group 6: Academic Planner
###########################

import sys
from datetime import datetime
from Numberjack import *
import Mistral
import DataStructures
from Output import Outputter

silent = True

def debug_print(msg):
    if not silent:
        print msg

# creates and solves a model for a given major
def generateSchedule(majorName):
    major = DataStructures.Major.getMajor(majorName)
    debug_print("Major: " + major.title)
    debug_print("Minimum units: " + str(major.minUnits))
    debug_print("Total # of classes: " + str(len(major.courses)))

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
    #Z = Variable(1, len(major.courses))
    
    # declare the Numberjack Constraint Model
    model = Model()
    
    # SEE page 14 fig. 4 of paper for mathematical constraints:
    #     http://www.csun.edu/~vcmgt0j3/Publications/CP05%20Paper.pdf
    
    # OBJECTIVE FUNCTION: minimize Z
    # @TODO: currently this makes the solver take forever to run, investigate!
    #for i in range(len(courseTerms)):
    #    model.add(courseTerms[i] <= Z)
    #model.add(Minimize(Z))
    
    # Get the min unit for the major
    minUnits = int(major.minUnits)
    
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
        
        # for each prerequisite (String course code of prereq course)
        for prereq in prereqs:
            # get the index of the prerequisite course in the master course array
            prereqIndex = major.getCourseIndex(prereq)
            
            # make sure prerequisite constraint is satisfied:
            #    (1) course is taken AND the current prerequisite is satisfied
            #    (2) OR course was not taken (therefore prereqs don't have to be)
            #    NOTE: & and | logical operators are required for numberjack
            #         'and' and 'or' won't work... we had lots of early bugs from this
            model.add(((courseTerms[i] > 0) & (0 < courseTerms[prereqIndex] < courseTerms[i])) | (courseTerms[i] == 0))
        
        # CONSTRAINT: restrict course offerings for each course
        # get the offerings for each course
        offerings = course.offerings
        invalidTerms = [t for t in masterCourseTerms if str(t) not in offerings]
        #debug_print course.courseCode + ": " + str(invalidTerms)
        
        # restrict terms available to each course
        for k in invalidTerms:
            model.add(courseTerms[i] != k)  
    
    
    # CONSTRAINT: MAX UNIT LOAD IS ENFORCED FOR EACH TERM
    # for each possible term
    for term in range(1, len(courseTerms)):
        # the sum of courses scheduled for the current term must be <= the max allowed in a single term
        # 'i' represents the index of the course in the master course array
        # 'courseTerms[i]' is the term course i is scheduled for
        # 'term' is the current term we are adding the constraint for 
        model.add(sum([(courseTerms[i] == term) for i in range(len(courseTerms))]) <= 4 )
    
    # CONSTRAINT: Minimum units for major is met
    model.add(sum([(int(major.courses[i].units) * (courseTerms[i]>0)) for i in range(len(courseTerms))]) >= minUnits )
    
    # Solve the Model
    msolver = model.load('Mistral', courseTerms)
    debug_print("Solving...")
    starttime = datetime.now()
    msolver.solve()
    endtime = datetime.now()
    elapsed = endtime - starttime
    debug_print("Solution took " + str(elapsed))
     
    # debug_print final solution
    #@TODO: this will eventually be formatted output for the php ui script to read       
    outputter = Outputter(major, courseTerms, msolver)
    outputter.outputXML()
    #outputter.printSchedule()

# Generate a proposed schedule for selected major, or ics if none specified
selectedMajor = 'ics'
if len(sys.argv) > 1:
    selectedMajor = sys.argv[1]
generateSchedule(selectedMajor)



# DONT LOOK HERE -- THIS IS WHERE CODE GOES TO DIE

    #debug_print "\n\nDISPLAYING COURSE SELECTION FOR MAJOR " + major.title
    #for i in range(len(major.courseGroups)):
    #    debug_print "\n############################"
    #    courseGroup = major.courseGroups[i]
    #    debug_print "Classes for course group: " + courseGroup.title
    #    startIndex = courseGroup.startIndex
    #    endIndex = startIndex + len(courseGroup.courses)
    #    for j in range(len(courseGroup.courses)):
    #        debug_print courseGroup.courses[j].courseCode + ": " + str(courseTerms[startIndex + j].get_value(msolver))
