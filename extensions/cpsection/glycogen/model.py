# Copyright (C) 2008 One Laptop Per Child
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

#from gettext import gettext as _
#import gconf


# replacement for jarabe/desktop/homebox.py 112 _set_view(self, view):
_FAVORITES_VIEW = 0
_LIST_VIEW = 1
_PATHWAY_VIEW = 2 # glycogen's view

def new_homebox_set_view(self, view):
    if view == _FAVORITES_VIEW:
        if self._list_view in self.get_children():
            self.remove(self._list_view)
        if self._pathway_view in self.get_children():
            self.remove(self._pathway_view)

        if self._favorites_view not in self.get_children():
            self.add(self._favorites_view)
            self._favorites_view.show()
            
    elif view == _LIST_VIEW:
        if self._favorites_view in self.get_children():
            self.remove(self._favorites_view)
        if self._pathway_view in self.get_children():
            self.remove(self._pathway_view)
        
        if self._list_view not in self.get_children():
            self.add(self._list_view)
            self._list_view.show()
            
    elif view == _PATHWAY_VIEW:
        if self._favorites_view in self.get_children():
            self.remove(self._favorites_view)
        if self._list_view in self.get_children():
            self.remove(self._list_view)
            
        if self._pathway_view not in self.get_children():
            self.add(self._pathway_view)
            self._pathway_view.show()

    else:
        raise ValueError('Invalid view: %r' % view)






# keeping as gconf examples
#def get_corner_delay():
#    client = gconf.client_get_default()
#    corner_delay = client.get_int('/desktop/sugar/frame/corner_delay')
#    return corner_delay
#
#def set_corner_delay(delay):
#    """Set a delay for the activation of the frame using hot corners.
#    instantaneous: 0 (0 milliseconds)
#    delay: 100 (100 milliseconds)
#    never: 1000 (disable activation)
#    """
#    try:
#        int(delay)
#    except ValueError:
#        raise ValueError(_('Value must be an integer.'))
#    client = gconf.client_get_default()
#    client.set_int('/desktop/sugar/frame/corner_delay', int(delay))
#    return 0
