#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Invocación a HelioIsis desde cualquier deidad. Aportar el objeto
        ``HEISIS`` y ayuda a evitar referencias circulares de código. Para
        invocarlo se utilizará siempre la declaración:

        ``from olimpo import HEISIS``

        De esta manera queda unificado su uso en toda la solución.

    :Autor:     Tony Diana
    :Versión:   A7.2

    ---------------------------------------------------------------------------
"""

# --- Módulos propios
from helioisis import const as K
from helioisis.kernel import ClaseHeIsis


# --- Configurador global
HEISIS = ClaseHeIsis()


# --- Al igual que ZEUS, borra sus propias constantes ya innecesarias
del K.SOY, K.VERSION
