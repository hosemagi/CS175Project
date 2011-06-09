###########################
# main.py
# Group 6: Academic Planner
###########################

import sys
import math
from datetime import datetime
from Numberjack import *
import Mistral
import DataStructures
from Output import Outputter

silent = True

# Configuration Variables (default values) 
selectedMajor = 'ics'               # the code for major to generate a plan for
max_term_units = 20                 # the maximum number of units to schedule in an individual term
preferredCourses = []               # a list of courses that the user wishes to include in the plan
optimizeTimeToCompletion = False    # if this is false, we will use a heuristic method instead to find a reasonable time to completion
optimizeTotalDifficulty = False     # if this is false, we will use a heuristic method instead to find a reasonable overall difficulty rating

TermDifficulty = None


def debug_print(msg):
    if not silent:
        print msg

# creates and solves a model for a given major
def generateSchedule(majorName, max_term_units, preferredCourses):
    major = DataStructures.Major.getMajor(majorName)
    debug_print("Major: " + major.title)
    debug_print("Minimum units: " + str(major.minUnits))
    debug_print("Total # of classes: " + str(len(major.courses)))
    
    # A Numberjack array of Variables
    #    - the index of an element in the array represents a course (as its index in major.courses)
    #    - the value of element 'i' in the array is an int representing the term course 'i' was scheduled for
    courseTerms = VarArray(len(major.courses), 0, len(major.courses)/2)
    masterCourseTerms = range(1, len(major.courses))
    
    # declare the Numberjack Constraint Model
    model = Model()
    
    # SEE page 14 fig. 4 of paper for mathematical constraints:
    #     http://www.csun.edu/~vcmgt0j3/Publications/CP05%20Paper.pdf
    
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
        model.add(sum([(int(major.courses[i].units) * (courseTerms[i] == term)) for i in range(len(courseTerms))]) <= max_term_units)
        
    
    # CONSTRAINT: MINIMUM UNIT REQUIREMENT FOR MAJOR IS MET
    model.add(sum([(int(major.courses[i].units) * (courseTerms[i]>0)) for i in range(len(courseTerms))]) >= minUnits )
    
    # CONSTRAINT: EACH PREFERRED ELECTIVE IS TAKEN
    for i in range(len(preferredCourses)):
        courseCode = preferredCourses[i]
        courseIndex = major.getCourseIndex(courseCode)
        model.add(courseTerms[courseIndex] > 0)
    
    # OPTIMIZATION: FIND A SCHEDULE WITH A REASONABLY LOW DIFFICULTY RATING
    if optimizeTimeToCompletion:    
        TermsToCompletion = Variable(1, len(major.courses))
        for i in range(len(courseTerms)):
            model.add(courseTerms[i] <= TermsToCompletion)
        model.add(Minimize(TermsToCompletion))
    else:
        # if we have chosen not to perform a true optimization to minimize the overall time to completion, we can apply the following heuristic
        # choose a minimum number of units to schedule per term based on the maximum, taken as min=ceil((max-1)/4)*4
        # enforce this constraint
        if max_term_units > 16:
            min_term_units = 16
        elif max_term_units > 12:
            min_term_units = 12
        else:
            min_term_units = 8
        model.add(sum([(int(major.courses[i].units) * (courseTerms[i] == term)) for i in range(len(courseTerms))]) >= min_term_units)
    
    # Minimize overall difficulty
    #TermDifficulty = VarArray(len(major.courses), 0, 0)
    #if optimizeTotalDifficulty:
    #    TermDifficulty = VarArray(len(major.courses), 0, 15)
    #    for term in range(len(TermDifficulty)):
            # add the constraint that the value of the TermDifficulty[i] must be the sum
            # of difficulty ratings for term [i]
    #        model.add(TermDifficulty[term] == sum([(int(major.courses[i].diff) * (courseTerms[i] == term)) for i in range(len(courseTerms))]))
    #    model.add(Minimize(Sum(TermDifficulty)))
    
    
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
    outputter = Outputter(major, courseTerms, TermDifficulty, msolver)
    #outputter.outputXML()
    outputter.printSchedule()

# Parse command-line args from PHP script or other source
# argv[1] = major
# argv[2] = max units per term
# argv[3..n] = preferred course codes

if len(sys.argv) > 1:
    selectedMajor = sys.argv[1]

if len(sys.argv) > 2:
    max_term_units = int(sys.argv[2])
    
if(len(sys.argv) > 3):
    for i in range(3, len(sys.argv)):
        courseCode = sys.argv[i]
        preferredCourses.append(courseCode)

# Generate a proposed schedule for selected major, or ics if none specified
generateSchedule(selectedMajor, max_term_units, preferredCourses)


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
