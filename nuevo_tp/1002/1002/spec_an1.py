#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  spec_an.py
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


""" Para entender lo que se hace en el programa que sigue, por favor
    refererirse a las páginas 104 (118) Fourier Decomposition del DSP guide
    (Cáp. 5) y siguientes).
    Otros ejemplos de la decomposición en el Cáp 8 (The Discrete Fourier
    transformation) páginas 141 etc (155, etc).

    (Números de páginas entre paréntesis son las páginas físicas en el PDF)
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas
from main_menu import Main_menu
from toolbox import Toolbox
from pdb import set_trace as st

SIGNAL_HEIGHT = 60
SIGNAL_WIDTH  = 500
SIGNAL_SCALE  = 25
SIGNAL_OFFS   = 505

class Plot_signal(GooCanvas.Canvas):
    def __init__(self, sigs, labels = []):
        super().__init__()

        assert (len(labels) == 0) or (len(labels) == len(sigs))

        self.set_scrollable(False)
        self.set_bounds(0, 0,
                    SIGNAL_WIDTH * len(sigs), SIGNAL_HEIGHT)
        cvroot = self.get_root_item()
        siglen = len(sigs[0]) - 1
        sig_scale = SIGNAL_WIDTH / siglen

        self.set_size_request(-1, SIGNAL_HEIGHT + 8)

        for x, sig in enumerate(sigs):
            rect = GooCanvas.CanvasRect(
                        parent = cvroot,
                        x = 1 + x*SIGNAL_OFFS, y = 1,
                        width = SIGNAL_WIDTH,
                        height = SIGNAL_HEIGHT,
                        fill_color_rgba = 0x808080ff,
                        stroke_color = 'Gray', line_width = 2)

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


class Signal_editor(Gtk.Frame):
    def __init__(self, label, csig, ssig, tools):
        super().__init__()

        self.csig, self.ssig = csig, ssig
        self.plotter = Plot_signal([csig, ssig])
        self.add(self.plotter)

        toolbar = Gtk.HBox()
        toolbar.pack_start(Gtk.Label(label = label), False, False, 0)
        self.set_label_widget(toolbar)

        for tool in tools:
            btn = Gtk.Button.new_from_icon_name('accessories-text-editor',
                        Gtk.IconSize.MENU)
            btn.set_tooltip_text('Edit the input data')
            btn.connect('clicked', self.on_edit_clicked)
            toolbar.pack_start(btn, False, False, 0)


    def on_edit_clicked(self, btn):
        dlg = Gtk.Dialog()
        dlg.set_size_request(200, 300)
        dlg.add_buttons(
                    'Cancel', Gtk.ResponseType.CANCEL,
                    'Save...', Gtk.ResponseType.ACCEPT)

        # Crear una tabla con los valores a editar. La tabla contiene filas
        # de 2 elementos: coeficientes de cosenos y senos. La tabla es
        # directamente editable.
        self.sig_store = Gtk.ListStore(str, str)
        sig_view = Gtk.TreeView(model = self.sig_store)
        self.sig_store_sel = sig_view.get_selection()

        # Columna de izquierda: Coeficientes de cosenos
        renderer = Gtk.CellRendererText(editable = True)
        renderer.connect('edited', self.cell_edited, 0)
        col = Gtk.TreeViewColumn('Cosine', renderer, text = 0)
        col.set_expand(True)
        sig_view.append_column(col)

        # Columna de derecha: Coeficientes de senos
        renderer = Gtk.CellRendererText(editable = True)
        renderer.connect('edited', self.cell_edited, 1)
        col = Gtk.TreeViewColumn('Sine', renderer, text = 1)
        col.set_expand(True)
        sig_view.append_column(col)

        sig_scroller = Gtk.ScrolledWindow(vexpand = True)
        sig_scroller.add(sig_view)

        # Columna extra con comandos para remover/agregar filas de datos
        # en las muestras
        toolbox = self.make_toolbox()

        hbox = Gtk.HBox()
        tbox = self.make_toolbox()
        hbox.pack_start(sig_scroller, True, True, 0)
        hbox.pack_start(tbox, False, False, 0)

        dlg.get_content_area().add(hbox)
        hbox.show_all()

        # Llena la tabla de edición con los valores a editar
        for c, s in zip(self.csig, self.ssig):
            self.sig_store.append([f'{c}', f'{s}'])

        # Solo para fines diagnósticos: Imprime la tabla de coeficientes
        if dlg.run() == Gtk.ResponseType.ACCEPT:
            for row in self.sig_store:
                print(list(row))

        dlg.destroy()


    def make_toolbox(self):
        tbox = Gtk.VBox(spacing = 4, margin = 3)
        for imgname, handler, tip in [
                    ('list-add', self.add_sample, 'Agregar muestra'),
                    ('list-remove', self.remove_sample, 'remover muestra')]:
            img = Gtk.Image.new_from_icon_name(imgname, Gtk.IconSize.MENU)
            btn = Gtk.Button()
            btn.connect('clicked', handler)
            btn.set_image(img)
            btn.set_tooltip_text(tip)
            tbox.pack_start(btn, False, False, 0)
        return tbox


    def add_sample(self, btn):
        store, iter = self.sig_store_sel.get_selected()
        if iter:
            store.insert(iter, ['2.0', '2.0'])


    def remove_sample(self, btn):
        store, iter = self.sig_store_sel.get_selected()
        if iter == None:
            return
        store.remove(iter)


    def cell_edited(self, renderer, path, new_text, col):
        """ cell_edited recibe el *texto* del valor modificado y debe
            controlar si representa un valor numérico válido antes de aceptarlo
            e sustituirlo en la tabla.
        """
        iter = self.sig_store.get_iter(path)
        try:
            new_val = float(new_text)
            self.sig_store[iter][col] = new_text

        except:
            pass


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(1025, 500)

        vbox = Gtk.VBox(margin = 4)
        mm = Main_menu(['_File', '_Help'])
        mm.add_items_to('_File', [
                    ('_Quit', self.on_quit)])
        vbox.pack_start(mm, False, False, 0)

        # Default input signal
        inp_val = Signal_editor('Input signal',
                    [0.]*17 + [1.]*17,          # Cosenos
                    [0.] * 34,                  # Senos
                    ['edit'])
        vbox.pack_start(inp_val, False, False, 0)

        nr_basis = 34
        tb = Toolbox(1)
        sc, cc = tb.generate_basis_functions(nr_basis)
        for b_nr in range(nr_basis//2):
            basis_val = Signal_editor(f'Basis {b_nr}',
                        cc[b_nr],
                        sc[b_nr],
                        [])
            vbox.pack_start(basis_val, False, False, 0)

        self.scroller = Gtk.ScrolledWindow()
        self.scroller.add(vbox)
        self.add(self.scroller)
        self.show_all()


    def on_quit(self, menuitem):
        Gtk.main_quit()


    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
