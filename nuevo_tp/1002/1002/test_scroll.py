#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_scroll.py
#
#  Copyright 2024 John Coppens <john@jcoppens.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

from random import random
from pdb import set_trace as st

SIGNAL_HEIGHT = 60
SIGNAL_WIDTH  = 500
SIGNAL_SCALE  = 25
SIGNAL_OFFS   = 505


class Plot_signal(GooCanvas.Canvas):
    def __init__(self, sigs, labels = []):
        super().__init__()

        self.set_bounds(0, 0,
                    SIGNAL_WIDTH * len(sigs), SIGNAL_HEIGHT)
        cvroot = self.get_root_item()
        siglen = len(sigs[0]) - 1
        sig_scale = SIGNAL_WIDTH / siglen

        self.set_size_request(-1, SIGNAL_HEIGHT + 8)

        for x, sig in enumerate(sigs):
            points = GooCanvas.CanvasPoints.new(len(sig))
            for i, cs in enumerate(sig):
                points.set_point(i, i*sig_scale + x*SIGNAL_OFFS,
                                    SIGNAL_HEIGHT//2 - cs * SIGNAL_SCALE)
            poly = GooCanvas.CanvasPolyline(
                        parent = cvroot,
                        points = points,
                        line_width = 2,
                        stroke_color = 'Yellow',
                        fill_color = False)

class Signal(Gtk.Frame):
    def __init__(self):
        super().__init__()

        self.plotter = Plot_signal([[random() for r in range(32)]])
        self.add(self.plotter)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(600, 300)

        vbox = Gtk.VBox()
        for i in range(6):
            vbox.pack_start(Signal(), True, True, 0)

        scroller = Gtk.ScrolledWindow()
        scroller.add(vbox)
        self.add(scroller)
        self.show_all()

    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
