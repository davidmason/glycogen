
import gtk
import gobject
#import random
#from time import sleep

from mathogen_exam import MathogenExam


#_OPERATOR_BUTTON_TEXT_SCALE = 4
#_HINTMESSAGE_TEXT_SCALE = 5
#_PROGRESS_TEXT_SCALE = 5
#_CHALLENGE_TEXT_SCALE = 7
#_CHALLENGE_BUTTON_TEXT_SCALE = 5



#def is_int(s):
#    try:
#        int(s)
#        return True
#    except ValueError:
#        return False



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
        self.button_go = gtk.Button("Submit answer")
        
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
        self._problem_feedback.show()
        self._problem_viewer.pack_start(self._problem_feedback, True, True, 0)
        
        self._exam_feedback = gtk.Label("No exam completed")
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
        self._progress.set_text("Not doing an exam")
        self._progress.set_fraction(0.0)
        self._progress.show()
        self._progress_strip.pack_end(self._progress, True, True, 0)
        
        self.show()
        
        
    
    def _btn_menu_clicked_cb(self, widget, data=None):
        self._exam_box.hide()
        self._menu.show()
    
    def _menu_option_clicked_cb(self, widget, data):
        self._start_exam(data)
    
    def _build_menu(self, exams):
        menu = gtk.VBox(True, 20)
        for exam in exams.get_exam_list():
            btn = gtk.Button(exams.get_label(exam))
            btn.show()
            btn.connect("clicked", self._menu_option_clicked_cb, exam)
            menu.pack_start(btn, True, True, 0)
        return menu
    
    
    def _start_exam(self, exam):
        #TODO get exam model to start exam
        #TODO display current maths problem
        #TODO go button/enter need to be hooked up to a checking function that keeps track of the score
        
        self._menu.hide()
        self._exam_feedback.hide()
        self._problem_viewer.show()
        self._exam_box.show()    
    
    
    
# weight can be something like pango.WEIGHT_BOLD 
def _set_font_params(widget, scale=None, weight=None):
    context = widget.get_pango_context()
    font = context.get_font_description()
    if scale is not None:
        font.set_size(int(font.get_size() * scale))
    if weight is not None:
        font.set_weight(weight)
    widget.modify_font(font)
    
    
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

    
