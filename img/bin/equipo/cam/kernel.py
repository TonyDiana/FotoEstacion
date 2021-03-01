#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Kernel del manejo de las cámaras.

    :Autor:     Tony Diana
    :Versión:   A15.1

    ---------------------------------------------------------------------------
"""

# --- Módulos sistema
from math import ceil


# --- Módulos de terceros
from terceros.scp import ClasspropertyMeta, classproperty


# --- Módulos estándard
from std.disco import add_paths
from std.pitagoras import hipotenusa as hipo
from std.tinyDB import Registro, WORD_KEY


# --- Módulos de ZEUS
from olimpo import ZEUS


# --- Contantes
from .. import const as KEQ
from . import const as KCAM


#
class ClassCAM(Registro):
    """
    :Propósito: Clase integral manejador de una cámara.

    :param BD: Puntero a la BD.
    :type unDict: objet

    :param unDict:
        Diccionario o json con los datos de la cámara. Falso
        indicaría que se desea gestionar una cámara nueva.
    :type unDict: dict

    :param KEY:
        Clave de la cámara en la BD. Falso indicaría que se desea gestionar
        una cámara nueva.
    :type unDict: str

    :param ID:
        ID de la cámara en la BD. Falso indicaría que se desea gestionar una
        cámara nueva.
    :type unDict: str

    .. nota::
        El orden de procesado de los parámetros es:
            -1º el diccionario.
            -2º el ID.
            -3º la KEY.
            -4º si nada se recibe, se da de alta una cámara.
    """

    __slots__ = []

    #
    # --- Compatibles con EnteDatos
    #
    # --- Identificación de la cámara
    __B0 = "B0"                 # --- Separador visual
    __B1 = "B1_Vers"
    __B2 = "B2_Tipo"
    __B3 = "B3_Tipo_T"
    __B4 = "B4_Comentario"

    # --- Características
    __C00 = "C00"               # --- Separador visual
    __C01 = "C01_S_ancho"
    __C02 = "C02_S_alto"
    __C03 = "C03_CoC"
    __C04 = "C04_CoC_T"
    __C05 = "C05_ISO_m"
    __C06 = "C06_ISO_M"
    __C07 = "C07_Shutterlag"
    __C08 = "C08_Sincro_Flash"
    __C09 = "C09_Sleep"
    __C10 = "C10_Sleep_Min"
    __C11 = "C11_Espejo"
    __C12 = "C12_Espejo_Milis"
    __C13 = "C13_Expo"

    #
    def __init__(self,
                 BD: object = False,
                 unDict: dict = False,
                 KEY: str = False,
                 ID: int = False):

        Registro.__init__(self, BD=BD)

        #
        # --- Montar PAQUETE
        #
        # --- TUPLAS con campos bool, int y float y descriptivos
        self.EstablecerCTRL(self.BOOLS, (self.__C09, self.__C11))

        self.EstablecerCTRL(self.INTS, (self.__C03, self.__C05, self.__C06,
                                        self.__C07, self.__C08, self.__C10,
                                        self.__C13))

        self.EstablecerCTRL(self.FLOAT, (self.__C01, self.__C02))
        self.EstablecerCTRL(self.DESCR, (self.__B0, self.__C00))

        # --- Registro prototipo
        x = KCAM.TipoCamara.frontera - 1   # --- DSLR
        y = 1443    # --- Dof Master por defecto

        self.MontarPROTO(
            {
                self.__B0: (ZEUS.getSepJson + " Identificación"),
                self.__B1: KCAM.VERS,
                self.__B2: x,
                self.__B3: KCAM.TipoCamara.Nombrar(x),
                self.__B4: "",

                self.__C00: (ZEUS.getSepJson + " Características"),
                self.__C01: 36.0,
                self.__C02: 24.0,

                self.__C03: y,
                self.__C04: KCAM.FactoresCoC.Nombrar(y),

                self.__C05: 6,      # --- ISO  100
                self.__C06: 25,     # --- ISO 8000
                self.__C07: 59,
                self.__C08: 200,
                self.__C09: True,
                self.__C10: 5,
                self.__C11: True,
                self.__C12: 1000,
                self.__C13: 0,
            })

        del x, y

        # --- Identidad
        aux = __name__ + "." + self.__class__.__name__
        self.EstablecerCTRL(self.ENTE, aux)

        aux = KEQ.SOMOS + "." + KCAM.SOY
        self.EstablecerCTRL(self.TABLA, aux)
        del aux

        self.EstablecerCTRL(self.KEY, None)

        # --- Agregar datos, leer datos o buscar
        if unDict:
            # --- Se recibe el diccionario ya leido
            self.Agregar(unDict)
        elif (ID or KEY):
            # --- Se recibió un ID.
            self.EstablecerCTRL(self.ID, ID)
            self.EstablecerCTRL(self.KEY, KEY)
            self.LeerRegistro()

        else:
            # --- Nuevo, tomamos un registro prototipo
            self.Inicializar()
            self.EstablecerCTRL(self.KEY, "Nueva")

    #
    # --- Métodos públicos
    #
    #
    #
    def GuardarRegistro(self, masfecha: bool = False) -> bool:
        """
        Sobreescribe el método de la clase heredada, para primero dejar los
        datos del registro con lógica.

        Luego llama al método de la clase heredada para grabar efectivamente
        el registro.
        """
        self.__integridad()
        Registro.GuardarRegistro(self, masfecha=masfecha)

    #
    def LeerRegistro(self, masfecha: bool = False) -> bool:
        """
        Sobreescribe el método de la clase heredada, para dejar los
        datos del registro con lógica tras leer el registro de la BD.
        """
        Registro.LeerRegistro(self)
        self.__integridad()

    #
    # --- Propiedades REG
    #
    #
    # --- ID del registro
    @property
    def id(self):
        """ Obtener / Establecer el ID en la BD. """
        return self.DevolverCTRL(self.ID)

    @id.setter
    def id(self, dato):
        self.EstablecerCTRL(self.ID, dato)

    # --- Identidad
    @property
    def nombre(self):
        """ Obtener / Establecer el nómbre de la cámara. """
        return self.DevolverCTRL(self.KEY)

    @nombre.setter
    def nombre(self, dato):
        self.EstablecerCTRL(self.KEY, dato)

    #
    @property
    def comentario(self):
        """ Obtener / Establecer el comentario de la cámara. """
        return self.DevolverREG(self.__B4)

    @comentario.setter
    def comentario(self, dato):
        self.EstablecerREG(self.__B4, dato)

    #
    @property
    def tipoCam(self):
        """ Obtener / Establecer el número de tipo de cámara. """
        return self.DevolverREG(self.__B2)

    @tipoCam.setter
    def tipoCam(self, dato):
        self.EstablecerREG(self.__B2, dato)

    #
    # --- Sensor
    @property
    def altoSensor(self):
        """ Obtener / Establecer, el alto del sensor. """
        return self.DevolverREG(self.__C02)

    @altoSensor.setter
    def altoSensor(self, dato):
        self.EstablecerREG(self.__C02, dato)

    #
    @property
    def anchoSensor(self):
        """ Obtener / Establecer el ancho del sensor. """
        return self.DevolverREG(self.__C01)

    @anchoSensor.setter
    def anchoSensor(self, dato):
        self.EstablecerREG(self.__C01, dato)

    #
    @property
    def factorCoC(self):
        """ Obtener / Establecer el factor del círculo de confusión. """
        return self.DevolverREG(self.__C03)

    @factorCoC.setter
    def factorCoC(self, dato):
        self.EstablecerREG(self.__C03, dato)

    #
    @property
    def ISOmin(self):
        """ Obtener / Establecer el ISO mínimo de la cámara. """
        return self.DevolverREG(self.__C05)

    @ISOmin.setter
    def ISOmin(self, dato):
        self.EstablecerREG(self.__C05, dato)

    #
    @property
    def ISOmAX(self):
        """ Obtener / Establecer el ISO máximo de la cámara. """
        return self.DevolverREG(self.__C06)

    @ISOmAX.setter
    def ISOmAX(self, dato):
        self.EstablecerREG(self.__C06, dato)

    #
    # --- Tiempos
    @property
    def shutterlag(self):
        """ Obtener / Establecer el tiempo de Shutterlag. """
        return self.DevolverREG(self.__C07)

    @shutterlag.setter
    def shutterlag(self, valor):
        self.EstablecerREG(self.__C07, valor)

    #
    @property
    def sincroFlash(self):
        """ Obtener / Establecer el tiempo de sincronización del flash. """
        return self.DevolverREG(self.__C08)

    @sincroFlash.setter
    def sincroFlash(self, valor):
        self.EstablecerREG(self.__C08, valor)

    #
    @property
    def esSleep(self):
        """ Obtener / Establecer si está activada la autodesconexión. """
        return self.DevolverREG(self.__C09)

    @esSleep.setter
    def esSleep(self, valor):
        self.EstablecerREG(self.__C09, valor)

    #
    @property
    def sleepTime(self):
        """ Obtener / Establecer el tiempo para autodesconexión. """
        return self.DevolverREG(self.__C10)

    @sleepTime.setter
    def sleepTime(self, valor):
        self.EstablecerREG(self.__C10, valor)

    #
    @property
    def esEspejo(self):
        """ Obtener / Establecer si está activo el levantamiento espejo. """
        return self.DevolverREG(self.__C11)

    @esEspejo.setter
    def esEspejo(self, valor):
        self.EstablecerREG(self.__C11, valor)

    #
    @property
    def espejoTime(self):
        """ Obtener / Establecer el tiempo para levantamiento espejo. """
        return self.DevolverREG(self.__C12)

    @espejoTime.setter
    def espejoTime(self, valor):
        self.EstablecerREG(self.__C12, valor)

    #
    @property
    def ajusteExpo(self):
        """ Obtener / Establecer el ajuste de la exposición. """
        return self.DevolverREG(self.__C13)

    @ajusteExpo.setter
    def ajusteExpo(self, valor):
        self.EstablecerREG(self.__C13, valor)

    #
    # --- Propiedades Calculadas
    #
    #
    #
    @property
    def getDiagonal(self):
        """ Diagonal del sensor. """
        return hipo(self.altoSensor, self.anchoSensor, 2)

    #
    @property
    def getFactorFF(self):
        """ Factor comparación con FF. """
        ff = hipo(36, 24, 2)
        return round((ff / self.getDiagonal), 1)

    #
    @property
    def getCoC(self):
        """ Tamaño del círculo de confusión. """
        return round((self.getDiagonal / (self.factorCoC or 1)), 5)

    #
    @property
    def getObjNormal(self):
        """ Diagonal al alza más 2 por ajuste CANON APS-C. """
        diag = ceil(self.getDiagonal) + 2

        for x in KCAM.OBJ_NORM:
            if x > diag:
                return x

    #
    # --- Métodos privados
    #
    #
    #
    def __integridad(self) -> None:
        # --- Da integridad a los datos, tanto al leer como al grabar
        self.EstablecerREG(self.__B3, KCAM.TipoCamara.Nombrar(self.tipoCam))
        self.EstablecerREG(self.__C04, KCAM.FactoresCoC.Nombrar(self.factorCoC))

        # --- Si es sin espejo, desactivar los valores
        if not(KCAM.TipoCamara.esConEspejo(self.tipoCam)):
            self.esEspejo = False
            self.espejoTime = 0


#
class ListaCAM(object, metaclass=ClasspropertyMeta):
    """
    :Propósito:
        Toma una lista de cámaras de la BD y la gestiona para varios
        propósitos, por eso es un objeto.

        Funciona como clase y no debe instanciarse.

        Dispone de varias propiedades de clase:

        - listaDatos:
            Ofrece una tupla válida para montar un ListStore.

        - fileGlade:
            Ofrecer el path + archivo ``.glade`` de la lista de cámaras.

        - nombreEnGlade:
            Ofrecer el nombre del treeview para evitar palabra mágica. Una vez
            cargado el glade que ofrece la propiedad ``fileGlade`` se debe
            agregar el **Gtk Tree View** en el que se encuentra la lista de las
            cámaras. El **Gtk Tree View** se denomina ``__treeviewDeCamaras__``,
            esta propiedad evita tener que usar esa palabra mágica.

            .. Nota::

                Este archivo ``.glade`` ofrece el evento ``SEL_CAM_changed_cb``
                que reacciona al cambio de cámara seleccionada. Ofrece el
                evento no el código solucionado.

        - GtkListStore:
            Nombre del ``GtkListStore``, evitar palabra mágica.
    """

    __slots__ = []

    # --- Palabras mágicas
    # camlist.glade, __treeviewDeCamaras__, __LST_CAM__

    __LISTA: dict = None

    #
    @classmethod
    def __leer(cls):
        # --- Para minimizar variables y ciclos se acometen los punteros de una
        cls.__LISTA = ZEUS.BD.PtrTabla(KEQ.SOMOS + "." + KCAM.SOY).all()

    #
    @classproperty
    def listaDatos(cls):
        """ Ofrecer los datos para una ListStore. """
        cls.__leer()
        lista: list = []
        for x in cls.__LISTA:
            tupla = (x.doc_id, x[WORD_KEY])
            lista.append(tupla)

        return lista

    #
    @classproperty
    def fileGlade(cls):
        """ Ofrecer el path + archivo ``.glade`` de la lista de cámaras. """
        return add_paths(ZEUS.getPathTema, KEQ.SOMOS, "camlist.glade")

    #
    @classproperty
    def nombreEnGlade(cls):
        """
        Ofrecer el nombre del treeview para evitar palabra mágica. Una vez
        cargado el glade que ofrece la propiedad ``fileGlade`` se debe
        agregar el **Gtk Tree View** en el que se encuentra la lista de las
        cámaras. El **Gtk Tree View** se denomina ``__treeviewDeCamaras__``,
        esta propiedad evita tener que usar esa palabra mágica.

        .. Nota:
        Este archivo ``.glade`` ofrece el evento ``SEL_CAM_changed_cb`` que
        reacciona al cambio de cámara seleccionada. Ofrece el evento no el
        código solucionado.
        """
        return "__treeviewDeCamaras__"

    #
    @classproperty
    def GtkListStore(cls):
        """ Nombre del ``GtkListStore``, evitar palabra mágica. """
        return "__LST_CAM__"
