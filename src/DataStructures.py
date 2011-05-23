'''
@author: preston
'''

#import XML parsing packages from python standard library
import xml.dom.minidom

# Documentation
#
# Class Course
#    Fields
#        title            (human readable pretty title)
#        courseCode       (formal course code)
#        units            (number of units for this course)
#        prereqs          (a list of course codes that represent prerequisite courses)
#                         NOTE: you can access Course objects by using major.getCourse(courseCode)
#        offerings        a list of terms when this course is offered (@TODO: IMPLEMENT THIS)
#
#    Methods
#        <none>
#
# Class CourseGroup
#    Fields
#        title                 (human readable pretty title)
#        numCoursesRequired    (min number of courses that must be taken from this group)
#        courses               (list of courses in this group)
#
#        Methods
#            <none>
#
# Class Major
#    Fields
#        title            (human readable pretty title)
#        minUnits         (minimum cumulative units required for major)
#        courseGroups     (list of course groups for this major)
#        courses          (an internal dictionary of courses that maps course codes to instances
#                          of course objects)
#                         NOTE: use major.getCourse(courseCode) to get a course instance by its code
#
#    Methods
#        STATIC getMajor(majorName)
#            loads and returns an instance of 'Major' for the given major name (cse, cs, ics, in4matx)
#            automatically handles xml parsing from file
#        
#        getCourse(courseCode)
#            returns an instance of 'Course' for the given course code in the major

class Course:
    """Defines a course"""
    
    def __init__(self):
        print "Initializing course..."
        self.prereqs = []
        self.units = 0
        self.courseCode = ""
        self.offerings = []
        self.title = ""
        
class CourseGroup:
    """Defines a requirement group for a major, created by a Major object"""
    
    def __init__(self):
        print "Initializing course group..."
        self.title = ""
        self.numCoursesRequired = 0
        self.courses = []

class Major:
    """Class for holding information for a given major, initialized with XML file"""
    
    def __init__(self):
        print "Initializing major..."
        self.title = ""
        self.minUnits = []
        self.courses = dict()
        self.courseGroups = []
        
    def getCourse(self, courseCode):
        return self.courses[courseCode]
        
    @staticmethod
    def getMajor(majorName):
        major = Major()
        if(majorName.lower() == "ics"):
            print "Loading XML File ICSMajor.xml"
            xmldoc = xml.dom.minidom.parse("../ICSMajor.xml")
            
            majorTitleNode = xmldoc.getElementsByTagName("major_title")
            minUnitsNode = xmldoc.getElementsByTagName("min_units")
            courseGroupNode = xmldoc.getElementsByTagName("groups")
            courseGroupNodes = courseGroupNode[0].getElementsByTagName("course_group")
            
            major.title = majorTitleNode[0].firstChild.nodeValue
            major.minUnits = minUnitsNode[0].firstChild.nodeValue
            
            print "Major name: " + major.title
            print "Min units: " + major.minUnits
            print "Parsing "+str(len(courseGroupNodes))+" required course groups..."
            
            for node in courseGroupNodes:
                print ""
                courseGroup = CourseGroup()
                courseGroupTitleNode = node.getElementsByTagName("title")
                courseGroupNumRequiredNode = node.getElementsByTagName("num_courses_required")
                coursesNode = node.getElementsByTagName("courses")
                coursesNodes = coursesNode[0].getElementsByTagName("course")
                
                courseGroup.title = courseGroupTitleNode[0].firstChild.nodeValue
                courseGroup.numCoursesRequired = courseGroupNumRequiredNode[0].firstChild.nodeValue
                major.courseGroups.append(courseGroup)
                
                print "Course Group: " + courseGroup.title
                print "Minimum Required: " + courseGroup.numCoursesRequired
                print "Parsing " + str(len(coursesNodes)) + " courses in group..."
                
                for courseNode in coursesNodes:
                    print "----------"
                    course = Course()
                    print "DEBUG: " + str(course.prereqs)
                    courseTitleNode = courseNode.getElementsByTagName("title")
                    courseUnitNode = courseNode.getElementsByTagName("units")
                    courseCodeNode = courseNode.getElementsByTagName("code")
                    coursePrereqsNode = courseNode.getElementsByTagName("prereqs")
                    coursePrereqsNodes = coursePrereqsNode[0].getElementsByTagName("course_code")
                    
                    course.title = courseTitleNode[0].firstChild.nodeValue
                    course.units = courseUnitNode[0].firstChild.nodeValue
                    course.courseCode = courseCodeNode[0].firstChild.nodeValue
                    
                    for node in coursePrereqsNodes:
                        course.prereqs.append(node.firstChild.nodeValue)
                    
                    print "Course : " + course.title
                    print "Code: " + course.courseCode
                    print "Units: " + course.units
                    print "Prereqs: " + str(course.prereqs)
                    
                    courseGroup.courses.append(course)
                    
                    major.courses[course.courseCode] = course
                    
            print "ALL COURSES IN MAJOR:"
            for key in major.courses.keys():
                print key + ": " + str(major.courses[key])
            
                    
        print "Successfully initialized major " + major.title
        return major


Major.getMajor('ics')
        
