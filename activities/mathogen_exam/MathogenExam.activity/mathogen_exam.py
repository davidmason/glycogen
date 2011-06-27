
import gtk
import gobject
import random

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
        # value tuples are: exam label,
        #                   number of questions,
        #                   maximum value for questions,
        #                   list of operators for questions
        self.exams = {"easy": ("Beginner maths exam", 20, 10, ['+', '-']),
                      "intermediate": ("Intermediate maths exam", 30, 20, ['+', '-', '*']),
                      "advanced": ("Advanced maths exam", 40, 30, ['+', '-', '*', '/']) }
        
        self._problems = None
        self.current_problem = None
    
    def get_exam_list(self):
        """Returns a list of available exams"""
        return self.exams.keys()
    
    def get_label(self, exam_id):
        return self.exams[exam_id][0]  #exam label is first element in tuple
    
    def start_exam(self, exam_id):
        """Generates exam questions based on the given exam id.
        
        Use get_problem() to retrieve the current question.
        Use answer_count() to get the number of questions answered
        Use correct_count() to get the number of questions answered correctly
        Use question_count() to get the total number of questions
            in the current exam.
        
        returns: True if a problem is loaded
                 False if there are no problems available (empty exam)
        """
        
        self.answers = 0
        self.correct = 0
        self.questions = self.exams[exam_id][1]
        
        self._problems = []
        
        limit = self.exams[exam_id][2]
        operators = self.exams[exam_id][3]
        
        for question_num in range(self.questions):
            operator = operators[question_num%len(operators)]
            self._problems.append(SimpleMathProblem(operator, limit))
        
        return self._next_problem()
    
    def _next_problem(self):
        """Loads the next problem from the list.
        
        returns: True if a new problem was loaded,
                 False if there were no more problems to load
                 and current problem has been set to None
        
        """
        try:
            self._current_problem = self._problems.pop()
            return True
        except IndexError:
            self._current_problem = None
            return False
    
    def get_problem(self):
        return self._current_problem
    
    def answer_count(self):
        return self.answers
    
    def correct_count(self):
        return self.correct
    
    def question_count(self):
        return self.questions
    
    
    def try_answer(self, answer):
        """Checks the user's answer and advances to the next problem,
        which may be None if the exam is finished.
        
        returns: True if the answer was correct,
                 False otherwise
        """
        
        self.answers += 1
        correct = (answer == self._current_problem.answer)
        if correct:
            self.correct += 1
        self._next_problem()
        return correct
            
            
    
#    def challenge_complete(self, challenge_name):
#        repo = ChallengeRepo()
#        result = repo.get_result(BUNDLE_ID, challenge_name)
#        result.set_result(True)
#        repo.set_result(BUNDLE_ID, challenge_name, result)
        
        
class SimpleMathProblem():
    """Represents an addition/subtraction/multiplication/division problem.
    
    operator must be one of '+', '-', '*', '/'
    limit determines the maximimum number that can show up in the problem.
    
    The components of the problem can be accessed as 'operator',
    'operand1', 'operand2' and 'answer'
    
    """
    
    def _init_sum(self, limit):
        # set this problem up as a sum
        self.operator = '+'
        self.operand1 = random.randint(0, limit/2)
        self.operand2 = random.randint(0, limit/2)
        self.answer = self.operand1 + self.operand2
        
    
    def _init_difference(self, limit):
        # set this problem up as a difference
        self.operator = '-'
        self.operand1 = random.randint(0, limit)
        self.operand2 = random.randint(0, self.operand1)
        self.answer = self.operand1 - self.operand2
    
    def _init_product(self, limit):
        # set this problem up as a product
        self.operator = '*'
        self.operand1 = random.randint(1, limit/2)
        self.operand2 = random.randint(0, limit/self.operand1)
        self.answer = self.operand1 * self.operand2
    
    def _init_quotient(self, limit):
        # set this problem up as a quotient
        self.operator = '/'
        
        # this is the most complicated, since I want whole numbers
        # first we need to generate a non-prime (so it can be divided)
        non_primes = filter(lambda x: not all(x%i for i in xrange(2, x)) , range(1, limit))
        if not non_primes:
            non_primes.append(limit) # here we just use limit if there are no primes
        # select a random 'non-prime' from the list
        self.operand1 = random.choice(non_primes)
        
        # then we need to randomly select one of its factors
        factors = filter(lambda x: self.operand1 % x == 0 , range(1, self.operand1))
        self.operand2 = random.choice(factors)
        
        self.answer = self.operand1 / self.operand2

    
    def __init__(self, operator, limit=20):
        # limit determines the maximum answer for addition and multiplication
        # or the maximum operand for subtraction and division
        
        _init_functions = {'+': self._init_sum,
                           '-': self._init_difference, 
                           '*': self._init_product,
                           '/': self._init_quotient}
        if (operator in _init_functions):
            _init_functions[operator](limit)
        #else:
            # TODO: the wrong operator was passed. Throw an error or something
    
