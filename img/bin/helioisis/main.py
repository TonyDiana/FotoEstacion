#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Iniciar HelioIsis, separado de la kernel para facilitar la lectura del
        código y para simplificar el inicio. También evita las referencias
        circulares.

        Ofrece la función ``HEISIS_main()``, la cual inicia a HelioIsis.

    :Autor:     Tony Diana
    :Versión:   A7.1

    ---------------------------------------------------------------------------
"""

# --- Módulos propios
from .GUI.main import GO

HEISIS_main = GO
