#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejadores de entidades de exposición (EV, f/, T/V, ISO).
    :Autor:     Tony Diana
    :Versión:   A9.1

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
import math


# --- Módulos propios
from olimpo import HELIOS


class AbsEV(object):
    """
    :Propósito: Abastracción máxima de EV's.

    :param ev_min: Mínimo valor de EV posible
    :type ev_min: float

    :param ev_max: Mánimo valor de EV posible
    :type ev_max: float

    :param tercio_max:
        Máxima cantidad de tercios en esos EV's. Debería ser el resultado de
        ``(ev_max - ev_min) * 0.3``, pero es preferible pasar este valor, para
        evitar imprecisiones de redondeo, sobre todo porque tres tercios
        ofrecen 0.9 EV's en valor ``float``, aunque fotográficamente se
        redondean a 1. Si se envía el valor de 0, lo calculará de esa manera,
        pero de debe evitar usar de esta manera, especialmente cuando el máximo
        y/o mínimo EV tengan decimales.
    :type tercio_max: int
    """

    __slots__ = ["__EV_MIN", "__EV_MAX", "__TERCIO_MAX", "__miTercio",
                 "__miEV", "__tercioDecorable", "__textoDecorador"]

    # --- Constantes propias (Quizás un día resolvamos medios pasos)
    KTERCIO = float(1.0 / 3.0)
    KPASOS: int = 3
    KDECIMALES = 6  # --- Decimales de los EV's

    def __init__(self, ev_min: float, ev_max: float, tercio_max: int = 0):

        # --- Propiedades que no deberían variar
        self.__EV_MIN: float = ev_min
        self.__EV_MAX: float = ev_max
        self.__TERCIO_MAX: int = tercio_max

        self.__miTercio: int = 0    # --- Tercio actual, sólo iniciarlo

        # --- Para conocer el EV asociado, en tercio decorable asociado
        self.__tercioDecorable: int = 0
        self.__textoDecorador: str = ""

        # --- Controlar si nó nos informaron de los tercios máximos
        if self.__TERCIO_MAX == 0:
            self.__miev_atercio()

        # --- Y tomar EV=0 por defecto
        self.setEV(0)

    #
    # --- Propiedades públicas
    #
    #
    #
    def setEV(self, nuevoEV: float) -> bool:
        """
        :Propósito:
            Establecer un EV como el EV actual. Devuelve ``True`` si lo logra,
            y ``False`` si no es posible, pero siempre tomará un nuevo valor,
            el EV realmente posible. Luego transforma ese EV en el TERCIO
            correspondiente.

        :param nuevoEV:  Nuevo EV pretendido.
        :type nuevoEV: float
        """
        self.__miEV: float = nuevoEV
        resp: bool = True

        # --- Verificar rangos
        if (self.__miEV < self.__EV_MIN):
            self.__miEV = self.__EV_MIN
            resp = False

        elif (self.__miEV > self.__EV_MAX):
            self.__miEV = self.__EV_MAX
            resp = False

        # --- Obtener el nuevo TERCIO y seguir
        self.__miev_atercio()
        return resp

    #
    def setTERCIO(self, nuevoTercio: int) -> bool:
        """
        :Propósito:
            Establecer el TERCIO actual. Devuelve ``True`` si lo logra, y
            ``False`` si no es posible, pero siempre tomará un nuevo valor, el
            TERCIO realmente posible.

            Luego transforma ese TERCIO en el EV correspondiente.

        :param nuevotercio: Nuevo TERCIO pretendido
        :type nuevotercio: int
        """
        resp: bool = True

        # --- Verificar que está entre 0 y el máximo valor posible
        if (nuevoTercio < 0):
            self.__miTercio = 0
            resp = False

        else:
            self.__miTercio = nuevoTercio

            if (self.__miTercio > self.__TERCIO_MAX):
                self.__miTercio = self.__TERCIO_MAX
                resp = False

        # --- Sólo resta acomodar y devolver el resultado
        self.__mitercio_aev()
        self.__decorar()
        return resp

    #
    # --- Métodos públicos
    #
    #
    #
    def GanarTERCIOS(self, tercios: int = 1) -> bool:
        """
            Ganar varios TERCIOS de luz, por defecto 1.
        """
        return self.setTERCIO(self.__miTercio - tercios)

    #
    def PerderTERCIOS(self, tercios: int = 1) -> bool:
        """
            Perder varios TERCIOS de luz, por defecto 1.
        """
        return self.setTERCIO(self.__miTercio + tercios)

    #
    # --- Atributos
    #
    #
    #
    @property
    def getEV(self) -> float:
        """ Obtener el EV actual """
        return self.__miEV

    #
    @property
    def getTERCIO(self) -> int:
        """ Obtener el TERCIO actual """
        return self.__miTercio

    #
    @property
    def getTERCIOdecorado(self) -> tuple:
        """
            Devuelve una tupla con el TERCIO decorable y  el texto
            del decorador.
        """
        return (self.__tercioDecorable, self.__textoDecorador)

    #
    # --- Métodos privados
    #
    #
    # --- Convertir MI EV a TERCIO, evitando imprecisión matemática
    def __miev_atercio(self):
        # --- Cabe recordar que el EV mínimo representa self.__miTercio = 0
        self.__miTercio = int((self.__miEV - self.__EV_MIN) /
                              self.KTERCIO + 0.1)
        self.__decorar()

    #
    # --- Convertir mi TERCIO a EV
    # --- OJO: MATEMÁTICAS BÁSICAS, en este contexto se suma el negativo
    def __mitercio_aev(self):
        self.__miEV = float(self.__miTercio * self.KTERCIO) + self.__EV_MIN
        self.__miEV = round(self.__miEV, self.KDECIMALES)

    #
    # --- Calcular el tercio decorado y el decorador
    def __decorar(self):
        self.__textoDecorador = ""

        # --- Dividir en grupos de KPASOS (Por defecto 3)
        self.__tercioDecorable = math.floor(self.__miTercio / self.KPASOS)
        self.__tercioDecorable *= self.KPASOS

        # --- Cuando no coinciden es cuando hay que decorar
        if (self.__miTercio != self.__tercioDecorable):
            if ((self.__miTercio - self.__tercioDecorable) == 1):
                self.__textoDecorador = HELIOS.decUnTercio
            else:
                self.__textoDecorador = HELIOS.decDosTercios


