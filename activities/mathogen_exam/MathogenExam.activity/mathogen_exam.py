
import gtk
import gobject

from glycogen.challenge.challrepo import ChallengeRepo, Challenge, Result
from glycogen.challenge.result import ge_success_func


BUNDLE_ID = 'org.davidmason.mathogen_exam'

#TODO change to exam challenges
#challenges = { "add": Challenge(BUNDLE_ID, "add",
#                                   "Read to the last page of the Addition Tutorial",
#                                   Result(True, equals_success_func)),
#               "subtract": Challenge(BUNDLE_ID, "subtract",
#                                   "Read to the last page of the Subtraction Tutorial",
#                                   Result(True, equals_success_func)),
#               "multiply": Challenge(BUNDLE_ID, "multiply",
#                                   "Read to the last page of the Multiplication Tutorial",
#                                   Result(True, equals_success_func)),
#               "divide": Challenge(BUNDLE_ID, "divide",
#                                   "Read to the last page of the Division Tutorial",
#                                   Result(True, equals_success_func)) }


class MathogenExam():
    """Encapsulates a set of tutorial pages that can be displayed."""
    
    def __init__(self):
        self.exams = {"easy": ("Beginner maths exam", 20, ['+', '-']),
                      "intermediate": ("Intermediate maths exam", 30, ['+', '-', '*']),
                      "advanced": ("Intermediate maths exam", 40, ['+', '-', '*', '/']) }
#        self.tutorials = {"Addition Tutorial": 3,
#                          "Subtraction Tutorial": 3,
#                          "Multiplication Tutorial": 3,
#                          "Division Tutorial": 3 }
    
    def get_exam_list(self):
        """Returns a list of available tutorials"""
        return self.exams.keys()
    
    def get_label(self, exam_id):
        return self.exams[exam_id][0]
    
    def page_count(self, tutorial_name):
        return self.tutorials[tutorial_name]
    
    def get_page(self, tutorial_name, page_number):
        return self.build_page(tutorial_name, page_number)

    def build_page(self, tutorial, page_no):
        if tutorial == "Addition Tutorial":
            if page_no is 0:
                page = gtk.VBox(False, 0)
                para = "Addition tutorial intro page\nThese just have stub content for now."
                label = gtk.Label(para)
                label.show()
                page.pack_start(label, True, True, 0)
                page.show()
                return page
        
            if page_no is 1:
                page = gtk.Label("Addition tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Addition tutorial last page")
                page.show()
                self.challenge_complete("add")
                return page
        
        if tutorial == "Subtraction Tutorial":
            if page_no is 0:
                page = gtk.Label("Subtraction tutorial intro page")
                page.show()
                return page
                
            if page_no is 1:
                page = gtk.Label("Subtraction tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Subtraction tutorial last page")
                page.show()
                self.challenge_complete("subtract")
                return page
                
        if tutorial == "Multiplication Tutorial":
            if page_no is 0:
                page = gtk.Label("Multiplication tutorial intro page")
                page.show()
                return page
                
            if page_no is 1:
                page = gtk.Label("Multiplication tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Multiplication tutorial last page")
                page.show()
                self.challenge_complete("multiply")
                return page
                
        if tutorial == "Division Tutorial":
            if page_no is 0:
                page = gtk.Label("Division tutorial intro page")
                page.show()
                return page
                
            if page_no is 1:
                page = gtk.Label("Division tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Division tutorial last page")
                page.show()
                self.challenge_complete("divide")
                return page
                
        
        
        #return error label if not a valid tutorial and page
        page = gtk.Label("Page number or tutorial not valid")
        page.show()
        return page
        
        
        
    def challenge_complete(self, challenge_name):
        repo = ChallengeRepo()
        result = repo.get_result(BUNDLE_ID, challenge_name)
        result.set_result(True)
        repo.set_result(BUNDLE_ID, challenge_name, result)
        
        
    
    
