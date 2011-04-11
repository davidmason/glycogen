from sugar.activity import activity
import logging

import sys, os
import gtk

class MathogenPrac(activity.Activity):
    def hello(self, widget, data=None):
        logging.info('Hello World')
    
    
    # weight can be something like pango.WEIGHT_BOLD 
    def _setFontParams(self, widget, scale=None, weight=None):
        context = widget.get_pango_context()
        font = context.get_font_description()
        if scale is not None:
            font.set_size(int(font.get_size() * scale))
        if weight is not None:
            font.set_weight(weight)
        widget.modify_font(font)

    
    def __init__(self, handle):
        print "running activity init", handle
        activity.Activity.__init__(self, handle)
        print "activity running"

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
        self._setFontParams(self.button_add, scale=2)
        self._setFontParams(self.button_subtract, scale=2)
        self._setFontParams(self.button_multiply, scale=2)
        self._setFontParams(self.button_divide, scale=2)
        
        # pack contents into topbar
        self.topbar.pack_start(self.button_add, False, False, 5)
        self.topbar.pack_start(self.button_subtract, False, False, 5)
        self.topbar.pack_start(self.button_multiply, False, False, 5)
        self.topbar.pack_start(self.button_divide, False, False, 5)
        self.topbar.pack_end(self.hintmessage, False, False, 5)
        
        # Section 2: challenge
        # holds a table that shows the sum and hint, as well as the answer entry
        self.challenge = gtk.Table(rows=2, columns=6, homogeneous=False)
        
        # top row is the problem/answer
        self.label_num1 = gtk.Label("7")
        self.label_operator = gtk.Label("+")
        self.label_num2 = gtk.Label("4")
        self.label_equals = gtk.Label("=")
        self.answer = gtk.Entry(3)
        self.button_go = gtk.Button("Go!")
        
        
        self._setFontParams(self.label_num1, scale=4)
        self._setFontParams(self.label_operator, scale=4)
        self._setFontParams(self.label_num2, scale=4)
        self._setFontParams(self.label_equals, scale=4)
        self._setFontParams(self.answer, scale=4)
        self._setFontParams(self.button_go, scale=4)
        
        self.challenge.attach(self.label_num1, 0, 1, 0, 1)
        self.challenge.attach(self.label_operator, 1, 2, 0, 1)
        self.challenge.attach(self.label_num2, 2, 3, 0, 1)
        self.challenge.attach(self.label_equals, 3, 4, 0, 1)
        self.challenge.attach(self.answer, 4, 5, 0, 1)
        self.challenge.attach(self.button_go, 5, 6, 0, 1)
        
        # bottom row is for the clue (hidden by default)
        self.label_num1_clue = gtk.Label("..... ..")
        self.label_operator_clue = gtk.Label("+")
        self.label_num2_clue = gtk.Label("....")
        self.label_equals_clue = gtk.Label("=")
        self.label_answer_clue = gtk.Label("..... ..... .")
        self.button_clue = gtk.Button("?")
        
        self._setFontParams(self.label_num1_clue, scale=4)
        self._setFontParams(self.label_operator_clue, scale=4)
        self._setFontParams(self.label_num2_clue, scale=4)
        self._setFontParams(self.label_equals_clue, scale=4)
        self._setFontParams(self.label_answer_clue, scale=4)
        self._setFontParams(self.button_clue, scale=4)
        
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
        self.layout.pack_start(self.challenge, True, True, 5)
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

        # Creates a new button with the label "Hello World".
#        self.button = gtk.Button("Mathogen Practice")
    
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
#        self.button.connect("clicked", self.hello, None)
    
        # Set the button to be our canvas. The canvas is the main section of
        # every Sugar Window. It fills all the area below the toolbox.
#        self.set_canvas(self.button)
    
        # The final step is to display this newly created widget.
#        self.button.show()
