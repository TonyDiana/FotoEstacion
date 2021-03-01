#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Constantes para las cámaras
    :Autor:     Tony Diana
    :Versión:   A9.1

    ---------------------------------------------------------------------------
"""

# --- Librerías de terceros
from terceros.scp import ClasspropertyMeta, classproperty


# --- Identidad
SOY = "cam"
VERS = "0"      # --- Por si algún día debemos hacer cambio de base de datos


# --- Objetivos normales
OBJ_NORM = (18, 28, 35, 40, 50, 85, 100, 120, 135, 150, 220)


# --- Se ofrece separado de las razones fotométricas, para poder usarlo en GUI
ISOS = (
        "25", "32", "40", "50", "64", "80", "100", "125", "160", "200", "250",
        "320", "400", "500", "640", "800", "1000", "1250", "1600", "2000",
        "2500", "3200", "4000", "5000", "6400", "8000", "10.000", "12.800",
        "16.000", "20.000", "25.600", "32.000", "40.000", "51.200", "64.000",
        "80.000", "102.400"
    )


#
class FactoresCoC(metaclass=ClasspropertyMeta):
    """
    :Propósito:
        Ofrecer los factores del círculo de confusión y sus características.
        Es un objeto que funciona como un ``enum`` inteligente. Funciona como
        objeto invocable sin necesidad de ser instanciado, es un puro
        ``@classmethod`` y/o ``@classproperty``.
    """

    # --- Factores del círculo de confusión
    FACTOR_CoC = {
        1000: "Mínimo Canon",
        1250: "Lentes Canon",
        1443: "Dof Master",
        1500: "Máximo Canon",
        1730: "Fórmula Zeiss"
        }

    @classmethod
    def Nombrar(cls, tipo: int) -> str:
        """ Nombrar el tipo de CoC. """
        return cls.FACTOR_CoC[tipo]

    @classproperty
    def factoresAtupla(cls) -> list:
        """ Devuelve el diccionario de factores convertido en tupla/tuplas. """
        return tuple(cls.FACTOR_CoC.items())


#
class TipoCamara(metaclass=ClasspropertyMeta):
    """
    :Propósito:
        Ofrecer los tipos de cámaras y características de los tipos.
        Es un objeto que funciona como un ``enum`` inteligente. Funciona como
        objeto invocable sin necesidad de ser instanciado, es un puro
        ``@classmethod`` y/o ``@classproperty``.
    """

    __slots__ = []

    __TIPOS_CAM = {
        199: "DSLR Con espejo",
        201: "Mirrorless",
        }

    # --- Corte entre las sin y con espejo
    __CORTE: int = 200

    @classmethod
    def Nombrar(cls, tipo: int) -> str:
        """ Nombrar el tipo de cámara según el parámetro. """
        return cls.__TIPOS_CAM[tipo]

    @classmethod
    def esConEspejo(cls, tipo: int) -> bool:
        """ Saber si la cámara tiene o no tiene espejo, según el parámetro. """
        if (tipo > cls.__CORTE):
            return False

        else:
            return True

    @classproperty
    def frontera(cls) -> int:
        """ Retorna el valor frontera entre con y sin espejo. """
        return cls.__CORTE

    @classproperty
    def tiposAtupla(cls) -> list:
        """ Devuelve el diccionario de tipos convertido en tupla de tuplas. """
        return tuple(cls.__TIPOS_CAM.items())
