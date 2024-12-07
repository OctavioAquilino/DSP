#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  toolbox.py
#
#  Copyright 2024 john <jcoppens@vostro.ampr.net>
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


import pylab as plt
import numpy as np
import scipy

from math import pi, sin, cos
from random import random
from pdb import set_trace as st

class Toolbox:
    """ Class Toolbox:
        Algunas herramientas para mostrar efectos en procesamiento de señales.
        Parámetro(s) del constructor:
            fs      Frecuencia de sampleo       (Opcional, por defecto 48 kHz)
    """
    def __init__(self, fs = 48000):
        self.fs = fs


    def sine_generator(self, f, f0 = 0):
        """ Un método que se comporta como un 'generador' de Python (y un
            generador de senos en electrónica!):
            Parámetros:
                f   Obligatorio     Frecuencia a generar en Hz
                f0  Opcional        Fase inicial (en radianes) Defecto: 0
        """
        fase = f0
        dfase = 2*pi*f/self.fs

        while True:
            newfr = (yield sin(fase)) #Se agrega este cambios para poder cambiar la f funcionando
            if newfr is not None:
                dfase = 2*pi*newfr/self.fs
            fase += dfase


    def cosine_generator(self, f, f0 = 0):
        """ Un método que se comporta como un 'generador' de Python (y un
            generador de cosenos en electrónica!):
            Parámetros:
                f   Obligatorio     Frecuencia a generar en Hz
                f0  Opcional        Fase inicial (en radianes) Defecto: 0
        """
        fase = f0
        dfase = 2*pi*f/self.fs

        while True:
            yield cos(fase)
            fase += dfase


    def noise_generator(self):
        """ Otro generador genera ondas aleatoreas (ruido)
            El ruido generado está ubicado entre -1 y +1
        """
        while True:
            yield (random() - 0.5) * 2


    def generate_basis_functions(self, nr_samples):
        """ Generamos todas las funciones bases necesarias para procesar
            'nr_samples' muestras.
        """
        nr2 = (nr_samples // 2)+1
        for g in range(nr_samples):
            sgen = []
            cgen = []
            sc = []
            cc = []
            for f in range(nr2):
                sgen.append(  self.sine_generator(f * self.fs/nr_samples))
                cgen.append(self.cosine_generator(f * self.fs/nr_samples))
                sc.append(np.zeros(nr_samples))
                cc.append(np.zeros(nr_samples))

        for s in range(nr_samples):
            for f in range(nr2):
                sc[f][s] = next(sgen[f])
                cc[f][s] = next(cgen[f])

        return (sc, cc)


    def plot_basis_functions(self, sc, cc):
        nrs = len(sc[0])
        nr2 = (nrs //2) + 1

        # sines
        for c in range(nr2):
            plt.plot([y for y in cc[c]], label = f'label {c}')
        plt.legend()
        plt.show()

        # cosines
        for c in range(nr2):
            plt.plot([y for y in sc[c]], label = f'label {c}')
        plt.legend()
        plt.show()


    def dump_basis_functions(self, sc, cc):
        nrs = len(sc[0])
        nr2 = (nrs//2) + 1

        # cosines
        for order in range(nr2):
            cstr = f'{order:2d}'
            for c in cc[order]:
                cstr += f' {c:6.3f}'
            print(cstr)


    def set_kernel(self, kernel):
        """ set_kernel:
                - Almacena la lista provista por el parámetro 'kernel'
                - y reserva un registro de desplazamiento 'shift' del mismo
                  largo para calcular correlación
        """
        self.kernel = kernel
        self.shift = [0]*len(self.kernel)


    def correlate(self, sample):
        """ Agrega <muestra> a self.shift ('de arriba') y calcula la
            correlación entre el kernel y el 'shift'.
        """
        self.shift = self.shift[1:] + [sample]  # Descarta la primera muestra
                                                # shift[0] y agrega la muestra
        sum = 0
        for x in range(len(self.kernel)):       # Producto de kernel y shift,
                                                # y acumulamos la correlación en
                                                # 'sum'
            sum += self.kernel[x] * self.shift[x]
        return sum


# Rutinas de validación de la biblioteca

def test_basis_functions():
    tb = Toolbox()
    ss, sc = tb.generate_basis_functions(15)
    # ~ tb.plot_basis_functions(ss, sc)
    tb.dump_basis_functions(ss, sc)


def test_correlate():
    """ Kernel simple y luego correlación con los mismos elementos. El resultado
        tiene que dar:

        [0, 0, 0, 0, 0, 0, 0, 0] 0                                              0*7
        [0, 0, 0, 0, 0, 0, 0, 1] 7                                        0*6   1*7
        [0, 0, 0, 0, 0, 0, 1, 2] 20                                 0*5 + 1*6 + 2*7
        [0, 0, 0, 0, 0, 1, 2, 3] 38                           0*4 + 1*5 + 2*6 + 3*7
        [0, 0, 0, 0, 1, 2, 3, 4] 60                     0*3 + 1*4 + 2*5 + 3*6 + 4*7
        [0, 0, 0, 1, 2, 3, 4, 5] 85               0*2 + 1*3 + 2*4 + 3*5 + 4*6 + 5*7
        [0, 0, 1, 2, 3, 4, 5, 6] 112        0*1 + 1*2 + 2*3 + 3*4 + 4*5 + 5*6 + 6*7
        [0, 1, 2, 3, 4, 5, 6, 7] 140  0*0 + 1*1 + 2*2 + 3*3 + 4*4 + 5*5 + 6*6 + 7*7

    """
    tb = Toolbox(48000)
    tb.set_kernel([0, 1, 2, 3, 4, 5, 6, 7])

    for s in range(8):
        cor = tb.correlate(s)
        print(tb.shift, cor)


def two_tones():
    """ Genera 2 tonos simultáneamente:
             1000Hz con amplitud 0.3
             1500Hz con amplitud 0.7
    """
    tb = Toolbox(48000)
    sg_1000Hz = tb.sine_generator(1000)
    sg_1500Hz = tb.sine_generator(1500)
    y = []
    for i in range(96):
        y.append(0.3 * next(sg_1000Hz)  + 0.7 * next(sg_1500Hz))

    plt.plot(y)
    plt.grid()
    plt.show()


def noise():
    """ Genera 100 muestras de 'ruido'
    """
    tb = Toolbox(48000)
    ng = tb.noise_generator()
    y = []
    for i in range(100):
        y.append(next(ng))
    plt.plot(y)
    plt.grid()
    plt.show()


def main(args):
    # Descomentar la prueba que desea ejecutar.
    # ~ two_tones()
    # ~ noise()
    # ~ test_correlate()
    test_basis_functions()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
