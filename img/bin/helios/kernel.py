#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Kernel efectiva de Helios.

    :Autor:     Tony Diana
    :Versión:   A9.1

    ---------------------------------------------------------------------------
"""

# --- Módulos estándard
from std.tinyDB import Registro


# --- Módulos de ZEUS
from olimpo import ZEUS


# --- Módulos propios
from . import const as K


#
def HELIOS_init(obj: object) -> None:
    """
    :Propósito:
        Contiene todo el ``__init__`` efectivo de ``HELIOS``, para liberar la
        carga de memoria de este. Recibe a ``HELIOS`` como objeto abstracto,
        así que sólo ``HELIOS`` la debería llamar.
    """

    # --- Especiales
    #
    #
    obj.EstablecerCTRL(obj._ClaseHelios__SOY, K.SOY)
    obj.EstablecerCTRL(obj._ClaseHelios__VERSION, K.VERSION)

    #
    # --- Montar PAQUETE
    #
    # --- TUPLAS con campos bool, int y float y descriptivos
    obj.EstablecerCTRL(obj.BOOLS, (obj._ClaseHelios__DFZV,
                                   obj._ClaseHelios__DFZW,
                                   obj._ClaseHelios__DFZX)
                       )

    obj.EstablecerCTRL(obj.INTS, (obj._ClaseHelios__DA1,
                                  obj._ClaseHelios__DA2,
                                  obj._ClaseHelios__DA3,
                                  obj._ClaseHelios__DA4,
                                  obj._ClaseHelios__DA5)
                       )

    # obj.EstablecerCTRL(obj.FLOAT, False)
    obj.EstablecerCTRL(obj.DESCR, (obj._ClaseHelios__DYZ0,
                                   obj._ClaseHelios__DYZ1,
                                   obj._ClaseHelios__DYZ3,
                                   obj._ClaseHelios__DYZ5,
                                   obj._ClaseHelios__DFZT,
                                   obj._ClaseHelios__DA0)
                       )

    # --- Registro prototipo
    obj.MontarPROTO(
        {
            obj._ClaseHelios__D0Z: K.VERSION,

            obj._ClaseHelios__DA0: ((ZEUS.getSepJson) + " Última medición"),
            obj._ClaseHelios__DA1: 0,
            obj._ClaseHelios__DA2: 0,
            obj._ClaseHelios__DA3: 0,
            obj._ClaseHelios__DA4: 0,
            obj._ClaseHelios__DA5: 0,

            obj._ClaseHelios__DFZT: ((ZEUS.getSepJson) + " Decoradores"),
            obj._ClaseHelios__DFZV: True,
            obj._ClaseHelios__DFZW: True,
            obj._ClaseHelios__DFZX: True,
            obj._ClaseHelios__DFZY: K.DEC_UN_3,
            obj._ClaseHelios__DFZZ: K.DEC_DOS_3,

            obj._ClaseHelios__DYZ0: ((ZEUS.getSepJson) + " Fotometría"),
            obj._ClaseHelios__DYZ1: ((ZEUS.getSepJsonCorto) + " Aperturas"),
            obj._ClaseHelios__DYZ2: {},

            obj._ClaseHelios__DYZ3: ((ZEUS.getSepJsonCorto) +
                                     " Tiempos exposición"),

            obj._ClaseHelios__DYZ4: {},
            obj._ClaseHelios__DYZ5: ((ZEUS.getSepJsonCorto) + " ISO's"),
            obj._ClaseHelios__DYZ6: {}
        }
    )

    # --- BD, Tabla y KEY del registro
    obj.BD = ZEUS.BD
    obj.EstablecerCTRL(obj.TABLA, ZEUS.getFileConf)
    obj.EstablecerCTRL(obj.KEY, K.SOY)


#
class ClaseHelios(Registro):
    """ :Propósito: Clase manejadora de Helios.

    .. note::
        Aunque no utiliza una estructura de diseño **Singleton**, si se
        instancia más de un objeto ``HELIOS``, todos apuntarán a las mismas
        propiedades de clase (ya que reconvierte las propiedades de
        ``EnteDatos`` a propiedades de su propia clase) y tendrán el mismo
        comportamiento.
    """

    __slots__ = []

    __mg = {
        "msg": "Cambiados los decoradores y/o su comportamiento"
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
    # --- Datos generales
    __D0Z = "0Z_Vers"

    # --- Última medición efectiva
    __DA0 = "A0"               # --- Separador visual
    __DA1 = "A1_f"
    __DA2 = "A2_T/V"
    __DA3 = "A3_ISO"
    __DA4 = "A4_Libre"
    __DA5 = "A5_Cam"

    # --- Personalización fotometría
    __DYZ0 = "YZ0"             # --- Separador visual
    __DYZ1 = "YZ1"             # --- Texto Separador Aperturas
    __DYZ2 = "YZ2"             # --- Aperturas
    __DYZ3 = "YZ3"             # --- Texto Separador Tiempos
    __DYZ4 = "YZ4"             # --- Tiempos de exposición
    __DYZ5 = "YZ5"             # --- Texto Separador ISO's
    __DYZ6 = "YZ6"             # --- ISO's
    __DFZT = "FZT"             # --- Separador visual
    __DFZV = "FZV_Dec_TV"      # --- Decorar los T/V
    __DFZW = "FZW_Prio_Dec"    # --- Priorizar uso de decoradores
    __DFZX = "FZX_Usa"         # --- Usar decoradores
    __DFZY = "FZY_UN_3"        # --- Decorador de un tercio
    __DFZZ = "FZZ_DOS_3"       # --- Decorador de dos tercios

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
            HELIOS_init(self)
            self.LeerRegistro()

    #
    # --- Métodos públicos
    #
    #
    #
    def f(self, TERCIO: int) -> str:
        """ Ofrece el texto de la apertura de un tercio específico. """
        # --- Como va a tener mucho uso, se evitan ciclos de código
        return self.PAQUETE[self.REG][self.__DYZ2][TERCIO]

    #
    def T_V(self, TERCIO: int) -> str:
        """ Ofrece el texto del T/V de un tercio específico. """
        # --- Como va a tener mucho uso, se evitan ciclos de código
        return self.PAQUETE[self.REG][self.__DYZ4][TERCIO]

    #
    def ISO(self, TERCIO: int) -> str:
        """ Ofrece el texto del ISO de un tercio específico. """
        # --- Como va a tener mucho uso, se evitan ciclos de código
        return K.ISOS[TERCIO]

    #
    # --- Propiedades Especiales
    #
    #
    #
    @property
    def getSoy(self) -> str:
        """ Evitar Helios como palabra mágica. """
        return self.DevolverCTRL(self.__SOY)

    @property
    def getVersion(self) -> str:
        """ Versión actual de Helios. """
        return self.DevolverCTRL(self.__VERSION)

    #
    # --- Propiedades REG
    #
    #
    # --- Última medición
    @property
    def ultimo_f(self) -> int:
        """ Ultimo f/ utilizado. """
        return self.DevolverREG(self.__DA1)

    @ultimo_f.setter
    def ultimo_f(self, dato):
        self.EstablecerREG(self.__DA1, dato)

    #
    @property
    def ultimo_T_V(self) -> int:
        """ Ultimo T/V utilizado. """
        return self.DevolverREG(self.__DA2)

    @ultimo_T_V.setter
    def ultimo_T_V(self, dato):
        self.EstablecerREG(self.__DA2, dato)

    #
    @property
    def ultimo_ISO(self) -> int:
        """ Ultimo ISO utilizado. """
        return self.DevolverREG(self.__DA3)

    @ultimo_ISO.setter
    def ultimo_ISO(self, dato):
        self.EstablecerREG(self.__DA3, dato)

    #
    @property
    def liberado(self) -> int:
        """ Obtener / Establecer la razón fotométrica que está liberada. """
        return self.DevolverREG(self.__DA4)

    @liberado.setter
    def liberado(self, dato):
        self.EstablecerREG(self.__DA4, dato)

    #
    # --- Fotometría
    @property
    def getAperturas(self) -> tuple:
        """ Tupla con el valor personalizado de las aperturas. """
        return self.DevolverREG(self.__DYZ2)

    #
    @property
    def getTiempos(self) -> tuple:
        """ Tupla con el valor personalizado de los tiempos de exposición. """
        return self.DevolverREG(self.__DYZ4)

    #
    @property
    def getIsos(self) -> tuple:
        """ Tupla con el valor personalizado de los ISO's. """
        return self.DevolverREG(self.__DYZ6)

    #
    # --- Decoradores
    @property
    def esDecoradorActivo(self) -> bool:
        """ Obtener / Establecer si están activos los decoradores. """
        return self.DevolverREG(self.__DFZX)

    @esDecoradorActivo.setter
    def esDecoradorActivo(self, dato):
        if (self.DevolverREG(self.__DFZX) != dato):
            # --- Vamos a guardar y a generar un log
            self.EstablecerREG(self.__DFZX, dato)
            self.GuardarRegistro()
            ZEUS.log_INFO(self.DevolverCTRL(self.ENTE), self.__mg["msg"])
            self.GuardarRegistro()

    #
    @property
    def esDecoradoTV(self) -> bool:
        """
        Obtener / Establecer si se decorarán los tiempos de exposición.
        """
        return self.DevolverREG(self.__DFZV)

    @esDecoradoTV.setter
    def esDecoradoTV(self, dato):
        if (self.DevolverREG(self.__DFZV) != dato):
            # --- Vamos a guardar y a generar un log
            self.EstablecerREG(self.__DFZV, dato)
            self.GuardarRegistro()
            ZEUS.log_INFO(self.DevolverCTRL(self.ENTE), self.__mg["msg"])
            self.GuardarRegistro()

    #
    @property
    def esDecoradorPrioritario(self) -> bool:
        """
        Obtener / Establecer si se usan antes los decoradores a los valores
        tradicionales.
        """
        return self.DevolverREG(self.__DFZW)

    @esDecoradorPrioritario.setter
    def esDecoradorPrioritario(self, dato):
        if (self.DevolverREG(self.__DFZW) != dato):
            # --- Vamos a guardar y a generar un log
            self.EstablecerREG(self.__DFZW, dato)
            self.GuardarRegistro()
            ZEUS.log_INFO(self.DevolverCTRL(self.ENTE), self.__mg["msg"])
            self.GuardarRegistro()

    #
    @property
    def decUnTercio(self) -> str:
        """ Obtener / Establecer el decorador para 1/3. """
        return self.DevolverREG(self.__DFZY)

    @decUnTercio.setter
    def decUnTercio(self, dato):
        if (self.DevolverREG(self.__DFZY) != dato):
            # --- Vamos a guardar y a generar un log
            self.EstablecerREG(self.__DFZY, dato)
            self.GuardarRegistro()
            ZEUS.log_INFO(self.DevolverCTRL(self.ENTE), self.__mg["msg"])
            self.GuardarRegistro()

    #
    @property
    def decDosTercios(self) -> str:
        """ Obtener / Establecer el decorador para 2/3.. """
        return self.DevolverREG(self.__DFZZ)

    @decDosTercios.setter
    def decDosTercios(self, dato):
        if (self.DevolverREG(self.__DFZZ) != dato):
            # --- Vamos a guardar y a generar un log
            self.EstablecerREG(self.__DFZZ, dato)
            self.GuardarRegistro()
            ZEUS.log_INFO(self.DevolverCTRL(self.ENTE), self.__mg["msg"])
            self.GuardarRegistro()
