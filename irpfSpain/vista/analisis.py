from typing import List

from inquirer import shortcuts

from .constantes.mensajes import *


class Analisis:

    def __init__(self, controlador):
        self.controlador = controlador

    def mostrarTituloAnalisis(self) -> None:
        print(TITULO_ANALISIS)
        print(MENSAJE_COMPROBACIONES)

    def mostrarMenuReintento(self) -> str:
        return shortcuts.list_input(message=MENSAJE_OPCIONES, choices=OPCIONES_ANALISIS)

    def preguntarAño(self) -> str:
        return shortcuts.text(PREGUNTA_AÑO_RENTA)

    def imprimirErrores(self, listaErrores: List[str], mensajeErrores: str) -> None:
        print(mensajeErrores)
        for error in listaErrores:
            print(f" - {error}")
        print()

    def imprimirMensaje(self, mensaje: str) -> None:
        print(mensaje)
