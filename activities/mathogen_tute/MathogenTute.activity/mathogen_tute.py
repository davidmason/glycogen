
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
        self.tutorials = {"Addition Tutorial": 3,
                          "Subtraction Tutorial": 3,
                          "Multiplication Tutorial": 3,
                          "Division Tutorial": 3 }
    
    def get_tutorial_list(self):
        """Returns a list of available tutorials"""
        return self.tutorials.keys()
    
    def page_count(self, tutorial_name):
        return self.tutorials[tutorial_name]
    
    def get_page(self, tutorial_name, page_number):
        return self.build_page(tutorial_name, page_number)
    
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

    def build_page(self, tutorial, page_no):
        if tutorial == "Addition Tutorial":
            if page_no is 0:
                page = gtk.VBox(False, 0)
                para = "Addition tutorial intro page\nThese just have stub content for now."
                label = gtk.Label(para)
                label.show()
                page.pack_start(label, True, True, 0)
                page.show()
                return page
        
            if page_no is 1:
                page = gtk.Label("Addition tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Addition tutorial last page")
                page.show()
                return page
        
        if tutorial == "Subtraction Tutorial":
            if page_no is 0:
                page = gtk.Label("Subtraction tutorial intro page")
                page.show()
                return page
                
            if page_no is 1:
                page = gtk.Label("Subtraction tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Subtraction tutorial last page")
                page.show()
                return page
                
        if tutorial == "Multiplication Tutorial":
            if page_no is 0:
                page = gtk.Label("Multiplication tutorial intro page")
                page.show()
                return page
                
            if page_no is 1:
                page = gtk.Label("Multiplication tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Multiplication tutorial last page")
                page.show()
                return page
                
        if tutorial == "Division Tutorial":
            if page_no is 0:
                page = gtk.Label("Division tutorial intro page")
                page.show()
                return page
                
            if page_no is 1:
                page = gtk.Label("Division tutorial first page")
                page.show()
                return page
                
            if page_no is 2:
                page = gtk.Label("Division tutorial last page")
                page.show()
                return page
                
        
        
        #return error label if not a valid tutorial and page
        page = gtk.Label("Page number or tutorial not valid")
        page.show()
        return page
        
        
    
    
