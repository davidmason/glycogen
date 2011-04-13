from sugar.activity import activity
import logging

import sys, os
import gtk
import random

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class MathogenPracGui(activity.Activity):
    
    # weight can be something like pango.WEIGHT_BOLD 
    def _setFontParams(self, widget, scale=None, weight=None):
        context = widget.get_pango_context()
        font = context.get_font_description()
        if scale is not None:
            font.set_size(int(font.get_size() * scale))
        if weight is not None:
            font.set_weight(weight)
        widget.modify_font(font)
    
    def tryAnswer(self, widget, data=None):
        userInput = self.answer.get_text()
        
        if (len(userInput) == 0):
            self.hintmessage.set_text("You didn't enter an answer yet")
        if (not is_int(userInput)):
            self.hintmessage.set_text("Your input doesn't look like a number")
        if (self._practice.tryAnswer(int(userInput))):
            self.hintmessage.set_text("That's right!")
            # also get a new problem
            #TODO need to get the operator from the buttons
            self.showProblem(self._practice.newProblem('+'))
        else:
            self.hintmessage.set_text("So close! Try again.")
            self.answer.grab_focus()
            # could make a function that takes the suggested and actual answer and generates a message
    
    def __init__(self, handle):
        # This runs the constructor for an activity
        activity.Activity.__init__(self, handle)
        
        #TODO this code could possibly be more readable by separating it into functions
        
        operator_button_text_scale = 4
        challenge_text_scale = 7
        
        # Creates the Toolbox. It contains the Activity Toolbar, which is the
        # bar that appears on every Sugar window and contains essential
        # functionalities, such as the 'Collaborate' and 'Close' buttons.
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()
        
        # Create the main layout window that will have 3 sections
        self.layout = gtk.VBox(False, 0)
        self.set_canvas(self.layout)
        
        # Section 1: topbar
        # holds 4 buttons that change the mode, and a hint message label
        self.topbar = gtk.HBox(False, 0)
        
        # create contents for topbar
        self.button_add = gtk.Button("+")
        self.button_subtract = gtk.Button("-")
        self.button_multiply = gtk.Button("x")
        self.button_divide = gtk.Button("/") #TODO try to add a division sign
        self.hintmessage = gtk.Label("this label will say how close your answer is (e.g. 'so close!')")
        
        # increase font size
        self._setFontParams(self.button_add, scale=operator_button_text_scale)
        self._setFontParams(self.button_subtract, scale=operator_button_text_scale)
        self._setFontParams(self.button_multiply, scale=operator_button_text_scale)
        self._setFontParams(self.button_divide, scale=operator_button_text_scale)
        
        # pack contents into topbar
        self.topbar.pack_start(self.button_add, False, False, 5)
        self.topbar.pack_start(self.button_subtract, False, False, 5)
        self.topbar.pack_start(self.button_multiply, False, False, 5)
        self.topbar.pack_start(self.button_divide, False, False, 5)
        self.topbar.pack_end(self.hintmessage, False, False, 5)
        
        # Section 2: challenge
        # holds a table that shows the sum and hint, as well as the answer entry
        self.challenge = gtk.Table(rows=2, columns=6, homogeneous=False)
        self.challenge.set_col_spacing(column=4, spacing=30)
        self.challenge.set_row_spacing(row=1, spacing=50)
        
        # top row is the problem/answer
        self.label_num1 = gtk.Label("0")
        self.label_operator = gtk.Label("%")
        self.label_num2 = gtk.Label("0")
        self.label_equals = gtk.Label("=")
        self.answer = gtk.Entry(3)
        self.button_go = gtk.Button("Go!")
        
        
        self._setFontParams(self.label_num1, scale=challenge_text_scale)
        self._setFontParams(self.label_operator, scale=challenge_text_scale)
        self._setFontParams(self.label_num2, scale=challenge_text_scale)
        self._setFontParams(self.label_equals, scale=challenge_text_scale)
        self._setFontParams(self.answer, scale=challenge_text_scale)
        self._setFontParams(self.button_go, scale=challenge_text_scale)
        
        self.challenge.attach(self.label_num1, 0, 1, 0, 1)
        self.challenge.attach(self.label_operator, 1, 2, 0, 1)
        self.challenge.attach(self.label_num2, 2, 3, 0, 1)
        self.challenge.attach(self.label_equals, 3, 4, 0, 1)
        self.challenge.attach(self.answer, 4, 5, 0, 1)
        self.challenge.attach(self.button_go, 5, 6, 0, 1)
        
        # bottom row is for the clue (hidden by default)
        self.label_num1_clue = gtk.Label("")
        self.label_operator_clue = gtk.Label("")
        self.label_num2_clue = gtk.Label("")
        self.label_equals_clue = gtk.Label("")
        self.label_answer_clue = gtk.Label("")
        self.button_clue = gtk.Button("?")
        
        self._setFontParams(self.label_num1_clue, scale=challenge_text_scale)
        self._setFontParams(self.label_operator_clue, scale=challenge_text_scale)
        self._setFontParams(self.label_num2_clue, scale=challenge_text_scale)
        self._setFontParams(self.label_equals_clue, scale=challenge_text_scale)
        self._setFontParams(self.label_answer_clue, scale=challenge_text_scale)
        self._setFontParams(self.button_clue, scale=challenge_text_scale)
        
        self.challenge.attach(self.label_num1_clue, 0, 1, 1, 2)
        self.challenge.attach(self.label_operator_clue, 1, 2, 1, 2)
        self.challenge.attach(self.label_num2_clue, 2, 3, 1, 2)
        self.challenge.attach(self.label_equals_clue, 3, 4, 1, 2)
        self.challenge.attach(self.label_answer_clue, 4, 5, 1, 2)
        self.challenge.attach(self.button_clue, 5, 6, 1, 2)
        
        
        # Section 3: racetrack
        # holds a display representing the student's progress
        self.racetrack = gtk.HBox(False, 0)
        
        # for now the racetrack is just a progress bar, but later it will use the
        # student's icon and move it towards a representation of a goal (possibly
        # a cupcake or something sugary or glycogeny)
        self.progress = gtk.ProgressBar()
        self.progress.set_text("Level 0")
        self.progress.set_fraction(0.5)
        
        self.racetrack.pack_start(self.progress, True, True, 0)
        
        # pack the 3 sections into the main layout
        self.layout.pack_start(self.topbar, False, False, 5)
        self.layout.pack_start(self.challenge, True, True, 30)
        self.layout.pack_start(self.racetrack, False, False, 0)
        
        
        # show all of topbar
        self.button_add.show()
        self.button_subtract.show()
        self.button_multiply.show()
        self.button_divide.show()
        self.hintmessage.show()
        self.topbar.show()
        
        # show all of challenge
        self.label_num1.show()
        self.label_operator.show()
        self.label_num2.show()
        self.label_equals.show()
        self.answer.show()
        self.button_go.show()
        
        self.label_num1_clue.show()
        self.label_operator_clue.show()
        self.label_num2_clue.show()
        self.label_equals_clue.show()
        self.label_answer_clue.show()
        self.button_clue.show()
        
        self.challenge.show()
        
        # show all of racetrack
        self.progress.show()
        self.racetrack.show()
        
        #show everything
        self.layout.show()
        
        
        self.button_go.connect("clicked", self.tryAnswer, None)
        self.answer.connect("activate", self.tryAnswer, None)
        
        # create a new MathogenPrac() to keep track of number of questions answered
        self._practice = MathogenPrac() #this should already have the first (addition) question answered
        
        self.showProblem(self._practice.currentProblem)
        
    def showProblem(self, prob):
        self.label_num1.set_text(str(prob.operand1))
        self.label_num2.set_text(str(prob.operand2))
        self.label_operator.set_text(prob.operator)
        self.answer.set_text("")
        self.answer.grab_focus()
        self.hintmessage.set_text("Try this one...")
        

