#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sstv_gen.py
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
#  2024/11/03 - v1031a
#       Ahora puede generar líneas repetidas (parámetro N en 'generate_line')
#       Uso preferido, ya que no causa saltos de fase entre líneas.
#  2024/11/02 - v1031
#       Primera versión completa. Genera una sola línea de 'video'

from toolbox import Toolbox
import pylab as plt
import numpy as np
import scipy as sp
import readline

from pdb import set_trace as st

Fs = 24000


def input_with_prefill(prompt, text):
    # Rutina auxiliar que permite pedir datos al usuario, con un valor precargado
    # https://stackoverflow.com/a/8505387/1545014
    def hook():
        readline.insert_text(text)
        readline.redisplay()

    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result


def test_generator():
    # Simplemente una prueba para comprobar si toolbox está correctamente
    # aceptando los comandos de cambiar de frecuencia
    #   - inicialmente pide 120 muestras a 1000 Hz
    #   - luego da la orden de cambiar a 2000 Hz
    #   - y solicita 120 muestras mas.

    tb = Toolbox(Fs)
    sg = tb.sine_generator(1000)

    samples = []
    for i in range(240):
        if i == 120:
            samples.append(sg.send(2000))
        else:
            samples.append(next(sg))

    # ~ print(samples)
    plt.plot(samples)
    plt.show()


def write_wav(samples, fname):
    sp.io.wavfile.write(fname, Fs, np.array(samples))


# Todo lists.
#       Primer elemento es el comando (None finaliza la linea. Un numero
#       será la nueva frecuencia (en Hz). Letras indican casos especiales.
#
#       El segundo elemento es el tiempo (en ms) de permanencia en este estado.

MARTIN_M1_TEST = [
    (1200,   4.862),
    (1500,   0.572),
    (2300, 146.432),    # White
    (1500,   0.572),
    (1900, 146.432),    # Gray
    (1500,   0.572),
    (1500, 146.432),    # Black
    (1500,   0.572),
    (None,   0)]

# Definición de la cantidad de pixeles por línea
MARTIN_M1_W = 320
# Ahora generamos 320 'comandos' para crea la escala de grises para 1 color
MARTIN_M1_RAMP = [(f, 146.432/MARTIN_M1_W)
            for f in np.linspace(2300, 1500, MARTIN_M1_W, endpoint = False)]
# Y finalmente generamos la línea completa:
#       4.862 ms del pulso de sincronismo horizontal
#       0.572 ms 'porche' negro
#     146.432 ms con 320 pixeles para 'Azul'
#       0.572 ms 'porche' negro
#     146.432 ms con 320 pixeles para 'Verde'
#       0.572 ms 'porche' negro
#     146.432 ms con 320 pixeles para 'Rojo'
#       0.572 ms 'porche' negro

MARTIN_M1_GRAYS = ( [(1200,   4.862),
                     (1500,   0.572)] + MARTIN_M1_RAMP +
                    [(1500,   0.572)] + MARTIN_M1_RAMP +
                    [(1500,   0.572)] + MARTIN_M1_RAMP +
                    [(1500,   0.572), (None, 0)]
                  )


def generate_line(todo_list, N = 1):
    """ Genera N (por defecto 1) líneas de la señal de SSTV.
        'todo_list' contiene tuplas de los pasos a seguir, como tuplas
    """
    # Start the sine generator
    tb = Toolbox(Fs)
    sg = tb.sine_generator(1200)
    next(sg)                    # Pedido inicial, para habilitar send()
    t = 0                       # Tiempo absoluto
    dt = 1000/Fs                # Tiempo entre muestras
    samples = []                # Acumulador de muestras generadas

    # Bucle exterior que genera N líneas
    for n in range(N):
        index = 0               # Apunta al item activo en 'todo'
        # Este bucle se ejecuta Fs veces por segundo, hasta que encuentra None
        while True:
            t += dt                 # Tiempo relativo en ms
            if t >= 0:
                cmd, incr = todo_list[index]
                t -= incr
                index += 1

                if cmd is None:
                    break

                else:
                    samples.append(sg.send(cmd))
            else:
                samples.append(next(sg))


    fn = input_with_prefill('nombre para el archivo .wav - ', 'sstv.wav')
    if fn != '':
        write_wav(samples, fn)
    # ~ print(samples)



def main(args):
    generate_line(MARTIN_M1_GRAYS, 3)
    # ~ generate_line(MARTIN_M1_TEST)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
