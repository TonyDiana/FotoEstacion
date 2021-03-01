#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores de mediciones fotométricas.
    :Autor:     Tony Diana
    :Versión:   A9.1

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
from enum import Enum


# --- Módulos propios
from olimpo import HELIOS
from .entidades import f, T_V, ISO


# --- Constantes propias
class Liberado(Enum):
    """
    Enumerador que indica qué elemento fotométrico está liberado y debe cambiar
    al medir la luz. Si están liberados todos, está en modo super usuario.
    ``HELIOS`` se encarga personalmente de este control.

    .. todo::
        No está desarrollado el modo super usuario.
    """

    # --- Como se va a grabar en el jSon, es necesario conocer un valor
    #   predecible, por eso no se puede usar auto()
    f = 1
    T_V = 2
    ISO = 3
    TODOS = 255


class Medicion(f, T_V, ISO):
    """
    :Propósito: Manejador de una exposición fotométrica.

    :TERCIO_f: Tercio del f/ o ``False``.
    :TERCIO_T_V: Tercio del T/V o ``False``.
    :TERCIO_ISO: Tercio del ISO o ``False``.
    :EVS: EV's de la medición.
    :REAL: Es una medición real o se está en proceso.

    .. note::
        En caso de no pasarle razones fotométricas, tomará las últimas
        empleadas, igual que un exposímetro comercial, donde el ISO y el tiempo
        de exposición, si estamos midiendo con aperturas, no cambian aunque
        apaguemos el aparato.
    """

    __slots__ = ["__EV", "__real", "__error"]

    def __init__(self, TERCIO_f: int = False, TERCIO_T_V: int = False,
                 TERCIO_ISO: int = False, EVS: float = 0.0, REAL: bool = False):

        # --- Iniciadores
        f.__init__(self, TERCIO=(TERCIO_f or HELIOS.ultimo_f))
        T_V.__init__(self, TERCIO=(TERCIO_T_V or HELIOS.ultimo_T_V))
        ISO.__init__(self, TERCIO=(TERCIO_ISO or HELIOS.ultimo_ISO))

        # --- Atributos privados
        self.__EV: float = EVS
        self.__real: bool = REAL
        self.__error: bool = False      # --- Saber si hay error en la medición
        self.__evError: float = 0.0     # --- Cuanto error hay

        # --- Si es medición real (no recién encendido), hay que acomodar
        if self.__real:
            self.__acomodar()

    #
    # --- Métodos públicos
    #
    #
    #
    def setEV(self, EV: float) -> None:
        """ Establecer el EV, y con ello una medición en firme. """
        self.__real = True
        self.__EV = EV

        # --- Ahora debemos acomodar la medición
        self.__acomodar()

    #
    def GanarTERCIOS_f(self, tercios: int = 1) -> bool:
        """ Ganar varios TERCIOS de luz en el f/, por defecto 1. """
        return f.GanarTERCIOS(tercios=tercios)

    #
    def PerderTERCIOS_f(self, tercios: int = 1) -> bool:
        """ Perder varios TERCIOS de luz en el f/, por defecto 1. """
        return f.PerderTERCIOS(tercios=tercios)

    #
    def GanarTERCIOS_T_V(self, tercios: int = 1) -> bool:
        """ Ganar varios TERCIOS de luz en el T/V, por defecto 1. """
        return T_V.GanarTERCIOS(tercios=tercios)

    #
    def PerderTERCIOS_T_V(self, tercios: int = 1) -> bool:
        """ Perder varios TERCIOS de luz en el T/V, por defecto 1. """
        return T_V.PerderTERCIOS(tercios=tercios)

    #
    def GanarTERCIOS_ISO(self, tercios: int = 1) -> bool:
        """ Ganar varios TERCIOS de luz en el ISO, por defecto 1. """
        return ISO.GanarTERCIOS(tercios=tercios)

    #
    def PerderTERCIOS_ISO(self, tercios: int = 1) -> bool:
        """ Perder varios TERCIOS de luz en el ISO, por defecto 1. """
        return ISO.PerderTERCIOS(tercios=tercios)

    #
    # --- Atributos
    #
    #
    # --- Razones fotométricas
    @property
    def getEV(self) -> float:
        """ Obtener el EV de la medición unificada. """
        return self.__EV

    #
    @property
    def getTexto_f(self) -> str:
        """ Obtener el texto del f asociado. """
        return f.getTexto

    @property
    def getTextoDecorado_f(self) -> str:
        """ Obtener el texto del f asociado con decorador """
        return f.getTextoDecorado

    #
    @property
    def getTexto_T_V(self) -> str:
        """ Obtener el texto del T/V asociado """
        return T_V.getTexto

    @property
    def getTextoDecorado_T_V(self) -> str:
        """ Obtener el texto del T/V asociado con decorador """
        return T_V.getTextoDecorado

    #
    @property
    def getTexto_ISO(self) -> str:
        """ Obtener el texto del ISO asociado """
        return ISO.getTexto

    @property
    def getTextoDecorado_ISO(self) -> str:
        """ Obtener el texto del ISO asociado con decorador """
        return ISO.getTextoDecorado

    #
    # --- Métodos privados
    #
    #
    # --- Acomoda el EV entre las relaciones fotométricas
    def __acomodar(self) -> None:

        print(HELIOS.liberado)
        print(Liberado.f.value)

        if HELIOS.liberado == Liberado.f:
            # --- Estamos buscando el f/
            suma = T_V.getEV + ISO.getEV
            falta = self.__EV - suma
            resp = f.setEV(falta)

        elif HELIOS.liberado == Liberado.T_V:
            # --- Estamos buscando el tiempo de exposición
            suma = f.getEV + ISO.getEV
            falta = self.__EV - suma
            resp = T_V.setEV(falta)

        else:
            # --- Estamos buscando el ISO
            suma = f.getEV + T_V.getEV
            falta = self.__EV - suma
            resp = ISO.setEV(falta)

        # --- Veamos si ha funcionado
        if resp:
            self.__Error = False
            self.__evError = 0.0

        else:
            self.__Error = True
            self.__evError = self.__EV - (f.getEV + T_V.getEV + ISO.getEV)
