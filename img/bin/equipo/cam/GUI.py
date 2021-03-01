#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: GUI de una cámara fotográfica.
    :Autor:     Tony Diana
    :Versión:   A15.1

    ---------------------------------------------------------------------------
"""
# -----------------------------------------------------------------------------
# Mapa de señales
# stack_sensor_interactivo --- Señal value-changed --- Ancho y alto del sensor
#                                          changed --- Factor CoC
# stack_identidad_interactivo ---          changed --- tip_cam
# -----------------------------------------------------------------------------


# --- Módulos estandard
from std.gtk import Ventana
from std.disco import add_paths
from std.ismtp import ClassMail


# --- Deidades
from olimpo import ZEUS


# --- Módulos propios
from . import const as KCAM
from .. import const as KEQ
from .kernel import ClassCAM


#
class MailGUICam(ClassMail):
    """
    :Propósito: Clase para enviar i-mails al GUI de cámaras fotográficas.

    :param KEY: KEY de la cámara a procesar. ``None`` o ``False`` = Nueva.
    :type KEY: str

    :param ID: ID de la cámara a procesar o ``None``
    :type ID: int

    :param auto: Si el mail es auto-iMail. Por defecto no.
    :type auto: bool

    :param send: Si enviar inmediatamente.
    :type auto: bool
    """

    __slots__ = []

    # --- Cuerpo del i-Mail
    __KEY = "K"     # --- KEY de cámara a procesar
    __ID = "I"     # --- ID de cámara a procesar

    #
    def __init__(self,
                 KEY: str = False,
                 ID: int = 0,
                 auto: bool = False,
                 send: bool = False):

        # --- 1º montamos el mail sin enviar todavía
        ClassMail.__init__(self)

        # --- Identidad
        aux = __name__ + "." + self.__class__.__name__
        self.EstablecerCTRL(self.ENTE, aux)
        del aux

        # --- Registro prototipo, por defecto nada
        self.MontarPROTO(
            {
                # --- Por defecto nada
                self.__KEY: None,
                self.__ID: None,
            })

        # --- Cuerpo del mensaje
        self.clave = KEY
        self.id = ID

        if auto:
            self.AutoMail()

        if send:
            self.EnviarMail()

    #
    # --- Respuestas
    #
    #
    @property
    def clave(self):
        """ CLAVE de la cámara. """
        return self.DevolverREG(self.__KEY)

    @clave.setter
    def clave(self, valor):
        self.EstablecerREG(self.__KEY, valor)

    #
    @property
    def id(self):
        """ ID en la BD de la cámara. """
        return self.DevolverREG(self.__ID)

    @id.setter
    def id(self, valor):
        self.EstablecerREG(self.__ID, valor)


#
class GUI(Ventana):
    """
    :Propósito:
        Clase manejadora del GUI de una cámara. Busca un i-Mail con
        instrucciones. Si no recibe nada, crea una cámara nueva. Con dicho
        propósito crea un objeto ``ClassCAM`` propio.

    """

    __slots__ = ["cam", "help", "inter"]

    #
    # --- Razones fotométricas propias
    __ISOS: list = []

    #
    # --- Palabras mágicas
    __mg = {
        # --- Índice de la ayuda
        # CAM_HOME

        # --- ComboBox / ListStores
        "tc": ("tip_cam", "tipos_camaras"),
        "fc": ("fac_CoC", "factores_CoC"),
        "isom": ("iso_min", "iso_mi"),
        "isoM": ("iso_max", "iso_ma"),

        # --- GtkEntry's
        # DIAG, NORMAL, FAC_FF, COC

        "name": "NAME",
        "comm": "COMM",

        "w": "ANCHO",
        "h": "ALTO",

        "exp": "AJUSTE",

        "shut": "SHUTTER",
        "flash": "FLASH",
        "sleep": "DESCO",
        "sleep_t": "DESCO_T",

        # --- REPETICIÓN PARA NO COMPLICAR EL CÓDIGO
        "espejo": "ESPEJO",
        "esp_time": "ESPEJO_T",
        # --- Para ocultar o mostrar el espejo
        "esp": ("ESP2", "ESP3", "ESPEJO", "ESPEJO_T"),

        # --- Archivos glade asociados
        # cam.glade, MAIN
    }

    #
    def __init__(self):

        # --- Montar las razones fotométricas en la clase, sólo una vez
        if not(self.__class__.__ISOS):
            i: int = 0
            for x in KCAM.ISOS:
                aux: tuple = (i, x)
                self.__class__.__ISOS.append(aux)
                i += 1
            del i, x, aux

        # --- Desactivar los eventos interactivos GTK
        self.inter: bool = False

        # --- Objeto cámara a manejar
        self.cam: object = ClassCAM(BD=ZEUS.BD)

        # --- Marcadores globales de cargas diferidas de glade
        self.help: bool = True

        # --- Crear ventana, 1º lista de glades
        path1: str = add_paths(ZEUS.getPathTema, KEQ.SOMOS, "cam.glade")
        path2: str = ZEUS.getFileCSS

        Ventana.__init__(self, fileGlade=path1, fileCss=path2)
        del path1, path2

        # --- Tomar la ventana principal, conectar señales y mostrar
        self.ConectarSignals(self)
        self.win = self.GUI("MAIN")
        self.win.show()

        # --- Busquemos un i-mail con instrucciones
        mail = MailGUICam()
        if mail.RecibirMailYBorrar():
            if mail.clave or mail.id:
                self.cam.id = mail.id
                self.cam.nombre = mail.clave
                self.cam.LeerRegistro()

        # --- Montamos los ComboBox, una sola vez
        self.montar_combos()

        # --- En esta GUI vamos a alimentar todos los datos siempre
        self.set_stack_identidad()
        self.set_stack_sensor()
        self.set_stack_sensor_calc()
        self.set_stack_tiempos()

        # --- Activamos la interactividad
        self.inter = True

        # --- Saltará a sg_gen_usu_realice por eventos GTK

    #
    # --- Propiedades calculadas
    #
    #
    # --- Tupla de isos para GUI's.
    @property
    def getISOS(self):
        return self.__ISOS

    #
    # --- Mostrar datos
    #
    #
    # --- Montar ComboBox
    def montar_combos(self):
        self.MontarCombo(self.__mg["tc"],
                         KCAM.TipoCamara.tiposAtupla,
                         self.cam.tipoCam)

        self.MontarCombo(self.__mg["fc"],
                         KCAM.FactoresCoC.factoresAtupla,
                         self.cam.factorCoC)

        self.MontarCombo(self.__mg["isom"],
                         self.getISOS,
                         self.cam.ISOmin)

        self.MontarCombo(self.__mg["isoM"],
                         self.getISOS,
                         self.cam.ISOmAX)

    # --- Stack de identidad
    def set_stack_identidad(self):
        self.SetTexto(self.__mg["name"], self.cam.nombre)
        self.SetTexto(self.__mg["comm"], self.cam.comentario)

        # --- Mostrar u ocultar espejo
        self.Visibilidad(self.__mg["esp"],
                         KCAM.TipoCamara.esConEspejo(self.cam.tipoCam))

    #
    # --- Stack del sensor
    def set_stack_sensor(self):
        self.SetValor(self.__mg["w"], self.cam.anchoSensor)
        self.SetValor(self.__mg["h"], self.cam.altoSensor)
        self.SetValor(self.__mg["exp"], self.cam.ajusteExpo)

    #
    # --- Stack del sensor, cálculos
    def set_stack_sensor_calc(self):
        self.SetTexto("DIAG", str(self.cam.getDiagonal))
        self.SetTexto("NORMAL", str(self.cam.getObjNormal))
        self.SetTexto("FAC_FF", str(self.cam.getFactorFF))
        self.SetTexto("COC", str(self.cam.getCoC))

    #
    # --- Stack de tiempos
    def set_stack_tiempos(self):
        self.SetValor(self.__mg["shut"], self.cam.shutterlag)
        self.SetValor(self.__mg["flash"], self.cam.sincroFlash)
        self.SetSwitch(self.__mg["sleep"], self.cam.esSleep)
        self.SetValor(self.__mg["sleep_t"], self.cam.sleepTime)
        self.SetSwitch(self.__mg["espejo"], self.cam.esEspejo)
        self.SetValor(self.__mg["esp_time"], self.cam.espejoTime)

    #
    # --- Datos interactivos
    #
    #
    # --- Stack de identidad
    def stack_identidad_interactivo(self, *args, **kwargs):
        if self.inter:
            self.get_stack_identidad()
            self.set_stack_identidad()

    # --- Stack del sensor
    def stack_sensor_interactivo(self, *args, **kwargs):
        if self.inter:
            self.get_stack_sensor()
            self.set_stack_sensor_calc()

    #
    # --- Recuperar datos
    #
    #
    # --- Stack de identidad
    def get_stack_identidad(self):
        self.cam.nombre = self.GetTexto(self.__mg["name"])
        self.cam.comentario = self.GetTexto(self.__mg["comm"])
        self.cam.tipoCam = self.GetCombo(self.__mg["tc"][0])

    #
    # --- Stack del sensor
    def get_stack_sensor(self, *args, **kwargs):
        self.cam.anchoSensor = float(self.GetValor(self.__mg["w"]))
        self.cam.altoSensor = float(self.GetValor(self.__mg["h"]))
        self.cam.ajusteExpo = int(self.GetValor(self.__mg["exp"]))
        self.cam.factorCoC = self.GetCombo(self.__mg["fc"][0])
        self.cam.ISOmin = self.GetCombo(self.__mg["isom"][0])
        self.cam.ISOmAX = self.GetCombo(self.__mg["isoM"][0])

    #
    # --- Stack de tiempos
    def get_stack_tiempos(self):
        self.cam.shutterlag = int(self.GetValor(self.__mg["shut"]))
        self.cam.sincroFlash = int(self.GetValor(self.__mg["flash"]))
        self.cam.esSleep = self.GetSwitch(self.__mg["sleep"])
        self.cam.sleepTime = int(self.GetValor(self.__mg["sleep_t"]))
        self.cam.esEspejo = self.GetSwitch(self.__mg["espejo"])
        self.cam.espejoTime = int(self.GetValor(self.__mg["esp_time"]))

    #
    # --- Botones y señales (bt_exit es de la clase heredada)
    #
    #
    # --- Botón OK
    def bt_ok(self, *args, **kwargs):
        # --- Recuperar datos hacia el objeto
        self.get_stack_identidad()
        self.get_stack_sensor()
        self.get_stack_tiempos()

        self.cam.GuardarRegistro(masfecha=True)

        self.bt_exit(*args, **kwargs)

    #
    # --- Solicitar ayuda
    def bt_help(self, *args, **kwargs):

        # --- Si nunca se hizo antes, hay que cargar y conectar señales
        if self.help:
            self.AgregarGlade(ZEUS.getFileGladeHelp)
            self.ConectarSignals(self)
            self.help = False

        self.MostrarUrl(ZEUS.urlHelp("CAM_HOME"))

    #
    # --- Respuestas
    #
    #
    @property
    def getRespuesta(self):
        """ Este menú siempre responde ``False`` """
        return False
