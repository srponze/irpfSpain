import sys
from typing import Callable, Dict

from .modelo.modelo import Modelo
from .vista.analisis import Analisis
from .vista.constantes.constantes import *
from .vista.constantes.mensajes import *
from .vista.menuPrincipal import MenuPrincipal
from .vista.resultados import Resultados


class Controlador:

    def __init__(self):

        while True:
            self.modelo = Modelo()
            self.menuPrincipal = MenuPrincipal()
            self.analisis = Analisis(self)
            self.resultados = Resultados()

            opcion = self.menuPrincipal.mostrarMenu()
            if opcion == OPCIONES_PRINCIPALES[0]:
                self.comprobarDocumentos()
                datos = self.modelo.realizarCalculos()
                self.mostrarResultados(datos)
            elif opcion == OPCIONES_PRINCIPALES[1]:
                break

    def mostrarResultados(self, datos: Dict):
        while True:
            self.resultados.mostrarComprobacionErrores(
                datos["listaMovimientosSinCompraActivos"],
                datos["listaMovimientosSinCompraDivisas"],
            )

            opcion = self.resultados.mostrarMenu()

            if opcion == OPCIONES_RESULTADOS[0]:
                opcion = self.resultados.movimientos(
                    TITULO_MOVIMIENTOS_ACTIVOS,
                    MENSAJE_CABECERA_ACTIVOS,
                    datos["listaMovimientosActivos"],
                    ACTIVOS,
                    TITULO_POSICIONES_ACTIVOS,
                    datos["listaPosicionesActivos"],
                    datos["listaMovimientosSinCompraActivos"],
                )
                if opcion == OPCIONES_AUXILIARES_RESULTADOS[1]:
                    sys.exit()
            elif opcion == OPCIONES_RESULTADOS[1]:
                opcion = self.resultados.movimientos(
                    TITULO_MOVIMIENTOS_DIVISAS,
                    MENSAJE_CABECERA_DIVISAS,
                    datos["listaMovimientosDivisas"],
                    DIVISAS,
                    TITULO_POSICIONES_DIVISAS,
                    datos["listaPosicionesDivisas"],
                    datos["listaMovimientosSinCompraDivisas"],
                )
                if opcion == OPCIONES_AUXILIARES_RESULTADOS[1]:
                    sys.exit()
            elif opcion == OPCIONES_RESULTADOS[2]:
                opcion = self.resultados.transacciones(
                    TITULO_TRANSACCIONES_ACTIVOS,
                    MENSAJE_CABECERA_ACTIVOS,
                    datos["transaccionesActivos"],
                    ACTIVOS,
                )
                if opcion == OPCIONES_AUXILIARES_RESULTADOS[1]:
                    sys.exit()
            elif opcion == OPCIONES_RESULTADOS[3]:
                opcion = self.resultados.transacciones(
                    TITULO_TRANSACCIONES_DIVISAS,
                    MENSAJE_CABECERA_DIVISAS,
                    datos["transaccionesDivisas"],
                    DIVISAS,
                )
                if opcion == OPCIONES_AUXILIARES_RESULTADOS[1]:
                    sys.exit()
            elif opcion == OPCIONES_RESULTADOS[4]:
                break
            elif opcion == OPCIONES_RESULTADOS[5]:
                sys.exit()

    def comprobarDocumentos(self) -> None:
        while True:
            self.analisis.mostrarTituloAnalisis()
            if not self.pasoDocumento(
                self.modelo.comprobarTransactions,
                MENSAJE_ERRORES_TRANSACTIONS,
                MENSAJE_TRANSACTIONS,
            ):
                continue

            if not self.pasoDocumento(
                self.modelo.comprobarAccount,
                MENSAJE_ERRORES_ACCOUNT,
                MENSAJE_ACCOUNT,
            ):
                continue

            if not self.pasoAño(
                self.modelo.comprobarAñoRenta,
                MENSAJE_ERRORES_AÑO_RENTA,
                MENSAJE_AÑO_RENTA,
            ):
                continue
            else:
                break

    def pasoDocumento(
        self,
        funcionComprobar: Callable,
        mensajeErrores: str,
        mensajeCorrecto: str,
    ) -> bool:
        while True:
            listaErrores = funcionComprobar()
            if listaErrores:
                self.analisis.imprimirErrores(listaErrores, mensajeErrores)
                opcion = self.analisis.mostrarMenuReintento()

                if opcion == OPCIONES_ANALISIS[0]:
                    continue

                elif opcion == OPCIONES_ANALISIS[1]:
                    return False

            else:
                self.analisis.imprimirMensaje(mensajeCorrecto)
                return True

    def pasoAño(
        self,
        funcionComprobar: Callable,
        mensajeErrores: str,
        mensajeCorrecto: str,
    ) -> bool:
        while True:
            entradaTexto = self.analisis.preguntarAño()
            listaErrores = funcionComprobar(entradaTexto)
            if listaErrores:
                self.analisis.imprimirErrores(listaErrores, mensajeErrores)
                opcion = self.analisis.mostrarMenuReintento()

                if opcion == OPCIONES_ANALISIS[0]:
                    continue

                elif opcion == OPCIONES_ANALISIS[1]:
                    return False

            else:
                self.analisis.imprimirMensaje(mensajeCorrecto)
                return True
