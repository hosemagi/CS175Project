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
max_term_units = 20               # the maximum number of units to schedule in an individual term
preferredCourses = []               # a list of courses that the user wishes to include in the plan
optimizeTimeToCompletion = False    # if this is false, we will use a heuristic method instead to find a reasonable time to completion
optimizeTotalDifficulty = False     # if this is false, we will use a heuristic method instead to find a reasonable overall difficulty rating
difficultyThreshold = "very hard"

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
    # Note: if we have chosen not to minimize the term to completion and use a heuristic instead,
    # this constraint will be set later
    if optimizeTimeToCompletion:
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
        min_term_units = 8
        if max_term_units > 16:
            min_term_units = 16
        elif max_term_units > 12:
            min_term_units = 12
        for term in range(1, 20):
            model.add(min_term_units <= sum([(int(major.courses[i].units) * (courseTerms[i] == term)) for i in range(len(courseTerms))]) <= max_term_units)
    
    # OPTIMIZATION: MINIMIZE OVERALL DIFFICULTY
    TermDifficulty = VarArray(len(major.courses), 0, 20)
    
    #define TermDifficulty in the constraint network 
    for term in range(1, 20):
        model.add(TermDifficulty[term] == sum([(int(major.courses[i].diff) * (courseTerms[i] == term)) for i in range(len(courseTerms))]))
    
    # check optimize vs heuristic
    if optimizeTotalDifficulty:
        for term in range(len(TermDifficulty)):
            # add the constraint that the value of the TermDifficulty[i] must be the sum
            # of difficulty ratings for term [i]
            model.add(Minimize(Sum(TermDifficulty)))
    else:
        # if we have chosen not to optimize the difficulty, use a heuristic instead
        # we'll define the difficulty heuristic as a constraint that ensures no single term
        # is above a difficulty threshold, where a term's difficulty is the sum of the difficulties
        # of the courses scheduled for that term
        # the user is allowed to configure this threshold from the UI, with 5 options:
        #    very easy:     total term difficulty <= 5 NOTE: removed as an option, infeasible for a full-time student
        #         easy:     total term difficulty < 7.5
        #        medium:    total term difficulty <= 10
        #        hard:      total term difficulty < 12.5
        #      very hard:    total term difficulty <= 15
        maxDifficulty = 0
        #if difficultyThreshold == "very easy":
        #    maxDifficulty = 5
        if difficultyThreshold == "easy":
            maxDifficulty = 7
        elif difficultyThreshold == "medium":
            maxDifficulty = 10
        elif difficultyThreshold == "hard":
            maxDifficulty = 12
        elif difficultyThreshold == "very hard":
            maxDifficulty = 15
        else:
            maxDifficulty = 10 # default to 'medium' if difficultyThreshold is malformed
        
        for term in range(1, 20):
            model.add(TermDifficulty[term] <= maxDifficulty)
    
    # Solve the Model
    msolver = model.load('Mistral', courseTerms)
    debug_print("Solving...")
    starttime = datetime.now()
    msolver.solve()
    endtime = datetime.now()
    elapsed = endtime - starttime
    #print "Solution took " + str(elapsed)
     
    # debug_print final solution
    #@TODO: this will eventually be formatted output for the php ui script to read       
    outputter = Outputter(major, courseTerms, TermDifficulty, msolver)
    outputter.outputXML()
    #outputter.printSchedule()

# Parse command-line args from PHP script or other source
# argv[1] = major
# argv[2] = max units per term
# argv[3] = difficultyThreshold (from: "easy", "medium", "hard", "very hard")
# argv[4] = minimize_time to minimize time to completion, false otherwise  (takes forever)
# argv[5] = minimize_difficulty to minimize total difficulty, false otherwise  (takes forever)
# argv[6..n] = course preferences, each additional argument must be a valid course code for the
#                provided major, and will be included in the final schedule

if len(sys.argv) > 1:
    selectedMajor = sys.argv[1]

if len(sys.argv) > 2:
    max_term_units = int(sys.argv[2])

if len(sys.argv) > 3:
    difficultyThreshold = sys.argv[3]
    
if len(sys.argv) > 4:
    if sys.argv[4] == "minimize_time":
        optimizeTimeToCompletion = True
    else:
        optimizeTimeToCompletion = False
        
if len(sys.argv) > 5:
    if sys.argv[5] == "minimize_difficulty":
        optimizeTotalDifficulty = True
    else:
        optimizeTotalDifficulty = False

if len(sys.argv) > 6:
    for i in range(6, len(sys.argv)):
        courseCode = sys.argv[i]
        preferredCourses.append(courseCode)

# Generate a proposed schedule for selected major, or ics if none specified
generateSchedule(selectedMajor, max_term_units, preferredCourses)

