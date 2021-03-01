#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores del tiempo y fechas.
    :Autor:     Tony Diana
    :Versión:   21.01.14

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
from datetime import datetime


def now(compacta: bool = False) -> str:
    """
    :Propósito:
        Devuelve la fecha del AHORA en formato AAAA/MM/DD HH:MM:SS:mc en forma
        normal y de forma compacta en formato AAMMDD HHMMSS:mc, según el
        parámetro recibido
    """
    x = datetime.now()

    if compacta:
        return datetime.strftime(x, '%y%m%d %H%M%S:%f')
    else:
        return datetime.strftime(x, '%Y/%m/%d %H:%M:%S:%f')
