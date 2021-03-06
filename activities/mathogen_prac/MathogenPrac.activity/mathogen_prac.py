
import gtk
import gobject
import random
from time import sleep

#TODO build infrastructure to be able to handle challenges when bundle is first added
from glycogen.challenge import challrepo
from glycogen.challenge.challrepo import Challenge, Result

from glycogen.challenge.result import ge_success_func


BUNDLE_ID = 'org.davidmason.mathogen_prac'



challenges = { "add_16": Challenge(BUNDLE_ID, "add_16",
                                   "Answer {target} addition questions correctly during a session",
                                   Result(16, ge_success_func)),
               "subtract_16": Challenge(BUNDLE_ID, "subtract_16",
                                   "Answer {target} subtraction questions correctly during a session",
                                   Result(16, ge_success_func)),
               "multiply_16": Challenge(BUNDLE_ID, "multiply_16",
                                   "Answer {target} multiplication questions correctly during a session",
                                   Result(16, ge_success_func)),
               "divide_16": Challenge(BUNDLE_ID, "divide_16",
                                   "Answer {target} division questions correctly during a session",
                                   Result(16, ge_success_func)) }

operatorchallenge = { '+': "add_16",
                      '-': "subtract_16",
                      '*': "multiply_16",
                      '/': "divide_16" }


class MathogenPrac():
    """A mathogen practice game, which generates simple mathematics problems
    and keeps track of answers and progress towards a goal number of correct
    answers.

    """
    
    def __init__(self, howMany=20):
        # initialise the counts for correct and incorrect for each operator
        # let's store them in maps for fun, then we can reuse the methods
        # that look them up and compare ratios
        
        # number of correct and incorrect answers:
        self._correct = { '+': 0, '-': 0, '*': 0, '/': 0}
        self.__incorrect = { '+': 0, '-': 0, '*': 0, '/': 0}
        self._target = howMany
        self.new_problem('+') #starts with a default addition problem
    
    def check_achievements(self, operator):
        challenge_id = operatorchallenge[operator]
        repo = challrepo.get_global_repository()
        result = repo.get_result(BUNDLE_ID, challenge_id)
        if result.get_result() is not None:
            if (result.get_result() >= self._correct[operator]):
                return  #higher result already recorded
        
        result.set_result(self._correct[operator])
        repo.set_result(BUNDLE_ID, challenge_id, result)
        
    
    def get_progress(self):
        """Returns a float representing the proportion of the target number
        of answers that have been answered correctly.
        """

        correct = sum([i for i in self._correct.values()])
        return float(correct) / float(self._target)

    
    def new_problem(self, operator):
        """Generates a new maths problem.
        
        Opeartor can be one of '+', '-', '*', '/'
        The numbers, operator and answer can then be retrieved
        from the problem, which is retrieved using getProblem().

        """
        
        self.currentProblem = SimpleMathProblem(operator, 20)
        return self.currentProblem
        
    def try_answer(self, answer):
        """Checks the user's answer to the current problem to see if it is
        correct, and records the result in the appropriate answer count.

        """

        if (answer == self.currentProblem.answer):
            self._correct[self.currentProblem.operator] += 1
            self.check_achievements(self.currentProblem.operator)
            return True
        else:
            self.__incorrect[self.currentProblem.operator] += 1
            return False
        

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
    
