import logging
import sys, os

import mathogen_tute
from sugar.activity import activity
from mathogen_tute_gui import MathogenTuteGui
from glycogen.challenge.challrepo import ChallengeRepo, Challenge



class MathogenTuteActivity(activity.Activity):
    """This class is used to load mathogen tute as a sugar activity.
    
    """
    
    def __init__(self, handle):
        # This runs the constructor for an activity
        activity.Activity.__init__(self, handle)
        
        # Creates the standard activity Toolbox.
        toolbox = activity.ActivityToolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()
        
        # Create the main mathogen tutorial window
        self.layout = MathogenTuteGui()
        self.set_canvas(self.layout)

        repository = ChallengeRepo()
        repository.update_challenges(mathogen_tute.BUNDLE_ID, mathogen_tute.challenges)

