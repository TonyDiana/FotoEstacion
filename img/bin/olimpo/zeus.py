#!/usr/bin/python3
# -*- coding: utf-8 *-*
"""
    :Propósito:
        Invocación a ZEUS desde cualquier deidad. Aportar el objeto ``ZEUS`` y
        ayuda a evitar referencias circulares de código. Para invocarlo se
        utilizará siempre la declaración:

        ``from olimpo import ZEUS``

        De esta manera queda unificado su uso en toda la solución.

    :Autor:     Tony Diana
    :Versión:   A7.2

    ---------------------------------------------------------------------------
"""


# --- Contantes y configuración
from zeus import const as K
from zeus.kernel import ClassZEUS


# --- Objeto ZEUS
ZEUS = ClassZEUS()


# --- Y como es ZEUS, le quita las variables globales a todo el mundo
del K.SOY, K.KOMUN, K.FILE_CONFIG, K.iSMTP
del K.VERSION, K.PATH_INI, K.PATH_BD, K.NOMBRE_BD, K.PATH_AYUDA
del K.PATH_DE_TEMAS, K.FL_CONF, K.JS_SEP, K.LOG_ERROR, K.LOG_INFO, K.TEMA

del K.ConfigSYS
