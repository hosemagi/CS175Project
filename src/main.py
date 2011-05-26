###########################
# main.py
# Group 6: Academic Planner
###########################

from datetime import datetime
from Numberjack import *
import Mistral
import DataStructures

# creates and solves a model for a given major
def model_courses(majorName):
    newMajor = DataStructures.Major.getMajor(majorName)
    majorTitle = newMajor.title
    print "Major: " + majorTitle
    minUnits = newMajor.minUnits
    print "Minimum units: " + str(minUnits)
    courseGroups = newMajor.courseGroups
    allCourses = newMajor.courses
    
    
    max_terms = 7 #might need to change/implement differently
    term_course_load_limit = 4
    total_classes = len(allCourses)
    print "Total # of classes: " + str(total_classes)
    scheduled = VarArray(total_classes, 0, max_terms)
    
    courseGroupSolutions = []
    
    model = Model()
    
    for i in range(len(courseGroups)):
        courseGroup = courseGroups[i]
        numCoursesRequired = courseGroup.numCoursesRequired
        courses = courseGroup.courses
        
        # initialize variable array for this group
        courseVariables = dict()
        courseCodes = []
        courseGroupSolutions.append(courseVariables)
        
        for j in courses:
            courseVariables[j.courseCode] = Variable(0, max_terms)
            courseCodes.append(j.courseCode)
            prereqs = j.prereqs
            #for k in prereqs
        
        # add constraint for each courseGroup
        #model.add(sum((courseVariables[course]>0) for course in range(len(courses)))>=int(numCoursesRequired))    
        model.add([ sum((courseVariables[code]>0) for code in courseCodes)>=int(numCoursesRequired) ])
    
    # must not exceed unit limit for a single term
    #for term in range(1, max_terms):
    #     model.add( sum([[sum((courseGroupSolutions[i] == term) for i in range(len(courseVariables)))] for courseVariables in courseGroupSolutions ] ) < 4) 
    
    # TODO #
    # add prereqs contraint
    # add minimum total units constraint
    # add "course offering" constraints
    
    #return model;
    msolver = Mistral.Solver(model)
    print scheduled
    print "Solving..."
    starttime = datetime.now()
    msolver.solve()
    endtime = datetime.now()
    elapsed = endtime - starttime
    print "Solution took " + str(elapsed)

    print "\n\nDISPLAYING COURSE SELECTION FOR MAJOR " + newMajor.title

    for i in range(len(courseGroupSolutions)):
        print "\n############################"
        print "Classes for course group: " + newMajor.courseGroups[i].title
        for k, j in courseGroupSolutions[i].items():
            print str(k) + ": " + str(j)
        
def print_courses(courses):
    for i in range(len(courses)):
        print "Course %d: %d" %(i, courses[i])


model_courses('ics')