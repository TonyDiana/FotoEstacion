#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Constantes globales de ZEUS para el inicio. Se ofrecen separadas de
        ZEUS, para facilitar la adaptación futura, pero ningún otro ente lo
        utilizará, salvo ZEUS.

    :Autor:     Tony Diana
    :Versión:   A8.2

    ---------------------------------------------------------------------------
"""
# -----------------------------------------------------------------------------
#   Dejar esto aquí para recordar siempre cómo podemos hacer
#                  from olimpo.const import *
#   No importa si nunca en la vida lo uso. Recordar que tiene que estar al final
#   con todas las variables que se desean enviar (o recibir al importar)
#
# __all__ = [ 'DEC_UN_3', 'DEC_DOS_3' ]
# -----------------------------------------------------------------------------

# --- Módulos estándard
from std.yaml import EnteYaml


# --- Versión de ZEUS
from .version import VERSION


# --- Identidad
SOY: str = VERSION  # --- Evitar flake8 F401 de la constante VERSION
SOY: str = "zeus"

KOMUN: str = "olimpo"
FILE_CONFIG: str = "./CONFIG"

# --- Servidor i-SMTP
iSMTP = "./ismtp"   # --- Modo Debug.
# iSMTP = False       # --- Modo normal.


# --- Path's y archivos
#
#
#
global PATH_INI, PATH_BD, PATH_AYUDA, PATH_DE_TEMAS, FL_CONF, JS_SEP
PATH_INI = "./"
PATH_BD = "bd/"
NOMBRE_BD = "BD"
PATH_AYUDA = "../manual/html"
PATH_DE_TEMAS = "../temas"
FL_CONF = "conf"    # --- Nombre de los archivos de configuración
JS_SEP = 30         # --- Tamaño del separador json


# --- Para los logs
global LOG_ERROR, LOG_INFO
LOG_ERROR = "log.csv"
LOG_INFO = LOG_ERROR    # --- De momento, el mismo


# --- Aspecto
#
#
#
TEMA = "Dark480"


#
class ConfigSYS(EnteYaml):
    """ :Propósito: Leer el archivo de configuración o montarlo. """

    __slots__ = []

    # --- Compatibles con EnteDatos
    #
    #
    # --- Datos de la versión
    __DA0 = "A0"                # --- Separador visual
    __DA1 = "A1_Versión"

    # --- Path's
    __DB0 = "B0"                # --- Separador visual
    __DB1 = "B1_PathINI"
    __DB2 = "B2_PathBD"
    __DB3 = "B3_PathAyuda"
    __DB4 = "B4_PathTemas"
    __DB5 = "B5_FilesConf"
    __DB6 = "B6_SepJson"
    __DB7 = "B2_NombreBD"

    # --- Archivos de log
    __DC0 = "C0"                # --- Separador visual
    __DC1 = "C1_LogError"
    __DC2 = "C2_LogInfo"

    #
    def __init__(self):

        EnteYaml.__init__(self)

        # --- Montar PAQUETE
        #
        # --- TUPLAS con campos bool, int y float y descriptivos
        #   self.EstablecerCTRL(self.BOOLS, False)
        #   self.EstablecerCTRL(self.INTS, False)
        #   self.EstablecerCTRL(self.FLOAT, False)
        self.EstablecerCTRL(self.DESCR, (self.__DA0, self.__DB0, self.__DC0))

        # --- Registro prototipo
        self.MontarPROTO(
            {self.__DA0: (("_" * JS_SEP) + " Aspectos Generales"),
             self.__DA1: VERSION,

             self.__DB0: (("_" * JS_SEP) + " Carpetas / Path's"),
             self.__DB1: PATH_INI,
             self.__DB2: PATH_BD,
             self.__DB3: PATH_AYUDA,
             self.__DB4: PATH_DE_TEMAS,
             self.__DB5: FL_CONF,
             self.__DB6: JS_SEP,
             self.__DB7: NOMBRE_BD,
             self.__DC0: (("_" * JS_SEP) + " Archivos de registro / logs"),
             self.__DC1: LOG_ERROR,
             self.__DC2: LOG_INFO
             })

        # --- Identidad
        aux = __name__ + "." + self.__class__.__name__
        self.EstablecerCTRL(self.ENTE, aux)
        del aux

        # --- Path y archivo de configuración.
        self.EstablecerCTRL(self.FILE, FILE_CONFIG)
        self.LeerRegistro()
        self.GuardarRegistro()

    #
    # --- Propiedades REG
    #
    #
    @property
    def getVersion(self):
        return self.DevolverREG(self.__DA1)

    @property
    def getPathINI(self):
        return self.DevolverREG(self.__DB1)

    @property
    def getPathBD(self):
        return self.DevolverREG(self.__DB2)

    @property
    def getPathHELP(self):
        return self.DevolverREG(self.__DB3)

    @property
    def getPathTemas(self):
        return self.DevolverREG(self.__DB4)

    @property
    def getFileConf(self):
        return self.DevolverREG(self.__DB5)

    @property
    def getSepJson(self):
        return self.DevolverREG(self.__DB6)

    @property
    def getNombreBD(self):
        return self.DevolverREG(self.__DB7)

    @property
    def getFileLogERROR(self):
        return self.DevolverREG(self.__DC1)

    @property
    def getFileLogINFO(self):
        return self.DevolverREG(self.__DC2)
