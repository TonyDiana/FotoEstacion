#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito: Manejador genérico de GTK
    :Autor:     Tony Diana
    :Versión:   21.01.24

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
# --- Este orden produce aviso de flake8 (E402), pero es el orden correcto

# --- Manejador web GTK
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2
# --- Este orden produce aviso de flake8 (E402), pero es el orden correcto


#
class Ventana(object):
    """
        :Propósito:
            Clase manejadora de GKT genérico. Pensado para heredar. Ofrece la
            propiedad ``GUI`` para manejar todos los objetos Gtk. También
            ofrece la propiedad ``builder``, la cual es el constructor del
            objeto GTK, por si se desea personalizar el comportamiento. Además,
            ofrece la propiedad ``win`` para usarla en el objeto que la hereda
            y aprovechar el método ``bt_exit`` de forma estandarizada.

        :param fileGlade:
            Nombre del archivo .glade con path completo. Puede recibir un
            string, o un objeto iterable y añadirá al manejador GTK todos los
            archivos glade que reciba. También puede no recibir un archivo
            glade, para montar el GUI manualmente.

        :param fileCss:
            Nombre del archivo .css con path completo. Puede recibir un
            string, o un objeto iterable y añadirá al manejador GTK todos los
            archivos glade que reciba. También puede no recibir un archivo
            glade, para montar el GUI manualmente.
    """

    __slots__ = ["GUI", "builder", "browser", "url", "win"]

    # --- Palabras mágicas
    __mg = {
        # --- Ventana de confirmación
        # CONFIR_MACION, CONFIR_MACION_TEXT,

        # --- Selección de carpeta o archivo
        # SELECT_FOLDER, SELECT_FILE,

        # --- Ayuda / web browser
        # help_web y ....
        "win_help_web": "WIN_HELP_WEB",
    }

    #
    # --- Generación de la ventana
    #
    #
    #
    def __init__(self, fileGlade: str, fileCss: str = False):

        # --- Crear un manejador
        self.builder = Gtk.Builder()
        self.win = None

        # --- Futuro manejador de web browser.
        self.browser = False
        self.url = None

        # --- Montar los archivos glade
        if fileGlade:
            if (type(fileGlade) == str):
                self.AgregarGlade(fileGlade)

            else:
                for x in fileGlade:
                    self.AgregarGlade(x)

        # --- Montar los archivos css
        if fileCss:
            if (type(fileCss) == str):
                self.AgregarCss(fileCss)

            else:
                for x in fileCss:
                    self.AgregarCss(x)

        # --- Tomar objetos
        self.GUI = self.builder.get_object

    #
    def AgregarGlade(self, file) -> None:
        """ Agrega un archivo Glade a la GUI """
        self.builder.add_from_file(file)

    #
    def AgregarCss(self, file) -> None:
        """ Agrega un CSS a la GUI """
        css = Gtk.CssProvider()
        css.load_from_path(file)

        Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    #
    def ConectarSignals(self, objGUI) -> None:
        """
        Conectar señales y botones. Requiere recibir el objeto que lo
        hereda como parámetro. Debería ser invocado de la siguiente
        manera: ``self.ConectarSignals(self)``.
        """
        self.builder.connect_signals(objGUI)

    #
    def Main(self) -> None:
        """ Lanzar el bucle de eventos GTK """
        Gtk.main()

    #
    def Quit(self, *args, **kwargs) -> None:
        """ Cerrar el bucle GTK """
        Gtk.main_quit()

    #
    # --- Visualización de elementos
    #
    #
    # --- Verdadero activador o desactivador de la sensibilidad
    def __sensitivo(self, elem, tipo=False) -> None:
        # --- Si se recibe un str, se convierte en tupla para iterarlo
        if (type(elem) is str):
            tmp = (elem, )

        else:
            tmp = elem

        for x in tmp:
            aux = self.GUI(x)
            aux.set_sensitive(tipo)

        del aux, tmp

    #
    def ActivoNO(self, elem) -> None:
        """
        Desactivar la sensibilidad de un elemento o varios elementos pasados
        en forma de tupla.

        :param elem: Nombre de los elementos a desactivar.
        :type elem: string, tuple
        """
        self.__sensitivo(elem, False)

    #
    def ActivoSI(self, elem) -> None:
        """
        Activar la sensibilidad de un elemento o varios elementos pasados en
        forma de tupla.

        :param elem: Nombre de los elementos a desactivar.
        :type elem: string, tuple
        """
        self.__sensitivo(elem, True)

    #
    def Mostrar(self, elemento) -> None:
        """ Mostrar un elemento o tupla de elementos. """
        self.Visibilidad(elemento, True)

    #
    def Ocultar(self, elemento) -> None:
        """ Ocultar un elemento o tupla de elementos. """
        self.Visibilidad(elemento, False)

    #
    def Visibilidad(self, elem, ver: bool = True) -> None:
        """
        Cambia la visibilidad de un elemento o tupla de elementos.
        El parámetro ``ver`` permite usar un sólo método para todo
        escenario.
        """
        # --- Si se recibe un str, se convierte en tupla para iterarlo
        if (type(elem) is str):
            tmp = (elem, )

        else:
            tmp = elem

        for x in tmp:
            if ver:
                self.GUI(x).show()
            else:
                self.GUI(x).hide()

        del x, tmp

    #
    def MostrarStack(self, stack, pagina) -> None:
        """ Mostrar una página concreta de un Stack o hijo. """
        tmp = self.GUI(stack)
        tmp.set_visible_child_name(pagina)
        del tmp

    #
    def AgregarListStore(self, elemento: str, lista: tuple) -> None:
        """
        Agrega elementos/tupla a una ListStore.

        .. nota::
            Comienza siempre por vaciar la ListStore, eso permite no tener
            que controlar si se ha llenado previamente, si es que así se
            desea, o permite usar glade con elementos de prueba y perderlos
            en ejecución.
        """
        lSt = self.GUI(elemento)
        lSt.clear()
        for x in lista:
            lSt.append(x)
        del lSt, x

    #
    def LeerListStore(self, elemento, columna: int = 0) -> None:
        """
        Unifica la lectura del elemento ListStore seleccionado por el
        usuario.
        """
        (model, inter) = elemento.get_selected()

        # --- Da problemas eliminar un registro que aparece en la rejilla
        try:
            return model[inter][columna]

        except Exception:
            return False

    #
    def ActivarCombo(self, elemento: str, lista: tuple, cual) -> None:
        """ Activa un elemento en el ComboBox. """

        # --- No encuentro una manera más Pitónica de hacerlo
        cb = self.GUI(elemento)
        i = 0
        for x in lista:
            if x[0] == cual:
                cb.set_active(i)
                break
            else:
                i += 1

        del cb, x, i

    #
    def MontarCombo(self, elementos: str, lista: tuple, cual) -> None:
        """
        Monta un ComboBox de la siguiente manera:

            - elementos es una tupla en la cual el 1º elemento es el nombre
              del widget del ComboBox. El segundo es el nombre de la ListStore.
            - lista es una tupla con los elementos a agregar en la ListStore;
              cada elemento tendrá el número índice y el nombre a mostrar
            - cual es el nombre del elemento a activar.
            - Utiliza los métodos ``AgregarListStore`` y ``ActivarCombo`` de la
              propia clase.
        """
        self.AgregarListStore(elementos[1], lista)
        self.ActivarCombo(elementos[0], lista, cual)

    #
    # --- Editables
    #
    #
    #
    def SetSwitch(self, cual, estado):
        """ Mostrar ON/OFF, el valor de un Switch. """
        self.GUI(cual).set_active(estado)

    #
    def GetSwitch(self, cual):
        """ Tomar el valor ON/OFF de un Switch. """
        return self.GUI(cual).get_active()

    #
    def SetTexto(self, donde, texto):
        """ Mostrar un texto en un elemento del GUI. """
        self.GUI(donde).set_text(texto)

    #
    def GetTexto(self, cual):
        """ Tomar un texto en un elemento del GUI. """
        return self.GUI(cual).get_text()

    #
    def SetValor(self, donde, valor):
        """ Mostrar un valor en un elemento del GUI. """
        self.GUI(donde).set_value(valor)

    #
    def GetValor(self, cual):
        """ Tomar un valor en un elemento del GUI. """
        return self.GUI(cual).get_value()

    #
    def SetBufferTexto(self, donde, texto):
        """ Mostrar un texto con buffer en un elemento del GUI. """
        buff = self.GUI(donde).get_buffer()
        buff.set_text(texto)
        del buff

    #
    def GetBufferTexto(self, cual):
        """ Tomar texto de un buffer en un elemento del GUI. """
        buffer = self.GUI(cual).get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        return buffer.get_text(start_iter, end_iter, True)

    #
    def GetCombo(self, cual):
        """ Obtener el índice del ComboBox activo. """
        lista = self.GUI(cual).get_model()
        activo = self.GUI(cual).get_active()
        return lista[activo][0]

    #
    # --- Botones estandarizados
    #
    #
    #
    def bt_exit(self, *args, **kwargs):
        """ Botón salir """
        self.win.destroy()
        self.Quit(self, *args, **kwargs)

    #
    # --- Diálogos estandarizados
    #
    #
    #
    def Confirmar(self, mensaje: str, *args, **kwargs) -> bool:
        """
        Usar una ventana de diálogo donde se pregunte **Si** o **No**.

        :param mensaje: String que se mostrará.

        :returns:
            Devuelve un ``False`` si el usuario cancela; en caso contrario
            envía la cadena con el archivo o carpeta, según el caso.
        """

        # --- Mostar el mensaje
        aux = self.GUI("CONFIR_MACION_TEXT")
        aux.set_text(mensaje)
        del aux

        # --- Solicitar confirmación y analizar la respuesta
        win = self.GUI("CONFIR_MACION")
        resp = win.run()
        win.hide()

        if resp == Gtk.ResponseType.OK:
            resp = True

        else:
            resp = False

        del win
        return resp

    #
    def SeleccionarCarpeta(self, GtkObjeto="SELECT_FOLDER", *args, **kwargs):
        """
            Seleccionar una carpeta.

            :param GtkObjeto:
                Nombre del objeto GTK que hay que manejar. Por defecto usa el
                valor para seleccionar una carpeta, pero reutiliza el código
                para un selector de archivos, no hay que hacer nada para que
                funcione, símplemente no pasar ningún dato.

            :param confirmar:
                Booleano que indica si se trata de una simple confirmación.
                Sirve para reaprovechar el código y que ``self.Confirmar()``
                no tenga que repetir código

            :returns:
                Devuelve un ``False`` si el usuario cancela; en caso contrario
                envía la cadena con el archivo o carpeta, según el caso.
        """

        win = self.GUI(GtkObjeto)
        resp = win.run()
        win.hide()

        # --- Analizar la respuesta
        if resp == Gtk.ResponseType.OK:
            # --- Ver si se trata de una confirmación o de un selector
            resp = win.get_filename()

        else:
            resp = False

        del win
        return resp

    #
    def SeleccionarFile(self, *args, **kwargs) -> str:
        """
            Seleccionar un archivo.

            :returns:
                Devuelve un ``False`` si el usuario cancela; en caso contrario
                envía la cadena con el archivo o carpeta, según el caso.
        """
        return self.SeleccionarCarpeta(GtkObjeto="SELECT_FILE",
                                       *args, **kwargs)

    #
    # --- Ayuda / web browser
    #
    #
    #
    def MostrarUrl(self, url: str) -> None:
        """
            Gestionador de una ventana de ayuda basada en un navegador
            web (aunque también puede servir de web browser).

            :param url: Dirección de la web o la ayuda.
        """

        # --- Crear el browser
        self.url = url

        # --- Evitar crear el browser 2 veces
        if not(self.browser):
            self.browser = WebKit2.WebView()
            tmp = self.GUI("HELP_WEB")
            tmp.add_with_viewport(self.browser)

            self.browser.show()

        # --- Mostrar la ventana
        tmp = self.GUI(self.__mg["win_help_web"])
        tmp.show()
        del tmp
        self.bt_HELP_WEB_home()

    #
    def bt_HELP_WEB_home(self, *args, **kwargs) -> None:
        """ Regresar al inicio de la ayuda/web """
        self.browser.load_uri(self.url)

    #
    def bt_HELP_WEB_exit(self, *args, **kwargs) -> None:
        """ Salir de la ayuda/web """
        tmp = self.GUI(self.__mg["win_help_web"])
        tmp.hide()
        del tmp
