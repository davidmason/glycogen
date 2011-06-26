
import gtk
import gobject
#import random
#from time import sleep

from glycogen.challenge import challrepo
from glycogen.challenge.challrepo import Challenge, Result

from glycogen.challenge.result import ge_success_func


BUNDLE_ID = 'org.davidmason.mathogen_tute'

#TODO challenges to view all pages for each tutorial
#challenges = { "add_15": Challenge(BUNDLE_ID, "add_15",
#                                   "Answer 15 addition questions correctly during a session",
#                                   Result(15, ge_success_func)),
#               "subtract_15": Challenge(BUNDLE_ID, "subtract_15",
#                                   "Answer 15 subtraction questions correctly during a session",
#                                   Result(15, ge_success_func)),
#               "multiply_15": Challenge(BUNDLE_ID, "multiply_15",
#                                   "Answer 15 multiplication questions correctly during a session",
#                                   Result(15, ge_success_func)),
#               "divide_15": Challenge(BUNDLE_ID, "divide_15",
#                                   "Answer 15 division questions correctly during a session",
#                                   Result(15, ge_success_func)) }


class MathogenTute():
    """Encapsulates a set of tutorial pages that can be displayed."""
    
    def __init__(self):
        self.tutorials = {"Addition Tutorial": self.build_addition_tutorial(),
                           "Subtraction Tutorial": self.build_subtraction_tutorial(),
                           "Multiplication Tutorial": self.build_multiplication_tutorial(),
                           "Division Tutorial": self.build_division_tutorial()}
        
        pass
    
    def get_tutorial_list(self):
        """Returns a list of available tutorials"""
        return self.tutorials.keys()
    
    def page_count(self, tutorial_name):
        return len(self.tutorials[tutorial_name])
    
    def get_page(self, tutorial_name, page_number):
        return self.tutorials[tutorial_name][page_number]
    
    #def check_achievements(self, operator):
    #    challenge_id = operatorchallenge[operator]
    #    repo = challrepo.get_global_repository()
    #    result = repo.get_result(BUNDLE_ID, challenge_id)
    #    if result.get_result() is not None:
    #        if (result.get_result() >= self._correct[operator]):
    #            return  #higher result already recorded
    #    
    #    result.set_result(self._correct[operator])
    #    repo.set_result(BUNDLE_ID, challenge_id, result)
        
        
#a tutorial is just a list of tutorial pages
#just use a container for each page

#tutorial builders return lists of gtk widgets: an ordered set of pages

    def build_addition_tutorial(self):
        pages = []
        for i in range(2):
            pages.append(self.build_addition_page(i))
        return pages
    
    def build_subtraction_tutorial(self):
        return []
    
    def build_multiplication_tutorial(self):
        return []
    
    def build_division_tutorial(self):
        return []


    def build_addition_page(self, page_no):
        if page_no is 0:
            #introduction page
            page = gtk.VBox(False, 0)
            para = "just testing this thing\nto make sure it works properly\nit does work. Have to do newlines manually.\n"
            label = gtk.Label(para)  #TODO set label to wrap
            label.show()
            page.pack_start(label, True, True, 0)
            page.show()
            return page
    
        if page_no is 1:
            page = gtk.Label("This is page 2")
            page.show()
            return page
            
        #TODO throw exception for trying to get out-of-range page
        
        
        
    
    
