#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Cambio de bases y codificaciones.
    :Autor:     Tony Diana
    :Versión:   21.01.01

    ---------------------------------------------------------------------------
"""

# --- Constante propia con la base de conversión
# ---              1         2         3         4         5         6
# ---     123456789 123456789 123456789 123456789 123456789 123456789 12
__BASE = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def base10_OtraBase(valor: int, base: int = 36) -> str:
    """
    Cambiar un número en base 10 a otra base (36 por defecto y 62 máximo).
    """

    # --- Evitamos que algún despistado envíe un string o una base mayor
    valor = int(valor)
    if base > 62:
        base = 62

    return ((valor == 0) and __BASE[0]) or \
           (base10_OtraBase(valor // base, base).lstrip(__BASE[0]) +
            __BASE[valor % base])


#
def otraBase_Base10(valor: str, base: int = 36) -> int:
    """ Cambiar un número en base x a base 10. """

    # --- Usaremos un int, porque los decimales no se tienen en cuenta
    resultado: int = 0

    # --- Evitamos que algún despistado envíe un int o una base mayor
    valor = str(valor)
    if base > 62:
        base = 62

    # --- Le damos la vuelta al valor
    valor = valor[::-1]
    pos = 0

    # --- Iteramos el valor
    for x in valor:
        resultado += __BASE.find(x) * pow(base, pos)
        pos += 1   # --- Al menos una vez sobrará

    # --- Devolvemos
    return resultado
