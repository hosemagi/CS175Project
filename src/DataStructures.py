###########################
# DataStructures.py
# Group 6: Academic Planner
###########################

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
#        scheduledTerm    
# 
#        diff            Difficulty Rating either 1,2 or 3 
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

silent = True

def debug_print(msg):
    if not silent:
        print msg

class Course:
    """Defines a course"""
    
    def __init__(self):
        debug_print("Initializing course...")
        self.prereqs = []
        self.units = 0
        self.courseCode = "NoCode"
        self.offerings = []
        self.title = "NoTitle"
        self.scheduledTerm = 0
        self.index = -1
        self.diff  = -1
        
class CourseGroup:
    """Defines a requirement group for a major, created by a Major object"""
    
    def __init__(self):
        debug_print("Initializing course group...")
        self.title = ""
        self.numCoursesRequired = 0
        self.courses = []
        self.startIndex = 0

class Major:
    """Class for holding information for a given major, initialized with XML file"""
    
    def __init__(self):
        debug_print("Initializing major...")
        self.title = ""
        self.minUnits = []
        self.courseDict = dict()
        self.courses = []
        self.courseGroups = []
        
    def getCourse(self, courseCode):
        return self.courseDict[courseCode]
    
    def getCourseIndex(self, courseCode):
        return self.courses.index(self.courseDict[courseCode])
        
    @staticmethod
    def getMajor(majorName):
        foundDuplicate = False
        major = Major()
        if(majorName.lower() == "ics"):
            debug_print("Loading XML File ICSMajor.xml")
            xmldoc = xml.dom.minidom.parse("../ICSMajor.xml")
        elif(majorName.lower() == "cs"):
            debug_print("Loading XML File CSMajor.xml")
            xmldoc = xml.dom.minidom.parse("../CSMajor.xml") 
        elif(majorName.lower() == "cse"):
            debug_print("Loading XML File CSEMajor.xml")
            xmldoc = xml.dom.minidom.parse("../CSEMajor.xml") 
        elif(majorName.lower() == "informatics"):
            debug_print("Loading XML File INFORMATICSMajor.xml")
            xmldoc = xml.dom.minidom.parse("../INFORMATICSMajor.xml") 
            
        majorTitleNode = xmldoc.getElementsByTagName("major_title")
        minUnitsNode = xmldoc.getElementsByTagName("min_units")
        courseGroupNode = xmldoc.getElementsByTagName("groups")
        courseGroupNodes = courseGroupNode[0].getElementsByTagName("course_group")
        
        major.title = majorTitleNode[0].firstChild.nodeValue
        major.minUnits = minUnitsNode[0].firstChild.nodeValue
        
        debug_print("Major name: " + major.title)
        debug_print("Min units: " + major.minUnits)
        debug_print("Parsing "+str(len(courseGroupNodes))+" required course groups...")
        
        index = 0
        for node in courseGroupNodes:
            debug_print("")
            courseGroup = CourseGroup()
            courseGroupTitleNode = node.getElementsByTagName("title")
            courseGroupNumRequiredNode = node.getElementsByTagName("num_courses_required")
            coursesNode = node.getElementsByTagName("courses")
            coursesNodes = coursesNode[0].getElementsByTagName("course")
            
            courseGroup.title = courseGroupTitleNode[0].firstChild.nodeValue
            courseGroup.numCoursesRequired = courseGroupNumRequiredNode[0].firstChild.nodeValue
            major.courseGroups.append(courseGroup)
            
            courseGroup.startIndex = index
            
            debug_print("Course Group: " + courseGroup.title)
            debug_print("Minimum Required: " + courseGroup.numCoursesRequired)
            debug_print("Parsing " + str(len(coursesNodes)) + " courses in group...")
            
            for courseNode in coursesNodes:
                debug_print("----------")
                course = Course()
                courseTitleNode = courseNode.getElementsByTagName("title")
                courseUnitNode = courseNode.getElementsByTagName("units")
                courseCodeNode = courseNode.getElementsByTagName("code")
                coursePrereqsNode = courseNode.getElementsByTagName("prereqs")
                coursePrereqsNodes = coursePrereqsNode[0].getElementsByTagName("course_code")
                courseOfferingsNode = courseNode.getElementsByTagName("offerings")
                courseOfferingsNodes = courseOfferingsNode[0].getElementsByTagName("term_id")
                courseDiffNode = courseNode.getElementsByTagName("diff")
                
                course.title = courseTitleNode[0].firstChild.nodeValue
                course.units = courseUnitNode[0].firstChild.nodeValue.encode('utf-8')
                course.courseCode = courseCodeNode[0].firstChild.nodeValue
                course.diff  = courseDiffNode[0].firstChild.nodeValue.encode('utf-8')
                course.index = index
                index += 1
                
                for courseCodeNode in coursePrereqsNodes:
                    course.prereqs.append(courseCodeNode.firstChild.nodeValue)
                
                for courseOfferingNode in courseOfferingsNodes:
                    course.offerings.append(courseOfferingNode.firstChild.nodeValue.encode('utf-8'))
                
                debug_print("Course : " + course.title)
                debug_print("Code: " + course.courseCode)
                debug_print("Units: " + course.units)
                debug_print("Prereqs: " + str(course.prereqs))
                debug_print("Difficulty: " +str(course.diff))
                
                major.courses.append(course)
                courseGroup.courses.append(course)
                
                if(major.courseDict.has_key(course.courseCode)):
                    debug_print("DUPLICATE: " + course.courseCode)
                    foundDuplicate = True
                major.courseDict[course.courseCode] = course
                    
        debug_print("\n\nALL COURSES IN MAJOR:")
        for i in range(len(major.courses)):
            debug_print(major.courses[i].courseCode + ": " + str(i))
            
                    
        debug_print("Successfully initialized major " + major.title)
        debug_print(str(len(major.courses)) + " courses")
        if foundDuplicate:
            debug_print("Found at least one duplicated course, check output")
        return major

#Major.getMajor('ics')
