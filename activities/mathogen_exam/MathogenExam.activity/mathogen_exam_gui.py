
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
        
        self._viewer = gtk.VBox(False, 0)
        #viewer stays hidden until an option is selected
        self.pack_start(self._viewer, True, True, 0)
        
        self._page_window = gtk.ScrolledWindow()
        self._page_window.set_size_request(1000, 500)
        self._page_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self._page_window.show()
        self._viewer.pack_start(self._page_window, True, True, 0)
        
        self._control_strip = gtk.HBox(True, 5)
        self._control_strip.show()
        self._viewer.pack_end(self._control_strip, False, False, 0)
        
        self._btn_menu = gtk.Button("Menu")
        self._btn_menu.connect('clicked', self._btn_menu_clicked_cb)
        self._btn_menu.show()
        self._control_strip.pack_start(self._btn_menu, True, False, 0)
        
        #self._page_buttons = gtk.HBox(True, 5)
        #self._page_buttons.show()
        #page buttons will be added to this
        #self._control_strip.pack_start(self._page_buttons, True, True, 0)
        #TODO progress indicator here instead
        
        
        #TODO use mathogen_prac gui code for this. Remove hint.
        
        self.show()
        
        
    
    def _btn_menu_clicked_cb(self, widget, data=None):
        self._viewer.hide()
        self._menu.show()
    
    def _menu_option_clicked_cb(self, widget, data):
        self._start_exam(data)
    
    def _btn_page_clicked_cb(self, widget, data):
        page_number = data
        self._show_page(self._tutorial, page_number)
    
    def _build_menu(self, exams):
        menu = gtk.VBox(True, 20)
        for exam in exams.get_exam_list():
            btn = gtk.Button(exams.get_label[exam])
            btn.show()
            btn.connect("clicked", self._menu_option_clicked_cb, exam)
            menu.pack_start(btn, True, True, 0)
        return menu
    
    
    def _start_exam(self, exam):
        #TODO get exam model to start exam
        #TODO display current maths problem
        #TODO go button/enter need to be hooked up to a checking function that keeps track of the score
        
        self._menu.hide()
        self._viewer.show()
    
    def _show_page(self, tutorial, page):
        """ Displays the indicated page in the viewing area """
        if len(self._page_window.get_children()) > 0:
            self._page_window.remove(self._page_window.get_children()[0])
        if len(self._page_window.get_children()) > 0:
            self._page_window.remove(self._page_window.get_children()[0])  #trying to overcome a bug
        self._page_window.add_with_viewport(self._tute.get_page(tutorial, page))
    
    
    
    
    
    
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

    
