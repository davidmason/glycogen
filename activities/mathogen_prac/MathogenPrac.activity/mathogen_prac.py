
import gtk
import gobject
import random
from time import sleep


class MathogenPrac():
    """A mathogen practice game, which generates simple mathematics problems
    and keeps track of answers and progress towards a goal number of correct
    answers.

    """
    
    def __init__(self, howMany=15):
        # initialise the counts for correct and incorrect for each operator
        # let's store them in maps for fun, then we can reuse the methods
        # that look them up and compare ratios
        
        # number of correct and incorrect answers:
        self._correct = { '+': 0, '-': 0, '*': 0, '/': 0}
        self.__incorrect = { '+': 0, '-': 0, '*': 0, '/': 0}
        self._target = howMany
        self.new_problem('+') #starts with a default addition problem
    
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
    
