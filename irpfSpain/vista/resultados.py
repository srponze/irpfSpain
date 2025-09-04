import sys
from typing import DefaultDict, Deque, Dict, List, Tuple

from inquirer import shortcuts

from irpfSpain.modelo.entidades.movimiento import Movimiento
from irpfSpain.modelo.entidades.transaccion import Transaccion
from irpfSpain.vista.constantes.constantes import *
from irpfSpain.vista.constantes.mensajes import *
from irpfSpain.vista.impresora import Impresora


class Resultados:

    def __init__(self):
        self.impresora = Impresora()

    def mostrarMenu(self, datos: Dict):
        while True:
            print(TITULO_RESULTADOS)
            if datos["listaMovimientosSinCompraActivos"]:
                print(MENSAJE_ERRORES_MOVIMIENTOS_ACTIVOS)
            if datos["listaMovimientosSinCompraDivisas"]:
                print(MENSAJE_ERRORES_MOVIMIENTOS_DIVISAS)
            print(SEPARACION)

            opcion = shortcuts.list_input(
                message=MENSAJE_OPCIONES_RESULTADOS,
                choices=OPCIONES_RESULTADOS,
            )

            if opcion == OPCIONES_RESULTADOS[0]:
                self.movimientos(
                    TITULO_MOVIMIENTOS_ACTIVOS,
                    MENSAJE_CABECERA_ACTIVOS,
                    datos["listaMovimientosActivos"],
                    ACTIVOS,
                    TITULO_POSICIONES_ACTIVOS,
                    datos["listaPosicionesActivos"],
                    datos["listaMovimientosSinCompraActivos"],
                )

            elif opcion == OPCIONES_RESULTADOS[1]:
                self.movimientos(
                    TITULO_MOVIMIENTOS_DIVISAS,
                    MENSAJE_CABECERA_DIVISAS,
                    datos["listaMovimientosDivisas"],
                    DIVISAS,
                    TITULO_POSICIONES_DIVISAS,
                    datos["listaPosicionesDivisas"],
                    datos["listaMovimientosSinCompraDivisas"],
                )

            elif opcion == OPCIONES_RESULTADOS[2]:
                self.transacciones(
                    TITULO_TRANSACCIONES_ACTIVOS,
                    MENSAJE_CABECERA_ACTIVOS,
                    datos["transaccionesActivos"],
                    ACTIVOS,
                )
            elif opcion == OPCIONES_RESULTADOS[3]:
                self.transacciones(
                    TITULO_TRANSACCIONES_DIVISAS,
                    MENSAJE_CABECERA_DIVISAS,
                    datos["transaccionesDivisas"],
                    DIVISAS,
                )
            elif opcion == OPCIONES_RESULTADOS[4]:
                return False
            elif opcion == OPCIONES_RESULTADOS[5]:
                sys.exit()

    def movimientos(
        self,
        tituloMovimientos: str,
        mensajeCabecera: str,
        listaMovimientos: List[Movimiento],
        codigoImpresion: int,
        tituloPosiciones: str,
        listaPosiciones: DefaultDict[Tuple, Deque[Movimiento]],
        listaMovimientosSinCompra: List[Movimiento],
    ) -> None:

        print(tituloMovimientos)
        print(mensajeCabecera)
        self.impresora.imprimirMovimientos(listaMovimientos, codigoImpresion)

        if listaPosiciones:
            print(tituloPosiciones)
            print(mensajeCabecera)
            self.impresora.imprimirPosiciones(listaPosiciones, codigoImpresion)

        if listaMovimientosSinCompra:
            print(TITULO_VENTAS_SIN_COMPRA_PREVIA)
            print(mensajeCabecera)
            self.impresora.imprimirMovimientos(
                listaMovimientosSinCompra, codigoImpresion
            )
        print()
        opcion = shortcuts.list_input(
            message=MENSAJE_OPCIONES,
            choices=OPCIONES_AUXILIARES_RESULTADOS,
        )

        if opcion == OPCIONES_AUXILIARES_RESULTADOS[1]:
            sys.exit()

    def transacciones(
        self,
        tituloTransacciones: str,
        mensajeCabecera: str,
        transacciones: DefaultDict[Tuple, List[Transaccion]],
        codigoImpresion: int,
    ) -> None:
        print(tituloTransacciones)
        print(mensajeCabecera)
        self.impresora.imprimirTransacciones(transacciones, codigoImpresion)
        print()
        opcion = shortcuts.list_input(
            message=MENSAJE_OPCIONES,
            choices=OPCIONES_AUXILIARES_RESULTADOS,
        )

        if opcion == OPCIONES_AUXILIARES_RESULTADOS[1]:
            sys.exit()
