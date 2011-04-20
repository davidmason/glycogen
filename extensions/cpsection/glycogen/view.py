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
from sugar.graphics.radiotoolbutton import RadioToolButton
from sugar.graphics.icon import Icon

from jarabe.controlpanel.sectionview import SectionView
from jarabe.controlpanel.inlinealert import InlineAlert

from jarabe.desktop import homebox
from jarabe.desktop import homewindow
from jarabe.desktop.activitieslist import ActivitiesList

# DEPRECATED: function to be attached as view_glycogen in the home box
#def view_glycogen_function(self):
#    logging.debug('GLYCOGEN: in view glycogen function')
#    if self._favorites_view in self.get_children():
#        self.remove(self._favorites_view)
#        
#    if self._list_view in self.get_children():
#        self.remove(self._list_view)
#        
#    if self._glycogen_view not in self.get_children():
#        self.add(self._glycogen_view)
#        self._glycogen_view.show()
#        
#    logging.debug('GLYCOGEN: end of view glycogen function')

class GlycogenLauncher(SectionView):
    
    def _show_pathway_button_cb(self, widget, data=None):
        logging.debug('GLYCOGEN: Activate! button pressed')
        
        # show the pathway view
        self.home_box._set_view(self.model._PATHWAY_VIEW)
        
        
    def _add_pathway_button_cb(self, widget, data=None):
        # get the instance of the home box
        home_window = homewindow.get_instance()
        self.home_box = home_window.get_home_box()
        logging.debug('GLYCOGEN: got home_box')
        
        # add the (fake) pathway view to it
        self.home_box._pathway_view = ActivitiesList()
        logging.debug('GLYCOGEN: made an ActivitiesList')
        
        # add the extra int to the homebox module to refer to the pathway view
        homebox._PATHWAY_VIEW = self.model._PATHWAY_VIEW # not a typo, I am trying to add it to the module
        
        # replace the default function with an overriden one
        self.home_box._set_view = types.MethodType(self.model.new_homebox_set_view, self.home_box)
        # the above may be failing because the callback functions are attached to the old version
        # of this method. In that case I would need to reattach them.
        logging.debug('GLYCOGEN: replaced function _set_view()')
        
        # disable the 'add' button as it shouldn't be needed any more
        self.button_add_pathway_view.set_sensitive(False)
        
        # enable the 'show' button since it is meaningful now
#        self.button_show_pathway_view.set_sensitive(True)
        
        # try to add a toolbar icon for the pathway view
        # (uses xo icon for now)
        logging.debug('GLYCOGEN: trying to add pathway button')
        self.add_pathway_button()
        logging.debug('GLYCOGEN: finished adding pathway button')
        
    def add_pathway_button(self):
        # get the hometoolbar
        toolbar = self.home_box._toolbar
        #add a new button, with a different icon
        
        toolbar._pathway_button = RadioToolButton(named_icon='sugar-xo')
        toolbar._pathway_button.props.group = toolbar._list_button
        toolbar._pathway_button.props.tooltip = _('Pathway view')
        toolbar._pathway_button.props.accelerator = _('<Ctrl>3')
#        toolbar._pathway_button.connect('toggled', toolbar.__view_button_toggled_cb,
#                                     _LIST_VIEW)

        toolbar._pathway_button.connect('toggled', self._show_pathway_button_cb, None)

        toolbar.insert(toolbar._pathway_button, toolbar.get_item_index(toolbar._list_button)+1)
        toolbar._pathway_button.show()
        
        #TODO need to hook this up to a toggle function so it will work when pressed
        
        
    
    def __init__(self, model, alerts):
        SectionView.__init__(self)
        
        logging.debug('GLYCOGEN: init GlycogenLauncher')
        
        self.model = model

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
        
        self.box_buttons = gtk.VBox()
        self.box_buttons.set_border_width(style.DEFAULT_SPACING * 2)
        self.box_buttons.set_spacing(style.DEFAULT_SPACING)
        
        self.button_add_pathway_view = gtk.Button('Add pathway view')
        self.button_add_pathway_view.connect('clicked', self._add_pathway_button_cb, None)
        self.button_add_pathway_view.show()
        
#        self.button_show_pathway_view = gtk.Button('Show it!')
#        self.button_show_pathway_view.connect('clicked', self._show_pathway_button_cb, None)
#        self.button_show_pathway_view.set_sensitive(False)
#        self.button_show_pathway_view.show()      
        
        self.box_buttons.pack_start(self.button_add_pathway_view, expand=False)
#        self.box_buttons.pack_start(self.button_show_pathway_view, expand=False)
        
        self.pack_start(self.box_buttons, expand=False)
        self.box_buttons.show()

