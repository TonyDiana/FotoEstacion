#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Menú del Setup de HelioIsis.
    :Autor:     Tony Diana
    :Versión:   A15.1

    ---------------------------------------------------------------------------
"""
# -----------------------------------------------------------------------------
# Mapa de señales, mostrar Stacks, asociadas a señal 'realice'
# sg_gen_usu_realice    sg_par_nube_realice     sg_cam_lent_realice
# sg_gen_cam_realice
#
# SEL_CAM_changed_cb --> Selección cámara en rejilla
# -----------------------------------------------------------------------------


# --- Módulos estandard
from std.gtk import Ventana
from std.disco import add_paths


# --- Deidades
from olimpo import ZEUS
from olimpo import HELIOS
from olimpo import HEISIS


# --- Equipo
from equipo import ClassCAM, ListaCAM, MailGUICam


# --- Módulos propios
from . import const as KMENU
from .ismtp import MailMain, MailSetup


#
class GUI(Ventana):
    """ :Propósito: Clase manejadora del GUI del menú del setup. """

    __slots__ = ["dif", "cam_sel_num", "cam_sel_nom", "ENTE"]

    # --- Palabras mágicas
    __mg = {
        # --- Índice de la ayuda
        # HI_Setup

        # --- GtkWindow principal
        # SETUP

        # --- Botones
        # _bt_cam_edit_, _bt_cam_delete_  Hacerlos visibles, un solo uso

        # --- GENERAL
        "btgen": ("_bt_gen_usu_", "_bt_gen_par_",
                  "_bt_gen_cam_", "_bt_gen_log_"),

        # --- PARAMETROS
        "btpar": ("_bt_par_nube_", "_bt_par_unid_", "_bt_par_deco_"),
        # --- CÁMARAS Y LENTES
        "btcam": ("_bt_cam_cam_", "_bt_cam_lent_"),

        # --- GtkEntry's
        "u_name": "USU_NAME",
        "u_mail": "USU_MAIL",
        "u_msg": "USU_MSG",

        "cl_path": "PATH_NUBE",
        "cl_act": "NUBE_ONOFF",
        "cl_veces": "NUBE_VECES",

        "un_stdw": "UN_STDW",

        "dec_act": "DEC_ONOFF",
        "dec_13": "DEC_13",
        "dec_23": "DEC_23",
        "dec_siempre": "DEC_PRIOR",
        "dec_tv": "DEC_TV",

        # --- GtkStacks's
        # GEN_USU, GEN_PAR, GEN_CAM, GEN_LOG
        "gen_main": "GENERAL",

        "par_main": "PARAM",
        "par_nube": "PAR_NUBE",
        "par_deco": "PAR_DECO",
        "par_unid": "PAR_UNID",

        "cam_main": "CAM",
        "cam_cam": "CAM_CAM",
        "cam_lent": "CAM_LENT",

        # --- Gestores de listas
        # LST_LENT, LST_LOG

        # --- Mensajes que sólo se usan una vez
        # --- Restaurar de la nube: "Si restaura la copia ...
        # --- Crear una cámara: "Crear una cámara"
        # --- Editar una cámara: "Cámara ... editada"
        # --- Borrar una cámara: "No podrá recuperar los datos ...
        # --- Borrar una cámara, log: "Cámara ... borrada"


        # --- Archivos glade asociados y ventana principal
        # setup.glade, SETUP
    }

    #
    def __init__(self):

        # --- Identidad
        self.ENTE: str = __name__ + "." + self.__class__.__name__

        # --- Marcadores globales de cargas diferidas de glade
        #   Ayuda, selector, confirmación
        self.dif = [True, True, True]

        # --- Cámara seleccionada
        self.cam_sel_num: int = None
        self.cam_sel_nom: str = None

        # --- Crear ventana, 1º lista de glades
        path1 = add_paths(HEISIS.getPathTema, KMENU.SOMOS, "setup.glade")
        path2 = (ZEUS.getFileCSS, HEISIS.getFileCSS)

        # --- Añadir el archivo de glade de la lista de cámaras
        path1 = (path1, ListaCAM.fileGlade)

        Ventana.__init__(self, fileGlade=path1, fileCss=path2)

        # --- Conectar la lista de cámaras en su objeto GTK padre
        path1 = self.GUI(ListaCAM.nombreEnGlade)
        path2 = self.GUI(ListaCAM.nombreEnGlade + "2")
        path2.add(path1)
        del path1, path2

        # --- Tomar la ventana principal, conectar señales y mostrar
        self.ConectarSignals(self)
        self.win = self.GUI("SETUP")
        self.win.show()

        # --- Busquemos un i-mail con instrucciones
        mail = MailSetup()
        if mail.RecibirMailYBorrar():
            # --- ¿Será a las cámaras?
            if (mail.adonde == self.__mg["cam_cam"]):
                self.bt_gen_cam()
                self.bt_cam_cam()
        del mail

        # --- Saltará a sg_gen_usu_realice por eventos GTK, allí está el inicio

    #
    # --- Respuestas
    #
    #
    @property
    def getRespuesta(self):
        """ Respuesta al menú, siempre ``False``. """
        return False

    #
    # --- Botones y señales (bt_exit es de la clase heredada)
    #
    #
    # --- Solicitar ayuda
    def bt_help(self, *args, **kwargs):
        if self.dif[0]:   # --- Si nunca se hizo antes
            self.AgregarGlade(ZEUS.getFileGladeHelp)
            self.ConectarSignals(self)
            self.dif[0] = False

        self.MostrarUrl(ZEUS.urlHelp("HI_Setup"))

    # --- Activar todos los botones generales
    def bts_gen_on(self):
        self.ActivoSI(self.__mg["btgen"])

    # --- Activar todos los botones de parámetros
    def bts_par_on(self):
        self.ActivoSI(self.__mg["btpar"])

    # --- Activar todos los botones de cámaras y lentes
    def bts_cam_on(self):
        self.ActivoSI(self.__mg["btcam"])

    #
    # --- Stack Usuario
    #
    #
    # --- Mostrar datos del usuario (Siempre se muestra lo 1º)
    def sg_gen_usu_realice(self, *args, **kwargs):
        self.bts_gen_on()
        self.ActivoNO(self.__mg["btgen"][0])

        self.SetTexto(self.__mg["u_name"], ZEUS.nombreUsuario)
        self.SetTexto(self.__mg["u_mail"], ZEUS.mailUsuario)
        self.SetBufferTexto(self.__mg["u_msg"], HEISIS.msg)

    # --- Botón datos del usuario
    def bt_gen_usu(self, *args, **kwargs):
        self.MostrarStack(self.__mg["gen_main"], "GEN_USU")
        self.bts_gen_on()
        self.ActivoNO(self.__mg["btgen"][0])

    # --- Confirmaron datos del usuario
    def bt_usu_ok(self, *args, **kwargs):
        ZEUS.nombreUsuario = self.GetTexto(self.__mg["u_name"])
        ZEUS.mailUsuario = self.GetTexto(self.__mg["u_mail"])
        HEISIS.msg = self.GetBufferTexto(self.__mg["u_msg"])
        self.bt_exit()

    #
    # --- Stack de parámetros generales / Nube
    #
    #
    # --- Botón datos nube en general
    def bt_gen_par(self, *args, **kwargs):
        self.MostrarStack(self.__mg["gen_main"], "GEN_PAR")
        self.bts_gen_on()
        self.ActivoNO(self.__mg["btgen"][1])

    # --- Botón datos nube en parámetros
    def bt_par_nube(self, *args, **kwargs):
        self.MostrarStack(self.__mg["par_main"], self.__mg["par_nube"])
        self.bts_par_on()
        self.ActivoNO(self.__mg["btpar"][0])

    # --- Mostrar datos de la nube (Siempre se muestra lo primero)
    def sg_par_nube_realice(self, *args, **kwargs):
        self.bts_par_on()
        self.ActivoNO(self.__mg["btpar"][0])
        self.SetValor(self.__mg["cl_veces"], ZEUS.vecesGuardar)
        self.SetTexto(self.__mg["cl_path"], ZEUS.pathNube)
        self.SetSwitch(self.__mg["cl_act"], ZEUS.esNubeActiva)

    # --- Confirmaron datos de la nube
    def bt_nube_ok(self, *args, **kwargs):
        ZEUS.esNubeActiva = self.GetSwitch(self.__mg["cl_act"])
        ZEUS.pathNube = self.GetTexto(self.__mg["cl_path"])
        ZEUS.vecesGuardar = self.GetValor(self.__mg["cl_veces"])
        self.bt_exit()

    # --- Solicitar confirmación para restaurar las copias
    def bt_restaurar(self, *args, **kwargs):

        # --- Si nunca se hizo antes, hay que cargar y conectar señales
        if self.dif[2]:
            self.AgregarGlade(ZEUS.getFileGladeConfirmar)
            self.ConectarSignals(self)
            self.dif[2] = False

        resp = "Si restaura la copia no hay manera de devolver"
        resp += " la copia anterior, confirme que eso es lo que"
        resp += " desea realmente."
        resp = self.Confirmar(mensaje=resp)

        # --- Restaurar de la nube y regresar al menú
        if resp:
            ZEUS.RestaurarNube()
            self.bt_exit()

    # --- Seleccionar una carpeta para la nube
    def bt_nube_carpeta(self, *args, **kwargs):

        # --- Si nunca se hizo antes, hay que cargar y conectar señales
        if self.dif[1]:
            self.AgregarGlade(ZEUS.getFileGladeSelCarpeta)
            self.ConectarSignals(self)
            self.dif[1] = False

        resp = self.SeleccionarCarpeta()

        # --- Si seleccionó una carpeta, sólo la mostramos, aun no guardamos
        if resp:
            self.SetTexto(self.__mg["cl_path"], resp)

        del resp

    #
    # --- Stack de parámetros de la unidad
    #
    #
    # --- Botón de la unidad
    def bt_par_unid(self, *args, **kwargs):
        self.MostrarStack(self.__mg["par_main"], self.__mg["par_unid"])
        self.bts_par_on()
        self.ActivoNO(self.__mg["btpar"][1])

        # --- Monstar los datos de la unidad
        self.SetSwitch(self.__mg["un_stdw"], ZEUS.esShutdown)

    # --- Confirmaron datos de la unidad
    def bt_uni_ok(self, *args, **kwargs):
        ZEUS.esShutdown = self.GetSwitch(self.__mg["un_stdw"])
        self.bt_exit()

    #
    # --- Stack de parámetros generales / Decoradores
    #
    #
    # --- Botón datos de los decoradores
    def bt_par_deco(self, *args, **kwargs):
        self.MostrarStack(self.__mg["par_main"], self.__mg["par_deco"])
        self.bts_par_on()
        self.ActivoNO(self.__mg["btpar"][2])

        # --- Mostrar datos de los decoradores
        self.SetSwitch(self.__mg["dec_act"], HELIOS.esDecoradorActivo)
        self.SetSwitch(self.__mg["dec_siempre"], HELIOS.esDecoradorPrioritario)
        self.SetSwitch(self.__mg["dec_tv"], HELIOS.esDecoradoTV)
        self.SetTexto(self.__mg["dec_13"], HELIOS.decUnTercio)
        self.SetTexto(self.__mg["dec_23"], HELIOS.decDosTercios)

    # --- Confirmaron datos de los decoradores
    def bt_deco_ok(self, *args, **kwargs):
        HELIOS.esDecoradorActivo = self.GetSwitch(self.__mg["dec_act"])
        HELIOS.esDecoradorPrioritario = self.GetSwitch(self.__mg["dec_siempre"])
        HELIOS.esDecoradoTV = self.GetSwitch(self.__mg["dec_tv"])
        HELIOS.decUnTercio = self.GetTexto(self.__mg["dec_13"])
        HELIOS.decDosTercios = self.GetTexto(self.__mg["dec_23"])
        self.bt_exit()

    #
    # --- Stack Cámaras
    #
    #
    # --- Mostrar datos de las cámaras (Siempre se muestra lo 1º)
    def sg_gen_cam_realice(self, *args, **kwargs):

        # --- Lista de cámaras al ListStore
        self.AgregarListStore(ListaCAM.GtkListStore, ListaCAM.listaDatos)

        self.bts_cam_on()
        self.ActivoNO(self.__mg["btcam"][0])

    # --- Botón datos de las cámaras en menú general
    def bt_gen_cam(self, *args, **kwargs):
        self.MostrarStack(self.__mg["gen_main"], "GEN_CAM")
        self.bts_gen_on()
        self.ActivoNO(self.__mg["btgen"][2])

    # --- Botón datos de las cámaras en menú cámaras y lentes
    def bt_cam_cam(self, *args, **kwargs):
        self.MostrarStack(self.__mg["cam_main"], self.__mg["cam_cam"])
        self.bts_cam_on()
        self.ActivoNO(self.__mg["btcam"][0])

    # --- Botón crear una cámara
    def bt_cam_alta(self, *args, **kwargs):

        # --- 1º Auto i-Mail para saber que regesamos aquí
        mail = MailSetup(adonde=self.__mg["cam_cam"], auto=True, send=True)
        # --- Reaprovecho palabra mágica cam_cam

        # --- 2º i-Mail a Cámaras
        mail = MailGUICam(send=True)

        # --- 3º i-Mail's al main del menú y salir
        mail = MailMain(adonde=KMENU.Option.SETUP, send=True)
        mail = MailMain(adonde=KMENU.Option.CAM, send=True)
        del mail

        # --- Registro de log
        ZEUS.log_INFO(self.ENTE, "Crear una cámara")
        self.bt_exit()

    # --- Selección de una cámara
    def SEL_CAM_changed_cb(self, elemento, *args, **kwargs):
        self.cam_sel_num = self.LeerListStore(elemento, columna=0)
        self.cam_sel_nom = self.LeerListStore(elemento, columna=1)
        self.Mostrar(("_bt_cam_edit_", "_bt_cam_delete_"))

    # --- Edición de una cámara
    def bt_cam_edit(self, *args, **kwargs):

        # --- Registro de log
        ZEUS.log_INFO(self.ENTE, "Cámara " + self.cam_sel_nom + " editada")

        # --- 1º Auto i-Mail para saber que regesamos aquí
        mail = MailSetup(adonde=self.__mg["cam_cam"], auto=True, send=True)
        # --- Reaprovecho palabra mágica cam_cam

        # --- 2º i-Mail a Cámaras
        mail = MailGUICam(ID=self.cam_sel_num, send=True)

        # --- 3º i-Mail's al main del menú y salir
        mail = MailMain(adonde=KMENU.Option.SETUP, send=True)
        mail = MailMain(adonde=KMENU.Option.CAM, send=True)
        del mail
        self.bt_exit()

    # --- Borrado de una cámara
    def bt_cam_delete(self, *args, **kwargs):

        # --- Si nunca se hizo antes, hay que cargar y conectar señales
        if self.dif[2]:
            self.AgregarGlade(ZEUS.getFileGladeConfirmar)
            self.ConectarSignals(self)
            self.dif[2] = False

        resp = "No podrá recuperar los datos de la cámara si los borra,"
        resp += " confirme que desea eliminarlos de forma definitiva."
        resp = self.Confirmar(mensaje=resp)

        # --- Borrar
        if resp:
            cam = ClassCAM(BD=ZEUS.BD, ID=self.cam_sel_num)
            cam.BorrarRegistro()

            # --- Registro de log
            ZEUS.log_INFO(self.ENTE, "Cámara " + self.cam_sel_nom + " borrada")

            # --- Volver a cargar la lista de cámaras
            self.sg_gen_cam_realice()

    #
    # --- Stack Lentes
    #
    #
    # --- Mostrar datos de las lentes
    def sg_cam_lent_realice(self, *args, **kwargs):

        # --- Primero borramos lo que tenga la lista
        aux = self.GUI("LST_LENT")
        aux.clear()
        del aux

    # --- Botón datos de las lentes en menú cámaras y lentes
    def bt_cam_lent(self, *args, **kwargs):
        self.MostrarStack(self.__mg["cam_main"], self.__mg["cam_lent"])
        self.bts_cam_on()
        self.ActivoNO(self.__mg["btcam"][1])

    # --- Botón crear una lente
    def bt_lent_alta(self, *args, **kwargs):
        pass

    #
    # --- Stack Logs
    #
    #
    #
    def bt_gen_log(self, *args, **kwargs):
        self.bts_gen_on()
        self.ActivoNO(self.__mg["btgen"][3])
        self.MostrarStack(self.__mg["gen_main"], "GEN_LOG")

        # --- Log al ListStore
        self.AgregarListStore("LST_LOG", ZEUS.getLog_lista)
