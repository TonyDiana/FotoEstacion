"""
    :Propósito: Metaclase singleton con control multi hilo a traves del GIL.
    :Autor:     Tony Diana
    :Versión:   20.12.30

    ---------------------------------------------------------------------------
"""

# --- Librería estándard Python
from threading import Lock

# --- Controlador de bloqueos
GIL: Lock = Lock()


class Singleton(type):

    __instancias = {}

    @classmethod
    def __call__(cls, *args, **kwargs):

        # --- Sólo si GIL le da paso
        with GIL:

            # --- Si nunca estuvo es el 1º y le damos el control total
            if cls not in cls.__instancias:
                temp = super(Singleton, cls).__call__(*args, **kwargs)
                cls.__instancias[cls] = temp
                del temp

        return cls.__instancias[cls]
