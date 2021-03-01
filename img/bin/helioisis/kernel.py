#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Kernel efectiva de HelioIsis.
    :Autor:     Tony Diana
    :Versión:   A9.1

    ---------------------------------------------------------------------------
"""

# --- Módulos estándard
from std.tinyDB import Registro


# --- Deidades
from olimpo import ZEUS
from olimpo import HELIOS


# --- Módulos propios
from . import const as K


#
def HEISIS_init(obj: object) -> None:
    """
    :Propósito:
        Tiene todo el ``__init__`` efectivo de ``HELIOISIS``, para liberar la
        carga de memoria de este. Recibe a ``HELIOISIS`` como objeto abstracto,
        así que sólo ``HELIOISIS`` la debería llamar.
    """

    # --- Especiales
    #
    #
    obj.EstablecerCTRL(obj._ClaseHeIsis__SOY, K.SOY)
    obj.EstablecerCTRL(obj._ClaseHeIsis__VERSION, K.VERSION)

    #
    # --- Montar PAQUETE
    #
    # --- TUPLAS con campos bool, int y float y descriptivos
    obj.EstablecerCTRL(obj.BOOLS, (obj._ClaseHeIsis__DS1,
                                   obj._ClaseHeIsis__DS2,
                                   obj._ClaseHeIsis__DS3))

    #   obj.EstablecerCTRL(obj.INTS, False)
    #   obj.EstablecerCTRL(obj.FLOAT, False)

    obj.EstablecerCTRL(obj.DESCR, (obj._ClaseHeIsis__DS0,
                                   obj._ClaseHeIsis__DT0))

    # --- Registro prototipo
    temp = {
            obj._ClaseHeIsis__D0Z: K.VERSION,
            obj._ClaseHeIsis__DS0: (ZEUS.getSepJson + " Memorizados"),
            obj._ClaseHeIsis__DS1: False,
            obj._ClaseHeIsis__DS2: False,
            obj._ClaseHeIsis__DS3: False,
            obj._ClaseHeIsis__DT0: (ZEUS.getSepJson + " Textos varios"),
            obj._ClaseHeIsis__DT1: "DEVOLVER",
            }
    obj.MontarPROTO(temp)
    del temp

    # --- BD, Tabla y KEY del registro
    obj.BD = ZEUS.BD
    obj.EstablecerCTRL(obj.TABLA, ZEUS.getFileConf)
    obj.EstablecerCTRL(obj.KEY, K.SOY)


#
class ClaseHeIsis(Registro):
    """ :Propósito: Clase manejadora de HelioIsis.

        .. note::
           Aunque no utiliza una estructura de diseño **Singleton**, si se
           instancia más de un objeto ``HEISIS``, todos apuntarán a las mismas
           propiedades de clase (ya que reconvierte las propiedades de
           ``EnteDatos`` a propiedades de su propia clase) y tendrán el mismo
           comportamiento.
    """

    __slots__ = []

    # --- Palabras mágicas
    __mg = {
        "msg": "Cambiado mensaje que solicita la devolución"
    }

    # --- Especiales
    __SOY = "SOY"
    __VERSION = "VERS"

    # --- Montar un PAQUETE de EnteDatos de clase para Singleton
    __PAQUETE = None

    #
    # --- Compatibles con EnteDatos
    #
    #
    #
    __D0Z = "0Z_Vers"

    # --- Memorizados para la ventana de exposición
    __DS0 = "S0"
    __DS1 = "S1"
    __DS2 = "S2"
    __DS3 = "S3"

    __DT0 = "T0"        # --- Separador visual, textos
    __DT1 = "T1"

    #
    def __init__(self):

        Registro.__init__(self)

        # --- Singleton sin Singleton
        if self.__class__.__PAQUETE:
            # --- nª instancia, puntero local a clase
            self.PAQUETE = self.__class__.__PAQUETE

        else:
            # --- 1ª instancia, puntero clase iniciado
            self.__class__.__PAQUETE = self.PAQUETE

            # --- Identidad
            aux = __name__ + "." + self.__class__.__name__
            self.EstablecerCTRL(self.ENTE, aux)
            del aux

            # --- Inicio efectivo
            HEISIS_init(self)
            self.LeerRegistro()

    #
    # --- Métodos Especiales
    #
    #
    #
    def Fin(self) -> None:
        """ Finalización del proceso de HelioIsis. """
        self.Guardar()
        HELIOS.GuardarRegistro()

    #
    def Guardar(self) -> None:
        """ Guardar los datos de HelioIsis. """
        self.GuardarRegistro()

    #
    # --- Propiedades Especiales
    #
    #
    #
    @property
    def getSoy(self) -> str:
        """ Evitar HelioIsis como palabra mágica. """
        return self.DevolverCTRL(self.__SOY)

    #
    @property
    def getVersion(self) -> str:
        """ Versión actual de HelioIsis. """
        return self.DevolverCTRL(self.__VERSION)

    #
    # --- Modo de la medición de exposición
    #
    #
    @property
    def esFlash(self) -> bool:
        """ Obtener / Establecer Si se está midiendo flash o continua. """
        return self.DevolverREG(self.__DS1)

    @esFlash.setter
    def esFlash(self, dato):
        self.EstablecerREG(self.__DS1, dato)

    #
    @property
    def esPuntual(self) -> bool:
        """ Obtener / Establecer Si se está midiendo puntual o evaluativa. """
        return self.DevolverREG(self.__DS2)

    @esPuntual.setter
    def esPuntual(self, dato):
        self.EstablecerREG(self.__DS2, dato)

    #
    @property
    def esApertura(self) -> bool:
        """ Obtener / Establecer Si se está midiendo la apertura o el T/V. """
        return self.DevolverREG(self.__DS3)

    @esApertura.setter
    def esApertura(self, dato):
        self.EstablecerREG(self.__DS3, dato)

    #
    # --- Mensajes
    #
    #
    @property
    def msg(self) -> str:
        """ Obtener / Establecer mensaje para solicitar la devolución. """
        return self.DevolverREG(self.__DT1)

    @msg.setter
    def msg(self, dato):
        if (self.DevolverREG(self.__DT1) != dato):
            # --- Vamos a guardar y a generar un log
            self.EstablecerREG(self.__DT1, dato)
            ZEUS.log_INFO(self.DevolverCTRL(self.ENTE), self.__mg["msg"])
            self.GuardarRegistro()

    #
    # --- Propiedades calculadas
    #
    #
    @property
    def getFileCSS(self) -> str:
        """ Path + archivo del CSS propio. """
        return ZEUS.MiCSS(self.DevolverCTRL(self.__SOY))

    #
    @property
    def getPathTema(self) -> str:
        """ Path del tema propio. """
        return ZEUS.MiPathTema(self.DevolverCTRL(self.__SOY))
