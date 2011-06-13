
import gtk
import gobject
import random
from time import sleep

from mathogen_prac import MathogenPrac

_NEW_QUESTION_DELAY = 900  # milliseconds


_OPERATOR_BUTTON_TEXT_SCALE = 4
_HINTMESSAGE_TEXT_SCALE = 5
_PROGRESS_TEXT_SCALE = 5
_CHALLENGE_TEXT_SCALE = 7
_CHALLENGE_BUTTON_TEXT_SCALE = 5



def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# weight can be something like pango.WEIGHT_BOLD 
def _set_font_params(widget, scale=None, weight=None):
    context = widget.get_pango_context()
    font = context.get_font_description()
    if scale is not None:
        font.set_size(int(font.get_size() * scale))
    if weight is not None:
        font.set_weight(weight)
    widget.modify_font(font)



class MathogenPracGui(gtk.VBox):
    """Handles GUI display for a mathogen practice game, as well as a lot of
    the control code. Game logic is in mathogen_prac.py


    """
    
    def _set_operator(self, widget, data):
        
        if (widget.get_active()):
            if (not data in self.operators):
                self.operators.append(data)
        else:
            if (data in self.operators):
                self.operators.remove(data)
        
    def _try_answer(self, widget, data=None):
        user_input = self.answer.get_text()
        
        if not user_input:
            self.hintmessage.set_text("You didn't enter an answer yet")
            return
        if (not is_int(user_input)):
            self.hintmessage.set_text("Your input doesn't look like a number")
            return
        if (self._practice.try_answer(int(user_input))):
            self.hintmessage.set_text("That's right!")
            self._show_progress(self._practice)
            gobject.timeout_add(_NEW_QUESTION_DELAY, self._next_problem_cb)
        else:
            self.hintmessage.set_text("Nope. Try again.")
            self.answer.grab_focus()
            # could make a function that takes the suggested and actual answer and generates a message
    
    def _next_problem_cb(self):
        self._show_problem(self._practice.new_problem(random.choice(self.operators)))
        return False  # return false so that it stops the timeout and runs only once
    
    
    def __init__(self, correct_to_win=15):
        """Creates a new mathogen practice game, and a gtk container
        that will display it.
        
        The optional correct_to_win argument indicates how many
        questions the player must answer before they are shown a
        message that says they have won.
        
        """
        
        # Initialise this gui window as a vertical box layout
        gtk.VBox.__init__(self, False, 0)
        
        #TODO this code could possibly be more readable by separating it into functions
        

        self.messages = {0.0: "Just starting", 0.25: "Good work", 0.5: "Half way!", 0.75: "Nearly done!", 1.0: "You win!"}
        
        # Section 1: topbar
        # holds 4 buttons that change the mode, and a hint message label
        self.topbar = gtk.HBox(False, 0)
        
        # create contents for topbar
        self.button_add = gtk.ToggleButton("+")
        self.button_subtract = gtk.ToggleButton("-")
        self.button_multiply = gtk.ToggleButton("x")
        self.button_divide = gtk.ToggleButton("/") #TODO try to add a division sign
        self.hintmessage = gtk.Label("this label will say how close your answer is (e.g. 'so close!')")
        
        # increase font size
        _set_font_params(self.button_add.get_child(), scale=_OPERATOR_BUTTON_TEXT_SCALE)
        _set_font_params(self.button_subtract.get_child(), scale=_OPERATOR_BUTTON_TEXT_SCALE)
        _set_font_params(self.button_multiply.get_child(), scale=_OPERATOR_BUTTON_TEXT_SCALE)
        _set_font_params(self.button_divide.get_child(), scale=_OPERATOR_BUTTON_TEXT_SCALE)
        _set_font_params(self.hintmessage, scale=_HINTMESSAGE_TEXT_SCALE)
        
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
        
        
        _set_font_params(self.label_num1, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_operator, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_num2, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_equals, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.answer, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.button_go.get_child(), scale=_CHALLENGE_BUTTON_TEXT_SCALE)
        
        self.challenge.attach(self.label_num1, 0, 1, 0, 1)
        self.challenge.attach(self.label_operator, 1, 2, 0, 1)
        self.challenge.attach(self.label_num2, 2, 3, 0, 1)
        self.challenge.attach(self.label_equals, 3, 4, 0, 1)
        self.challenge.attach(self.answer, 4, 5, 0, 1)
        
        # go button is in a container to provide some padding
        # go_button_container = gtk.Container()
        # go_button_container.
        self.challenge.attach(self.button_go, 5, 6, 0, 1)
        
        # bottom row is for the clue (hidden by default)
        self.label_num1_clue = gtk.Label("")
        self.label_operator_clue = gtk.Label("")
        self.label_num2_clue = gtk.Label("")
        self.label_equals_clue = gtk.Label("")
        self.label_answer_clue = gtk.Label("")
        self.button_clue = gtk.Button("?")
        
        _set_font_params(self.label_num1_clue, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_operator_clue, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_num2_clue, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_equals_clue, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_answer_clue, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.button_clue.get_child(), scale=_CHALLENGE_BUTTON_TEXT_SCALE)
        
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
        self.progress.set_text("Just starting")
        self.progress.set_fraction(0.0)
        _set_font_params(self.progress, scale=_PROGRESS_TEXT_SCALE)
        
        self.racetrack.pack_start(self.progress, True, True, 0)
        