class MathogenPrac():
    
    def __init__(self):
        # initialise the counts for correct and incorrect for each operator
        # let's store them in maps for fun, then we can reuse the methods
        # that look them up and compare ratios
        
        # number of correct and incorrect answers:
        self.__correct = { '+': 0, '-': 0, '*': 0, '/': 0}
        self.__incorrect = { '+': 0, '-': 0, '*': 0, '/': 0}
        self.newProblem('+') #starts with a default addition problem

    def newProblem(self, operator):
        """Generates a new maths problem.
        
        Opeartor can be one of '+', '-', '*', '/'
        The numbers, operator and answer can then be retrieved
        from the problem, which is retrieved using getProblem().
        """
        
        self.currentProblem = SimpleMathProblem(operator, 20)
        return self.currentProblem
        
    def tryAnswer(self, answer):
        if (answer == self.currentProblem.answer):
            self.__correct[self.currentProblem.operator] += 1
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
    
    def _initSum(self, limit):
        # set this problem up as a sum
        self.operator = '+'
        self.operand1 = random.randint(0, limit/2)
        self.operand2 = random.randint(0, limit/2)
        self.answer = self.operand1 + self.operand2
        
    
    def _initDifference(self, limit):
        # set this problem up as a difference
        self.operator = '-'
        self.operand1 = random.randint(0, limit)
        self.operand2 = random.randint(0, self.operand1)
        self.answer = self.operand1 - self.operand2
    
    def _initProduct(self, limit):
        # set this problem up as a product
        self.operator = '*'
        self.operand1 = random.randint(0, limit/2)
        self.operand2 = random.randint(0, limit/self._operand1)
        self.answer = self.operand1 * self.operand2
    
    def _initQuotient(self, limit):
        # set this problem up as a quotient
        self.operator = '/'
        
        # this is the most complicated, since I want whole numbers
        # first we need to generate a non-prime (so it can be divided)
        nonPrimes = _getNonPrimes(limit)
        if (len(nonPrimes) == 0):
            nonPrimes.append(limit) # here we just use limit if there are no primes
        # select a random 'non-prime' from the list
        self.operand1 = random.choice(nonPrimes)
        
        # then we need to randomly select one of its factors
        factors = filter(lambda x: self.operand1 % x == 0 , range(1, self.operand1))
        self.operand2 = random.choice(factors)
        
        self.answer = self._operand1 / self._operand2
    
#    def _notPrime(num): return !all(num % i for i in xrange(2, num))
    
    def _getNonPrimes(self, limit):
        # this will return all the non-primes up to limit
        # filter(_notPrime, range(0, limit))
        
        # equivalent with lambda function (delete _notPrime() if this works)
        # in fact just use this inline if it works, since it's only needed once
        return filter(lambda x: not all(x%i for i in xrange(2, x)) , range(1, limit))
        
    def _getFactors(self, number):
        # this will return 1 and number, as well as any other factors it has
        return 1 #TODO I thin kthis will get removed
    
    def __init__(self, operator, limit=20):
        # limit determines the maximum answer for addition and multiplication
        # or the maximum operand for subtraction and division
        
        initFunctions = {'+': self._initSum, '-': self._initDifference, '*': self._initProduct, '/': self._initQuotient}
        
        if (operator in initFunctions):
            initFunctions[operator](limit)
        #else:
            # the wrong operator was passed. Throw an error or something
            # TODO
            
        # map of operators to functions
#        if (operator == '+'): _initSum(limit)
#        if (operator == '-'): _initDifference(limit)
#        if (operator == '*'): _initProduct(limit)
#        if (operator == '/'): _initQuotient(limit)
        
        
        









