
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
                      "advanced": ("Advanced maths exam", 40, ['+', '-', '*', '/']) }
    
    def get_exam_list(self):
        """Returns a list of available exams"""
        return self.exams.keys()
    
    def get_label(self, exam_id):
        return self.exams[exam_id][0]  #exam label is first element in tuple
    

#    def challenge_complete(self, challenge_name):
#        repo = ChallengeRepo()
#        result = repo.get_result(BUNDLE_ID, challenge_name)
#        result.set_result(True)
#        repo.set_result(BUNDLE_ID, challenge_name, result)
        
        
    
    
