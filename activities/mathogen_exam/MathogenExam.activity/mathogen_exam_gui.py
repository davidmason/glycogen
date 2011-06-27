
import gtk
import gobject
#import random
#from time import sleep

from mathogen_exam import MathogenExam


_MENU_BUTTON_TEXT_SCALE = 4
_MESSAGE_TEXT_SCALE = 3
_PROGRESS_TEXT_SCALE = 3
_CHALLENGE_TEXT_SCALE = 6
_CHALLENGE_BUTTON_TEXT_SCALE = 3


# weight can be something like pango.WEIGHT_BOLD 
def _set_font_params(widget, scale=None, weight=None):
    context = widget.get_pango_context()
    font = context.get_font_description()
    if scale is not None:
        font.set_size(int(font.get_size() * scale))
    if weight is not None:
        font.set_weight(weight)
    widget.modify_font(font)




_NEW_QUESTION_DELAY = 900  # milliseconds



class MathogenExamGui(gtk.VBox):
    """Handles GUI display for a mathogen tutorials"""
    
    
    def __init__(self):
        """Creates a new mathogen tutorial display, with a clickable
        list of avaliable tutorials."""
        gtk.VBox.__init__(self, False, 0)
        
        self._exams = MathogenExam()
        
        self._menu = self._build_menu(self._exams)
        self._menu.show()
        self.pack_start(self._menu, True, True, 0)
        
        self._exam_box = gtk.VBox(False, 0)
        self.pack_start(self._exam_box, True, True, 0)
        #hidden until an exam is started
        
        self._problem_viewer = gtk.VBox(True, 0)
        self._problem_viewer.show()
        self._exam_box.pack_start(self._problem_viewer, True, True, 0)
        
        self._problem_display = gtk.HBox(True, 0)
        self._problem_display.show()
        self._problem_viewer.pack_start(self._problem_display, True, True, 0)
        
        self.label_num1 = gtk.Label("0")
        self.label_operator = gtk.Label("%")
        self.label_num2 = gtk.Label("0")
        self.label_equals = gtk.Label("=")
        self.answer = gtk.Entry(3)
        self.button_go = gtk.Button("Submit\nanswer")
        
        self.answer.connect("activate", self._check_answer_cb)
        self.button_go.connect("clicked", self._check_answer_cb)
        
        _set_font_params(self.label_num1, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_operator, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_num2, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.label_equals, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.answer, scale=_CHALLENGE_TEXT_SCALE)
        _set_font_params(self.button_go.get_child(), scale=_CHALLENGE_BUTTON_TEXT_SCALE)
        
        
        self._problem_display.pack_start(self.label_num1, True, True, 0)
        self._problem_display.pack_start(self.label_operator, True, True, 0)
        self._problem_display.pack_start(self.label_num2, True, True, 0)
        self._problem_display.pack_start(self.label_equals, True, True, 0)
        self._problem_display.pack_start(self.answer, True, True, 0)
        self._problem_display.pack_start(self.button_go, True, True, 0)
        
        self.label_num1.show()
        self.label_operator.show()
        self.label_num2.show()
        self.label_equals.show()
        self.answer.show()
        self.button_go.show()
        
        self._problem_feedback = gtk.Label("")
        _set_font_params(self._problem_feedback, scale=_MESSAGE_TEXT_SCALE)
        self._problem_feedback.show()
        self._problem_viewer.pack_start(self._problem_feedback, True, True, 0)
        
        self._exam_feedback = gtk.Label("No exam completed")
        _set_font_params(self._exam_feedback, scale=_MESSAGE_TEXT_SCALE)
        #hidden until user completes an exam
        self._exam_box.pack_start(self._exam_feedback, True, True, 0)
        
        self._progress_strip = gtk.HBox(False, 0)
        self._progress_strip.show()
        self._exam_box.pack_end(self._progress_strip, False, False, 0)
        
        self._btn_menu = gtk.Button("Menu")
        self._btn_menu.connect("clicked", self._btn_menu_clicked_cb)
        self._btn_menu.show()
        self._progress_strip.pack_start(self._btn_menu, False, False, 0)
        
        self._progress = gtk.ProgressBar()
        _set_font_params(self._progress, scale=_PROGRESS_TEXT_SCALE)
        self._progress.set_text("Not doing an exam")
        self._progress.set_fraction(0.0)
        self._progress.show()
        self._progress_strip.pack_end(self._progress, True, True, 0)
        
        self.show()
        
    def _check_answer_cb(self, widget, data=None):
        user_input = self.answer.get_text()
        
        if not user_input:
            self._problem_feedback.set_text("You didn't enter an answer yet")
            return
        try:
            input_num = int(user_input)
        except ValueError:
            self._problem_feedback.set_text("Your input doesn't look like a number")
            return
        
        if self._exams.try_answer(input_num):
            self._problem_feedback.set_text("Correct")
        else:
            self._problem_feedback.set_text("Incorrect")
        
        self._show_progress()
        self.answer.set_sensitive(False)
        gobject.timeout_add(_NEW_QUESTION_DELAY, self._next_problem_cb)
    
    
    def _next_problem_cb(self):
        problem = self._exams.get_problem()
        if problem is not None:
            self._show_problem(problem)
        else:  #no problems left, exam finished
            correct = self._exams.correct_count()
            questions = self._exams.question_count()
            grade = 100 * correct / questions
            raw_feedback = "Exam complete! Well done.\n\nAnswered {0} of {1} questions correctly.\n\nYour grade is {2}%"
            feedback = raw_feedback.format(correct, questions, grade)
            self._show_exam_feedback(feedback)
        return False  # return false so that it stops the timeout and runs only once
    
    def _show_exam_feedback(self, feedback):
        self._problem_viewer.hide()
        self._exam_feedback.set_text(feedback)
        self._exam_feedback.show()
    
    def _btn_menu_clicked_cb(self, widget, data=None):
        self._exam_box.hide()
        self._menu.show()
    
    def _menu_option_clicked_cb(self, widget, data):
        self._start_exam(data)
    
    def _build_menu(self, exams):
        menu = gtk.VBox(True, 20)
        for exam in exams.get_exam_list():
            btn = gtk.Button(exams.get_label(exam))
            _set_font_params(btn.get_child(), scale=_MENU_BUTTON_TEXT_SCALE)
            btn.show()
            btn.connect("clicked", self._menu_option_clicked_cb, exam)
            menu.pack_start(btn, True, True, 0)
        return menu
    
    
    def _start_exam(self, exam):
        if self._exams.start_exam(exam):
            self._show_problem(self._exams.get_problem())
            self._show_progress()
        else:
            self._show_exam_feedback("Error: this exam doesn't have any questions in it!\n\nTry a different one.")
            pass
        
        self._menu.hide()
        self._exam_feedback.hide()
        self._problem_viewer.show()
        self._exam_box.show()    
    
    def _show_problem(self, prob):
        self.label_num1.set_text(str(prob.operand1))
        self.label_num2.set_text(str(prob.operand2))
        self.label_operator.set_text(prob.operator)
        self.answer.set_text("")
        self.answer.set_sensitive(True)
        self.answer.grab_focus()
        self._problem_feedback.set_text("")
    
    def _show_progress(self):
        correct = self._exams.correct_count()
        answers = self._exams.answer_count()
        questions = self._exams.question_count()
        
        self._progress.set_text("Answered {0} of {1} questions. {2} correct".format(answers, questions, correct))
        
        fraction = float(answers) / float(questions)
        self._progress.set_fraction(fraction)

    

    
    
def close_window(self, widget, data=None):
    """Callback function to close the window when the program
    is run as main and the user pressed the 'x' to close it
    
    """
    gtk.main_quit()
    return False
        
# this will run mathogen tutorial in a window if this file is
# run directly.        
if __name__ == "__main__":
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title("Mathogen Exam")
    window.set_border_width(10)
    window.connect("delete_event", close_window)
    
    gui = MathogenExamGui()
    window.add(gui)
    window.show()
    gtk.main()

    
