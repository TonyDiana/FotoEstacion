#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Invocación a Helios desde cualquier deidad. Aportar el objeto
        ``HELIOS`` y ayuda a evitar referencias circulares de código. Para
        invocarlo se utilizará siempre la declaración:

        ``from olimpo import HELIOS``

        De esta manera queda unificado su uso en toda la solución.

    :Autor:     Tony Diana
    :Versión:   A7.2

    ---------------------------------------------------------------------------
"""

# --- Módulos propios
from helios import const as K
from helios.kernel import ClaseHelios


# --- Configurador global
HELIOS = ClaseHelios()


# --- Al igual que ZEUS, borra sus propias constantes ya innecesarias
del K.SOY, K.VERSION, K.DEC_UN_3, K.DEC_DOS_3
