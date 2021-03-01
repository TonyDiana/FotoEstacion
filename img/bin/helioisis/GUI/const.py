#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Constantes del GUI de HelioIsis
    :Autor:     Tony Diana
    :Versión:   A7.2

    ---------------------------------------------------------------------------
"""

# --- Módulos estándard
from std.datos import auto


# --- Identidad
SOMOS = "GUI"


#
class Option(object):
    """ Enumerador con las opciones del menú. """

    # --Se necesitan números fijos para permitir persistencia de iSMTP, por
    #   eso no serviría un auto(), además el valor de auto() no es serializable
    #   para el json de TinyDB, ni en memoria.

    SALIR = 1   # --- Nunca cambiar este valor, el resto no importa
    MAIN = auto()
    SETUP = auto()
    EXP = auto()
    CALC = auto()

    #
    # --- Opciones especiales
    #
    #
    CAM = auto()
