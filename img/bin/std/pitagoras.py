#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Cálculos matemáticos diversos.
    :Autor:     Tony Diana
    :Versión:   21.01.15

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
import math


def hipotenusa(cateto1: float, cateto2: float, decimales: int) -> float:
    """
    Calcula la hipotenusa, redondeada a un número específico de decimales.
    """
    return round(math.sqrt(
                           (cateto1 ** 2) + (cateto2 ** 2)),
                 decimales)


def cateto(hipotenusa: float, cateto: float, decimales: int) -> float:
    """
    Calcula un cateto, redondeado a un número específico de decimales.
    """
    return round(math.sqrt(
                           (hipotenusa ** 2) - (cateto ** 2)),
                 decimales)
