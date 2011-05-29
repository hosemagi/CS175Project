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


# writes results as JSON objects to output stream for use by UI
def outputScheduleJSON(major, courseTerms, solver):
    return 1