#        # pack the 3 sections into the main layout
#        self.layout.pack_start(self.topbar, False, False, 5)
#        self.layout.pack_start(self.challenge, True, True, 30)
#        self.layout.pack_start(self.racetrack, False, False, 0)

        #replacing above, as self is now the canvas:
        self.pack_start(self.topbar, False, False, 5)
        self.pack_start(self.challenge, True, True, 30)
        self.pack_start(self.racetrack, False, False, 0)
        
        
        # show all of topbar
        self.button_add.show()
        self.button_subtract.show()
        self.button_multiply.show()
        self.button_divide.show()
        self.hintmessage.show()
        self.topbar.show()
        
        # set button sizes in challenge
        self.button_go.set_size_request(10, 10)
        self.button_clue.set_size_request(50, 50)
        
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
        self.show()
        #old show, before self was the canvas
        #self.layout.show()
        
        # start with just the 'add' operation selected
        self.operators = ["+"]
        self.button_add.set_active(True)
        self.button_subtract.set_active(False)
        self.button_multiply.set_active(False)
        self.button_divide.set_active(False)
        
        
        self.button_go.connect("clicked", self._try_answer, None)
        self.answer.connect("activate", self._try_answer, None)
        
        # connect operator buttons
        self.button_add.connect("toggled", self._set_operator, "+")
        self.button_subtract.connect("toggled", self._set_operator, "-")
        self.button_multiply.connect("toggled", self._set_operator, "*")
        self.button_divide.connect("toggled", self._set_operator, "/")
        
        # create a new MathogenPrac() to keep track of number of questions answered
        self._practice = MathogenPrac() #this should already have the first (addition) question generated
        self._show_problem(self._practice.currentProblem)
    
        
    def _show_problem(self, prob):
        self.label_num1.set_text(str(prob.operand1))
        self.label_num2.set_text(str(prob.operand2))
        self.label_operator.set_text(prob.operator)
        self.answer.set_text("")
        self.answer.grab_focus()
        self.hintmessage.set_text("Try this one...")
    
    def _show_progress(self, prac):
        fraction = prac.get_progress()
        if fraction <= 1.0:
            self.progress.set_fraction(fraction)
        else:
            self.progress.set_fraction(1.0)
        
        # loop through self.messages until we get the right one
        keys = self.messages.keys()
        keys.sort()
        for key in keys:
            if (fraction >= key):
                message_key = key
            else:
                break
        self.progress.set_text(self.messages[message_key])


def close_window(self, widget, data=None):
    """Callback function to close the window when the program
    is run as main and the user pressed the 'x' to close it
    
    """
    gtk.main_quit()
    return False
        
# this will run mathogen practice in a window if this file is
# run directly.        
if __name__ == "__main__":
    #TODO use a command line argument for the number questions passed to the constructor
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("Mathogen Practice")
    window.set_border_width(10)
    window.connect("delete_event", close_window)
    
    gui = MathogenPracGui(15)
    window.add(gui)
    window.show()
    gtk.main()

    
