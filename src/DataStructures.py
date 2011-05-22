#import XML parsing packages from python standard library
import xml.dom.minidom

class Course:
    """Defines a course"""
    
    title = ""
    courseCode = ""
    units = 0
    prereqs = []
    offerings = []
    
    def __init__(self):
        print "Initializing course..."
        
class CourseGroup:
    """Defines a requirement group for a major, created by a Major object"""
    
    title = ""
    numCoursesRequired = 0
    courses = []
    
    def __init__(self):
        print "Initializing course group..."

class Major:
    """Class for holding information for a given major, initialized with XML file"""
    
    title = ""
    minUnits = 0
    courseGroups = []
    courses = dict()
    
    
    def __init__(self):
        print "Initializing major..."
        
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
                    courseTitleNode = courseNode.getElementsByTagName("title")
                    courseUnitNode = courseNode.getElementsByTagName("units")
                    courseCodeNode = courseNode.getElementsByTagName("code")
                    coursePrereqsNode = courseNode.getElementsByTagName("prereqs")
                    coursePrereqsNodes = coursePrereqsNode[0].getElementsByTagName("course_code")
                    
                    course.title = courseTitleNode[0].firstChild.nodeValue
                    course.units = courseUnitNode[0].firstChild.nodeValue
                    course.courseCode = courseCodeNode[0].firstChild.nodeValue
                    
                    for courseCodeNode in coursePrereqsNodes:
                        course.prereqs.append(courseCodeNode.firstChild.nodeValue)
                    
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
        
