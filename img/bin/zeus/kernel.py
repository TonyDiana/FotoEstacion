#!/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Kernel de ZEUS.
    :Autor:     Tony Diana
    :Versión:   A15.1

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
import gc   # --- Recolector de basura.


# --- Módulos estándard
from std.datos import auto
from std.disco import add_paths, copydir, mi_path, mkdir
from std import logs
from std.tinyDB import Registro
from std.tinyDB import BDYaml as BDClass
from std.yaml import EnteYaml


# --- Especial porque queremos dar valor a una global
from std import ismtp as IS


# --- Contantes
from . import const as K


#
class ConfTEMA(EnteYaml):
    """
    :Propósito:
        Clase manejadora de la configuración de tema. Sólo es utilizado
        por ZEUS, el cual es el único que lo gestiona.

    :param path: Path + archivo del archivo de configuración a gestionar.
    :type path: string

    :param separa: Separador de json, ya que no puede invocar a ZEUS.
    :type separa: str

    """

    __slots__ = []

    # --- Compatibles con EnteDatos
    #
    #
    # --- Datos de la pantalla
    __DA0 = "A0"               # --- Separador visual
    __DA1 = "A1_HORIZONTAL"    # --- Pixels
    __DA2 = "A2_VERTICAL"

    #
    def __init__(self, path: str, separa: str):

        EnteYaml.__init__(self)

        # --- Montar PAQUETE
        #
        # --- TUPLAS con campos bool, int y float y descriptivos
        #   self.EstablecerCTRL(self.BOOLS, False)
        self.EstablecerCTRL(self.INTS, (self.__DA1, self.__DA2))
        #   self.EstablecerCTRL(self.FLOAT, False)
        self.EstablecerCTRL(self.DESCR, self.__DA0)

        # --- Registro prototipo
        self.MontarPROTO({self.__DA0: (separa + " Pantalla"),
                          self.__DA1: 800,
                          self.__DA2: 480})

        # --- Identidad
        aux = __name__ + "." + self.__class__.__name__
        self.EstablecerCTRL(self.ENTE, aux)
        del aux

        # --- Path y archivo de configuración
        self.EstablecerCTRL(self.FILE, path)
        self.LeerRegistro()

    #
    # --- Propiedades REG
    #
    #
    # --- Tamaño máximo de la ventana en horizontal
    @property
    def horizontal(self) -> int:
        return self.DevolverREG(self.__DA1)

    # --- Tamaño máximo de la ventana en vertical
    @property
    def vertical(self) -> int:
        return self.DevolverREG(self.__DA2)


#
class MsgZEUS(object):
    """
    :Propósito:
        Ofrecer los mensajes de log de ZEUS, sin necesitar que estos estén
        dentro del objeto y facilitar su mantenimiento.
    """
    cambioUsuario = "Cambiado nombre del propietario"
    cambioMail = "Cambiado mail del propietario"
    cambioNube = "Cambiado el comportamiento de las copias en la nube"
    cambioSalir = "Cambiado el comportamiento al salir de ZEUS"


#
class GladesZEUS(object):
    """
    :Propósito:
        Ofrecer los archivos genéricos glade de ZEUS, sin necesitar que estos
        estén dentro del objeto y facilitar su mantenimiento.
    """
    SelCarpeta = "glades/selfolder.glade"
    SelFile = "glades/selfile.glade"
    Confirmar = "glades/confirm.glade"
    HelpWeb = "glades/helpweb.glade"


#
def ZEUS_Nube_BD(objzeus: object, restaurar: bool = False) -> None:
    """
    :Propósito:
        Copiar la base de datos a la nube o restaurar, según el parámetro
        recibido.

        Recibe al propio objeto ZEUS que debe manejarlo.
    """

    # --- Diferenciar entre copia y restauración
    if restaurar:
        _msg = "Restaurada la base de datos de la nube"
        _origen = objzeus.pathNube
        _destino = objzeus.pathBD

    else:
        _msg = "Copiada la base de datos en la nube"
        _origen = objzeus.getPathBD
        _destino = objzeus.pathNube

    # --- Si da error no importa pero no ponemos el contador a cero
    if copydir(_origen, _destino):
        objzeus.log_INFO(objzeus.DevolverCTRL(objzeus.ENTE), _msg)
        objzeus.veces = 0