#
class f(AbsEV):
    """
        :Propósito:
            Manejador de una apertura.

        :param TERCIO:
            TERCIO que debe tomar por defecto. Si no recibe ninguno hará caso
            al parametro ``EV``, pero si recibe alguno omitirá ese parámetro.

        :param EV:
            EV inicial, el cual sólo tomará en caso de no recibir ningún
            ``TERCIO``. En caso de no recibirlo, toma ``EV = 0`` como
            valor inicial (Se encarga ``AbsEV`` de ello).

    Las aperturas se establecen por la letra **f** minúscula, ya que la
    letra **F** mayúscula representa la distancia focal, y la apertura del
    diafragma es una relación entre la division de la distancia focal por
    el resultado de la sqrt(2).

    Usar **F** mayúscula para indicar la apertura es una barbaridad y me niego
    a hacerlo.
    """

    __slots__ = []

    # --- Constantes propias
    __EV_MIN: float = 0.0
    __EV_MAX: float = 14.0
    __EV_TER: int = 42

    #
    def __init__(self, TERCIO: int = False, EV: float = False):
        # --- Propiedades que no deberían variar
        AbsEV.__init__(self, self.__EV_MIN, self.__EV_MAX, self.__EV_TER)

        # --- Analizar parámetros
        if TERCIO:
            self.setTERCIO(TERCIO)

        elif EV:
            self.setEV(EV)

    #
    # --- Atributos
    #
    #
    #
    @property
    def getTexto(self) -> str:
        """ Obtener el texto del EV/TERCIO asociado """
        return ("f/" + HELIOS.f(self.getTERCIO))

    #
    @property
    def getTextoDecorado(self) -> str:
        """ Obtener el texto del EV/TERCIO asociado con decorador """
        _tercio, _decorador = self.getTERCIOdecorado
        return ("f/" + HELIOS.f(_tercio) + _decorador)


