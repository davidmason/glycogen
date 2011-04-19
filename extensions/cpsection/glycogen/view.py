# Copyright (C) 2008, OLPC
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import types
import gtk
import gobject
from gettext import gettext as _

import logging

from sugar.graphics import style

from jarabe.controlpanel.sectionview import SectionView
from jarabe.controlpanel.inlinealert import InlineAlert

from jarabe.desktop import homewindow
from jarabe.desktop.activitieslist import ActivitiesList

# function to be attached as view_glycogen in the home box
def view_glycogen_function(self):
    logging.debug('GLYCOGEN: in view glycogen function')
    if self._favorites_view in self.get_children():
        self.remove(self._favorites_view)
        
    if self._list_view in self.get_children():
        self.remove(self._list_view)
        
    if self._glycogen_view not in self.get_children():
        self.add(self._glycogen_view)
        self._glycogen_view.show()
        
    logging.debug('GLYCOGEN: end of view glycogen function')

class GlycogenLauncher(SectionView):
    
    def _activate_button_cb(self, widget, data=None):
        logging.debug('GLYCOGEN: Activate! button pressed')
        
        # get the instance of the home box
        home_window = homewindow.get_instance()
        self.home_box = home_window.get_home_box()
        logging.debug('GLYCOGEN: got home_box')
        
        # add the (fake) glycogen view to it
        self.home_box._glycogen_view = ActivitiesList()
        logging.debug('GLYCOGEN: made an ActivitiesList')
        
        self.home_box.view_glycogen = types.MethodType(view_glycogen_function, self.home_box)
        logging.debug('GLYCOGEN: attached function view_glycogen()')
        
        self.home_box.view_glycogen()
        
        
        # hardwire it to hide the other views (basically part of the _set_view(self, view): function
#        hb = self.home_box
#        
#        if hb._favorites_view in hb.get_children():
#            hb.remove(hb._favorites_view)
#        if hb._list_view in hb.get_children():
#            hb.remove(hb._list_view)
#        if hb._glycogen_view not in hb.get_children():
#            hb.add(hb._glycogen_view)
#            hb._glycogen_view.show()
#        
#        # add a (fake) view change function to the home box
#        self.home_box.set_glycogen_view = self.fake_set_view
#        logging.debug('GLYCOGEN: attached fake function')
#        
#        # try calling the fake function
#        logging.debug('GLYCOGEN: calling fake function')
#        self.home_box.set_glycogen_view()
#        logging.debug('GLYCOGEN: returned from fake function')
         
    
    def __init__(self, model, alerts):
        SectionView.__init__(self)
        
        logging.debug('GLYCOGEN: init GlycogenLauncher')
        
        self._model = model

        self.set_border_width(style.DEFAULT_SPACING * 2)
        self.set_spacing(style.DEFAULT_SPACING)
        self._group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)

        separator = gtk.HSeparator()
        self.pack_start(separator, expand=False)
        separator.show()

        label_activation = gtk.Label('Ready to activate Glycogen?')
        label_activation.set_alignment(0, 0)
        self.pack_start(label_activation, expand=False)
        label_activation.show()
        
        label_test = gtk.Label(self._model.test_get_string())
        label_test.set_alignment(0, 0)
        self.pack_start(label_test, expand=False)
        label_test.show()
        
        self._box_sliders = gtk.VBox()
        self._box_sliders.set_border_width(style.DEFAULT_SPACING * 2)
        self._box_sliders.set_spacing(style.DEFAULT_SPACING)

        self.button_activate_glycogen = gtk.Button('Activate!')
        self._box_sliders.pack_start(self.button_activate_glycogen, expand=False)
        self.button_activate_glycogen.connect("clicked", self._activate_button_cb, None)
        self.button_activate_glycogen.show()
        
        self.pack_start(self._box_sliders, expand=False)
        self._box_sliders.show()

