import logging

import sys, os

from sugar.activity import activity

from mathogen_prac_gui import MathogenPracGui


_CORRECT_ANSWERS_TO_WIN = 15


class MathogenPracActivity(activity.Activity):
    """This class is used to load mathogen practice as a sugar activity.
    
    This is done in a separate module so that it is easy to run
    mathogen practice in other contexts (for example, so that my sister
    can play mathogen practice on her computer that does not use the
    sugar desktop environment.
    
    """
    
    def __init__(self, handle):
        # This runs the constructor for an activity
        activity.Activity.__init__(self, handle)
        
        # Creates the Toolbox. It contains the Activity Toolbar, which is the
        # bar that appears on every Sugar window and contains essential
        # functionalities, such as the 'Collaborate' and 'Close' buttons.
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()
        
        
        # Create the main mathogen practice window
        self.layout = MathogenPracGui(_CORRECT_ANSWERS_TO_WIN)
        self.set_canvas(self.layout)