#
class T_V(AbsEV):
    """
        :Propósito:
            Manejador de un tiempo de exposición.

        :param TERCIO:
            TERCIO que debe tomar por defecto. Si no recibe ninguno hará caso
            al parametro ``EV``, pero si recibe alguno omitirá ese parámetro.

        :param EV:
            EV inicial, el cual sólo tomará en caso de no recibir ningún
            ``TERCIO``. En caso de no recibirlo, toma ``EV = 0`` como
            valor inicial (Se encarga ``AbsEV`` de ello).
    """

    __slots__ = []

    # --- Constantes propias
    __EV_MIN: float = -6.0
    __EV_MAX: float = 13.0
    __EV_TER: int = 57

    #
    def __init__(self, TERCIO: int = False, EV: float = False):
        # --- Propiedades que no deberían variar
        AbsEV.__init__(self, self.__EV_MIN, self.__EV_MAX, self.__EV_TER)

        # --- Analizar parámetros
        if TERCIO:
            self.setTERCIO(TERCIO)

        elif EV:
            self.setEV(EV)

    #
    # --- Atributos
    #
    #
    #
    @property
    def getTexto(self) -> str:
        """ Obtener el texto del EV/TERCIO asociado """
        return ("T/V " + HELIOS.T_V(self.getTERCIO))

    #
    @property
    def getTextoDecorado(self) -> str:
        """ Obtener el texto del EV/TERCIO asociado con decorador """
        _tercio, _decorador = self.getTERCIOdecorado
        return ("T/V " + HELIOS.T_V(_tercio) + _decorador)


#
class ISO(AbsEV):
    """
        :Propósito:
            Manejador de las sensibilidades.

        :param TERCIO:
            TERCIO que debe tomar por defecto. Si no recibe ninguno hará caso
            al parametro ``EV``, pero si recibe alguno omitirá ese parámetro.

        :param EV:
            EV inicial, el cual sólo tomará en caso de no recibir ningún
            ``TERCIO``. En caso de no recibirlo, toma ``EV = 0`` como
            valor inicial (Se encarga ``AbsEV`` de ello).
    """

    __slots__ = []

    # --- Constantes propias
    __EV_MIN: float = -2.0
    __EV_MAX: float = 10.0
    __EV_TER: int = 36

    #
    def __init__(self, TERCIO: int = False, EV: float = False):
        # --- Propiedades que no deberían variar
        AbsEV.__init__(self, self.__EV_MIN, self.__EV_MAX, self.__EV_TER)

        # --- Analizar parámetros
        if TERCIO:
            self.setTERCIO(TERCIO)

        elif EV:
            self.setEV(EV)

    #
    # --- Métodos públicos
    #
    #
    #
    def GanarTERCIOS(self, tercios: int = 1) -> bool:
        """
            Ganar varios TERCIOS de luz, por defecto 1. Sobreescribe
            el método de ``AbsEV``, porque su comportamiento es diferente
        """
        return AbsEV.PerderTERCIOS(tercios)

    #
    def PerderTERCIOS(self, tercios: int = 1) -> bool:
        """
            Perder varios TERCIOS de luz, por defecto 1. Sobreescribe
            el método de ``AbsEV``, porque su comportamiento es diferente
        """
        return AbsEV.GanarTERCIOS(tercios)

    #
    # --- Atributos
    #
    #
    #
    @property
    def getTexto(self) -> str:
        """ Obtener el texto del EV/TERCIO asociado """
        return ("ISO " + HELIOS.ISO(self.getTERCIO))

    #
    @property
    def getTextoDecorado(self) -> str:
        """ Obtener el texto del EV/TERCIO asociado con decorador """
        _tercio, _decorador = self.getTERCIOdecorado
        return ("ISO " + HELIOS.ISO(_tercio) + _decorador)