#
def ZEUS_inicio(objzeus: object) -> None:
    """
    :Propósito:
        Realiza los procesos necesarios para iniciar ZEUS, pero después de
        haber sido creado el objeto ZEUS propiamente dicho. Puesto que sólo
        se utilizará una vez, está fuera de la clase ``ClassZEUS`` para que
        pueda ser eliminado por el recolector de basura, una vez utilizado.

        Recibe al propio objeto ZEUS que debe manejarlo.
    """

    # --- Activar la gestión de log's
    logs.iniciar_logs(objzeus.getFileLogError, objzeus.getFileLogInfo)

    # --- Activar el Recolector de basura
    objzeus.BasuraOn()

    # --- Activar el servidor iSMTP
    IS.iSMTP = IS.iSever(bd=objzeus.getBDiSMTP)

    # --- Sumar una vez más
    objzeus.veces += 1


#
def ZEUS_final(objzeus: object) -> None:
    """
    :Propósito:
        Finaliza a ZEUS y no está dentro de ``ClassZEUS`` porque sólo se usará
        una vez.

        Recibe al propio objeto ZEUS que debe manejarlo.
    """

    # --- Ver las veces que se ha ejecutado y hacer copias en la nube
    if objzeus.esNubeActiva:
        if (objzeus.veces >= objzeus.vecesGuardar):
            ZEUS_Nube_BD(objzeus)


#
def ZEUS_init(objzeus: object) -> None:
    """
    :Propósito:
        Contiene todo el ``__init__`` efectivo de ``ZEUS``, para liberar la
        carga de memoria de este. Recibe a ``ZEUS`` como objeto abstracto,
        así que sólo ``ZEUS`` la debería llamar.
    """

    # --- Leer CONFIG.SYS y montar el registro de memoria
    config = K.ConfigSYS()
    monta1 = add_paths(config.getPathINI, config.getPathBD)

    # --- Aprovechamos para montar el nombre de la BD y crear la carpeta
    monta2 = add_paths(monta1, config.getNombreBD)
    # --- El nombre viene sin extensión, añadimos una para que mkdir no hierre
    mkdir(monta2 + ".txt")

    #
    # --- Montar PAQUETE MEM
    #
    objzeus.MontarMEM(
        {
            objzeus._ClassZEUS__CS1: config.getPathINI,
            objzeus._ClassZEUS__CS2: monta1,
            objzeus._ClassZEUS__CS3: K.VERSION,
            objzeus._ClassZEUS__CS4: config.getPathTemas,
            objzeus._ClassZEUS__CS5: config.getFileConf,
            objzeus._ClassZEUS__CS6: config.getSepJson,
            objzeus._ClassZEUS__CS7: add_paths(monta1, config.getFileLogERROR),
            objzeus._ClassZEUS__CS8: add_paths(monta1, config.getFileLogINFO),

            objzeus._ClassZEUS__Z0: K.SOY,
            objzeus._ClassZEUS__ZU: K.SOY,
            objzeus._ClassZEUS__ZZ: K.KOMUN,

            objzeus._ClassZEUS__BD: monta2,
            objzeus._ClassZEUS__iSMTP: K.iSMTP,
            objzeus._ClassZEUS__CSS: None,
            objzeus._ClassZEUS__REC: False,     # --- Sin recolector de basura
        }
    )

    # --- Borrar los elementos auxiliares
    del config, monta1, monta2

    # --- El path de la ayuda es algo especial
    if (K.PATH_AYUDA[0:1] == "."):
        # --- Es ruta relativa
        path = add_paths(mi_path(), K.PATH_AYUDA)
    else:
        # --- Es ruta absoluta
        path = K.PATH_AYUDA

    objzeus.EstablecerMEM(objzeus._ClassZEUS__CS9, path)
    del path

    #
    # --- Montar PAQUETE CTRL
    #
    # --- TUPLAS con campos bool, int y float y descriptivos
    objzeus.EstablecerCTRL(objzeus.BOOLS, (objzeus._ClassZEUS__DU3,
                                           objzeus._ClassZEUS__DUN4,
                                           objzeus._ClassZEUS__DUN7))

    objzeus.EstablecerCTRL(objzeus.INTS, (objzeus._ClassZEUS__DUN5,
                                          objzeus._ClassZEUS__DUN6))

    # objzeus.EstablecerCTRL(objzeus.FLOAT, False)
    objzeus.EstablecerCTRL(objzeus.DESCR, (objzeus._ClassZEUS__DU0,
                                           objzeus._ClassZEUS__DUN0))

    # --- Registro prototipo
    objzeus.MontarPROTO(
        {
            objzeus._ClassZEUS__D0Z: K.VERSION,
            objzeus._ClassZEUS__DU0: (objzeus.getSepJson + " Usuario"),
            objzeus._ClassZEUS__DU1: "Nombre Propietario",
            objzeus._ClassZEUS__DU2: "Mail propietario",
            objzeus._ClassZEUS__DU3: False,
            objzeus._ClassZEUS__DUN0: (objzeus.getSepJson + " Unidad"),
            objzeus._ClassZEUS__DUN2: K.TEMA,
            objzeus._ClassZEUS__DUN3: "",
            objzeus._ClassZEUS__DUN4: False,
            objzeus._ClassZEUS__DUN5: 0,
            objzeus._ClassZEUS__DUN6: 0,
            objzeus._ClassZEUS__DUN7: True,
        }
    )

    # --- BD, Tabla y KEY del registro
    objzeus.BD = BDClass(objzeus.getNombreBD)
    objzeus.BD.close()
    objzeus.EstablecerCTRL(objzeus.TABLA, objzeus.getFileConf)
    objzeus.EstablecerCTRL(objzeus.KEY, K.SOY)


