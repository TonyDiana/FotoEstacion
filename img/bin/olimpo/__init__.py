#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Simplificar la invocación de deidades. El orden correcto es:

            - ``from olimpo import ZEUS``
            - ``from olimpo import HELIOS``
            - ``from olimpo import HEISIS``

    :Autor:     Tony Diana
    :Versión:   A8.1

    ---------------------------------------------------------------------------
"""

from .zeus import ZEUS
from .helios import HELIOS
from .helioisis import HEISIS


# --- Evitar error de flake8 F401
a = ZEUS
a = HELIOS
a = HEISIS
del a
