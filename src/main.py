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
    
    
    max_terms = 15 #might need to change/implement differently
    term_course_load_limit = 4
    total_classes = len(allCourses)
    print "Total # of classes: " + str(total_classes)
    scheduled = VarArray(total_classes, 0, max_terms)
    
    model = Model()
    
    # add constraint that all courses scheduled before max_terms
    model.add([ scheduled[c] <= max_terms for c in scheduled ])
    
    for i in range(len(courseGroups)):
        courseGroup = courseGroups[i]
        numCoursesRequired = courseGroup.numCoursesRequired
        courses = courseGroup.courses
        print str(courses)
        courseLength = len(courses)
        print courseLength
        
        # initialize variable array for this group
        courseVariables = VarArray(len(courses), 0, max_terms)
        
        #current_scheduled_length = len(scheduled)
        #for c in courses:
        #    newClass = Variable(0, max_terms)
        #    scheduled.append(newClass)
            
        #model.add([ sum((scheduled[course]>0) for course in range(len(courses)))>=numCoursesRequired ])
        
        # add constraint for each courseGroup
        model.add([ sum((courseVariables[course]>0) for course in range(len(courses)))>=int(numCoursesRequired) ])
    
    for term in range(max_terms):
        # add constraint for each term that "course_load_limit" not exceeded
        model.add([ sum((scheduled[course_c] == term) for course_c in range(total_classes))<=term_course_load_limit ])
        print "Sum of scheduled[i] == " + str(term) + " for i in range " + str(total_classes) + " <= " + str(term_course_load_limit)
        
    # TODO #
    # add prereqs contraint
    # add minimum total units constraint
    # add "course offering" constraints
    
    #return model;
    msolver = Mistral.Solver(model)
    
    print "Solving..."
    starttime = datetime.now()
    msolver.solve()
    endtime = datetime.now()
    elapsed = endtime - starttime
    print "Solution took " + str(elapsed)

    print scheduled
    
def print_courses(courses):
    for i in range(len(courses)):
        print "Course %d: %d" %(i, courses[i])


model_courses('ics')