class Major:
    """Class for holding information for a given major, initialized with XML file"""
    
    title = ""
    min_units = 0
    courseGroups = []
    
    
    def __init__(self, XMLFilepath):
        print "Initializing major with XML file " + XMLFilepath + "..."
        
class CourseGroup:
    """Defines a requirement group for a major, created by a Major object"""
    
    title = ""
    numCoursesRequired = 0
    courses = []
    
    def __init__(self):
        print "Initializing course group..."
        
class Course:
    """Defines a course"""
    
    title = ""
    courseCode = ""
    units = 0
    prereqs = []
    offerings = []
    
    def __init__(self):
        print "Initializing course..."