#
class ClassZEUS(Registro):
    """
    :Propósito:
        Clase manejadora de ZEUS, desde y hacia el disco. Permanece en memoria
        pero puede mutar a lo largo de la ejecución.

    .. note::
        Aunque no utiliza una estructura de diseño **Singleton**, si se
        instancia más de un objeto ``ZEUS``, todos apuntarán a las mismas
        propiedades de clase (ya que reconvierte las propiedades de
        ``EnteDatos`` a propiedades de su propia clase) y tendrán el mismo
        comportamiento.
    """

    __slots__ = []

    # --- Tomar los datos de CONFIG.SYS
    __CS1 = auto()  # --- PATH_INI
    __CS2 = auto()  # --- PATH_BD
    __CS3 = auto()  # --- VERSION
    __CS4 = auto()  # --- PATH_DE_TEMAS
    __CS5 = auto()  # --- FL_CONF
    __CS6 = auto()  # --- JS_SEP
    __CS7 = auto()  # --- LOG_ERROR
    __CS8 = auto()  # --- LOG_INFO
    __CS9 = auto()  # --- PATH_AYUDA
    # --- TEMA se lee en CONFIG.SYS pero es un dato que va en REG

    # --- Otras cosas mezcladas con el CONFIG.SYS
    __Z0 = auto()   # --- ZEUS, para que no sea palabra mágica
    __ZU = auto()   # --- DEIDAD (Zeus usurpado)
    __ZZ = auto()   # --- OLIMPO

    __BD = auto()       # --- BD + PATH_BD montado
    __CSS = auto()      # --- Path + zeus.css
    __TEMA = auto()     # --- Path del tema en curso
    __REC = auto()      # --- Recolector de basura
    __iSMTP = auto()    # --- Base de datos iSMTP.

    # --- Se convertirá en un objeto que lee la configuración del tema
    __CONFTEMA = None

    # --- Montar un PAQUETE de EnteDatos de clase para Singleton
    __PAQUETE = None

    #
    # --- Compatibles con EnteDatos
    #
    #
    # --- Datos de la aplicación
    __D0Z = "0Z_Vers"           # --- Versión de ZEUS cuando se creó

    # --- Datos de usuario
    __DU0 = "U0"                # --- Separador visual
    __DU1 = "U1_Nombre"
    __DU2 = "U2_Mail"
    __DU3 = "U3_BetaTester"

    # --- Datos de la unidad
    __DUN0 = "UN0"              # --- Separador visual
    __DUN2 = "UN2_TemaActivo"
    __DUN3 = "UN3_PathNube"
    __DUN4 = "UN4_NubeActiva"
    __DUN5 = "UN5_VecesCopia"
    __DUN6 = "UN6_VecesUsado"
    __DUN7 = "UN7_Shutdown"

    #
    def __init__(self):

        Registro.__init__(self)

        # --- Singleton sin Singleton
        if self.__class__.__PAQUETE:
            # --- nª instancia de ZEUS, puntero local a clase
            self.PAQUETE = self.__class__.__PAQUETE

        else:
            # --- 1ª instancia, puntero clase iniciado
            self.__class__.__PAQUETE = self.PAQUETE

            # --- Identidad
            aux = __name__ + "." + self.__class__.__name__
            self.EstablecerCTRL(self.ENTE, aux)
            del aux

            # --- Ahora al inicio PROPIO
            ZEUS_init(self)
            self.LeerRegistro()

            # --- Ahora a montar datos del tema
            self.__montar_CONFTEMA()

    #
    # --- Métodos públicos
    #
    #
    # --- Ciclo ZEUS
    def Iniciar(self, deidad: str):
        """ Inicia ZEUS e indica qué deidad lo invoca. """
        self.EstablecerMEM(self.__ZU, deidad)
        ZEUS_inicio(objzeus=self)

    #
    def Acabar(self):
        """ Finaliza a ZEUS. """
        ZEUS_final(objzeus=self)
        self.GuardarRegistro()

    #
    def Guardar(self, mensaje: str):
        """ Guarda los datos de ZEUS y genera un mensaje en el log de INFO. """
        self.GuardarRegistro()
        self.log_INFO(self.DevolverCTRL(self.ENTE), mensaje)

    #
    def RestaurarNube(self):
        """ Propósito: Restaura de la nube. """
        ZEUS_Nube_BD(self, restaurar=True)

        # --- Debemos volver a cargar datos, al inicio efectivo
        self.__montar_CONFTEMA()

    #
    # --- Archivos varios
    #
    #
    #
    def MiFileConf(self, deidad: str):
        """ Le indica a una deidad cual es su archivo de configuración. """
        return add_paths(self.getPathBD, deidad, self.getFileConf)

    #
    def MiPathTema(self, deidad: str):
        """ Le indica a una deidad cual es su path del tema. """
        return add_paths(self.getPathTema, deidad)

    #
    def MiCSS(self, deidad: str):
        """ Le indica a una deidad cual es su archivo CSS. """
        return add_paths(self.getPathTema, deidad, (deidad + ".css"))
        # --- Se necesita 2 veces la deidad, porque el archivo es
        #     ...deidad/deidad.css

    #
    def urlHelp(self, NumAyuda: str):
        """ Url montada para solicitar enlace a la NumAyuda. """
        return ("file:" + self.getPathAyuda + "/search.html?q=" +
                NumAyuda + "&check_keywords=yes&area=default")

    #
    # --- Manejo de logs
    #
    #
    #
    def log_INFO(self, ente: str, mensaje: str) -> None:
        """ Generar un log de información. """
        logs.log_INFO(self.getDeidad, ente, mensaje)

    #
    def log_ERROR(self, ente: str, mensaje: str) -> None:
        """ Generar un log de error. """
        logs.log_ERROR(self.getDeidad, ente, mensaje)

    #
    @property
    def getLog_lista(self) -> list:
        """ Devuelve el archivo de log's en forma de lista para ListStore. """
        return logs.log_to_list(self.getFileLogInfo)

    #
    # --- Manejo del recolector de basura
    #
    #
    #
    def BasuraOn(self):
        """ Activar el recolector de basura. """
        self.EstablecerMEM(self.__REC, True)
        gc.enable()

    #
    def BasuraOff(self):
        """ Desactivar el recolector de basura. """
        self.EstablecerMEM(self.__REC, False)
        gc.disable()

    #
    def RecolectarBasura(self):
        """ Recolectar basura si está activada la opción. """
        if self.esBasuraActivo:
            gc.collect()

    #
    # --- Propiedades Especiales
    #
    #
    # --- Recolector de basura
    @property
    def esBasuraActivo(self):
        """ Conocer estado del recolector de basura (Garbage Collector). """
        return self.DevolverMEM(self.__REC)

    # --- Servidor iSMTP
    @property
    def getBDiSMTP(self):
        """ Nombre de la BD del iSMTP. """
        return self.DevolverMEM(self.__iSMTP)

    #
    # --- Propiedades MEM
    #
    #
    # --- Path inicial del disco
    @property
    def __pathINI(self):
        return self.DevolverMEM(self.__CS1)

    #
    @property
    def getNombreBD(self):
        """ Nombre de la base de datos. """
        return self.DevolverMEM(self.__BD)

    #
    @property
    def getPathBD(self):
        """ Path de la base de datos. """
        return self.DevolverMEM(self.__CS2)

    #
    @property
    def getVersion(self):
        """ Versión ZEUS. """
        return self.DevolverMEM(self.__CS3)

    #
    @property
    def getPathTema(self):
        """ Path del tema en curso. """
        return self.DevolverMEM(self.__TEMA)

    #
    @property
    def getPathAyuda(self):
        """ Path de la ayuda. """
        return self.DevolverMEM(self.__CS9)

    #
    @property
    def getFileConf(self):
        """ Nombre de los ficheros de configuración. """
        return self.DevolverMEM(self.__CS5)

    #
    @property
    def getSepJson(self):
        """ Serparador para json. """
        return ("_" * self.DevolverMEM(self.__CS6))

    #
    @property
    def getSepJsonCorto(self):
        """ Serparador corto para json. """
        return ("_" * int(self.DevolverMEM(self.__CS6) / 2))

    #
    @property
    def getFileLogError(self):
        """ Path + Nombre del fichero de logs de errores. """
        return self.DevolverMEM(self.__CS7)

    #
    @property
    def getFileLogInfo(self):
        """ Path + Nombre del fichero de logs de información. """
        return self.DevolverMEM(self.__CS8)

    #
    @property
    def getDeidad(self):
        """ Nombre de la deidad máxima. """
        return self.DevolverMEM(self.__ZU)

    #
    @property
    def getLugarComun(self):
        """ Para no usar ``olimpo`` como palabra mágica. """
        return self.DevolverMEM(self.__ZZ)

    #
    @property
    def getFileGladeSelCarpeta(self):
        """ Path + archivo del glade para seleccionar carpeta. """
        return add_paths(self.getPathTema, self.getLugarComun,
                         GladesZEUS.SelCarpeta)

    #
    @property
    def getFileGladeSelFile(self):
        """ Path + archivo del glade para seleccionar archivos. """
        return add_paths(self.getPathTema, self.getLugarComun,
                         GladesZEUS.SelFile)

    #
    @property
    def getFileGladeConfirmar(self):
        """ Path + archivo del glade para confirmaciones si/no. """
        return add_paths(self.getPathTema, self.getLugarComun,
                         GladesZEUS.Confirmar)

    #
    @property
    def getFileGladeHelp(self):
        """ Path + archivo del glade para ayuda y web browser. """
        return add_paths(self.getPathTema, self.getLugarComun,
                         GladesZEUS.HelpWeb)

    #
    @property
    def getFileCSS(self):
        """ Path + Nombre del fichero css global. """
        return self.DevolverMEM(self.__CSS)

    #
    # --- Propiedades REG
    #
    #
    # --- Datos del usuario
    #
    @property
    def nombreUsuario(self):
        """ Obtener / Establecer el nombre del usuario. """
        return self.DevolverREG(self.__DU1)

    @nombreUsuario.setter
    def nombreUsuario(self, dato):
        if (self.nombreUsuario != dato):
            self.EstablecerREG(self.__DU1, dato)

            # --- Vamos a guardar y a generar un log
            self.Guardar(MsgZEUS.cambioUsuario)

    #
    @property
    def mailUsuario(self):
        """ Obtener / Establecer el mail del usuario. """
        return self.DevolverREG(self.__DU2)

    @mailUsuario.setter
    def mailUsuario(self, dato):
        if (self.mailUsuario != dato):
            self.EstablecerREG(self.__DU2, dato)

            # --- Vamos a guardar y a generar un log
            self.Guardar(MsgZEUS.cambioMail)

    #
    @property
    def esUsuBetaTester(self):
        """ Obtener / Establecer si es un beta tester. """
        return self.DevolverREG(self.__DU3)

    @esUsuBetaTester.setter
    def esUsuBetaTester(self, dato):
        self.EstablecerREG(self.__DU3, dato)

    #
    # --- Datos de la unidad
    #
    @property
    def pathNube(self):
        """ Obtener / Establecer el path para copiar en la nube. """
        x = self.DevolverREG(self.__DUN3)
        if x:
            return x
        else:
            return ""

    @pathNube.setter
    def pathNube(self, dato):
        if (self.pathNube != dato):
            self.EstablecerREG(self.__DUN3, dato)

            # --- Vamos a guardar y a generar un log
            self.Guardar(MsgZEUS.cambioNube)

    #
    @property
    def esNubeActiva(self):
        """ Obtener / Establecer si la copia en la nube está activada. """
        return self.DevolverREG(self.__DUN4)

    @esNubeActiva.setter
    def esNubeActiva(self, dato):
        if (self.esNubeActiva != dato):
            self.EstablecerREG(self.__DUN4, dato)

            # --- Vamos a guardar y a generar un log
            self.Guardar(MsgZEUS.cambioNube)

    #
    @property
    def vecesGuardar(self):
        """ Obtener / Establecer cada cuantas veces se use, hay que guardar. """
        x = self.DevolverREG(self.__DUN5)
        if x:
            return x
        else:
            return 0

    @vecesGuardar.setter
    def vecesGuardar(self, dato):
        if (self.vecesGuardar != dato):
            self.EstablecerREG(self.__DUN5, dato)

            # --- Vamos a guardar y a generar un log
            self.Guardar(MsgZEUS.cambioNube)

    @property
    def veces(self):
        """ Obtener / Establecer las veces que se ha utilizado. """
        x = self.DevolverREG(self.__DUN6)
        if x:
            return x
        else:
            return 0

    @veces.setter
    def veces(self, dato):
        self.EstablecerREG(self.__DUN6, dato)

    #
    @property
    def esShutdown(self):
        """ Obtener / Establecer si realizará un shutdown al salir. """
        return self.DevolverREG(self.__DUN7)

    @esShutdown.setter
    def esShutdown(self, dato):
        if (self.esShutdown != dato):
            self.EstablecerREG(self.__DUN7, dato)

            # --- Vamos a guardar y a generar un log
            self.Guardar(MsgZEUS.cambioSalir)

    #
    # --- Propiedades del Tema
    #
    #
    @property
    def tema(self):
        """ Obtener / Establecer el tema usado. """
        x = self.DevolverREG(self.__DUN2)
        if x:
            return x
        else:
            return ""

    @tema.setter
    def tema(self, dato):
        self.EstablecerREG(self.__DUN2, dato)
        # --- Si se cambia el tema hay que remontar los path's
        self.__montar_CONFTEMA()

    #
    @property
    def getHorizontal(self):
        """ Tamaño máximo de la ventana en horizontal. """
        return self.__CONFTEMA.horizontal

    #
    @property
    def getVertical(self):
        """ Tamaño máximo de la ventana en vertical. """
        return self.__CONFTEMA.vertical

    #
    # --- Métodos privados
    #
    #
    # --- Leer y montar la configuración del tema (Por si cambia en ejecución)
    def __montar_CONFTEMA(self) -> None:

        # --- Montar el path del tema actual
        path = add_paths(self.DevolverMEM(self.__CS4), self.tema)
        self.EstablecerMEM(self.__TEMA, path)

        # --- Montar CSS común
        path = add_paths(self.getPathTema, self.getLugarComun,
                         (self.DevolverMEM(self.__Z0) + ".css")
                         )
        self.EstablecerMEM(self.__CSS, path)

        # --- Ahora debemos leer el json del tema
        path = add_paths(self.DevolverMEM(self.__CS4), self.tema,
                         self.getFileConf)

        # --- Eliminar puntero a cualquier objeto anterior y reapuntar
        self.__class__.__CONFTEMA = ""
        self.__class__.__CONFTEMA = ConfTEMA(path, self.getSepJson)
        del path
