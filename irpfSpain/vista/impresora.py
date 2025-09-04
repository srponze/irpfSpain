from typing import DefaultDict, Deque, List, Tuple

from irpfSpain.modelo.entidades.movimiento import Movimiento
from irpfSpain.modelo.entidades.transaccion import Transaccion
from irpfSpain.vista.constantes.constantes import *
from irpfSpain.vista.constantes.mensajes import *


class Impresora:

    def imprimirMovimientos(
        self, listamovimientos: List[Movimiento], modo: int
    ) -> None:
        if modo == ACTIVOS:
            for movimiento in listamovimientos:
                self.activo(movimiento)
        elif modo == DIVISAS:
            for movimiento in listamovimientos:
                self.divisa(movimiento)

    def imprimirPosiciones(
        self, listaPosiciones: DefaultDict[Tuple, Deque[Movimiento]], modo: int
    ) -> None:
        if modo == ACTIVOS:
            for key in listaPosiciones:
                for posicion in listaPosiciones[key]:
                    self.activo(posicion)
        elif modo == DIVISAS:
            for key in listaPosiciones:
                for posicion in listaPosiciones[key]:
                    self.divisa(posicion)

    def imprimirTransacciones(
        self, listaTransacciones: DefaultDict[Tuple, List[Transaccion]], modo: int
    ) -> None:
        if modo == ACTIVOS:
            for key in listaTransacciones:
                for transaccion in listaTransacciones[key]:
                    self.activo(transaccion.adquisicion)
                    self.activo(transaccion.transmision)
        elif modo == DIVISAS:
            for key in listaTransacciones:
                for transaccion in listaTransacciones[key]:
                    self.divisa(transaccion.adquisicion)
                    self.divisa(transaccion.transmision)

    def activo(self, movimiento: Movimiento) -> None:
        print(
            f"{movimiento.fecha}  {movimiento.hora}  {movimiento.activo[0:21]:22}"
            f" {movimiento.isin}  {movimiento.numero:5}"
            f" {round(movimiento.precio, 2):7,.2f} {movimiento.divisa}"
            f" {round(movimiento.valorLocal, 2):11,.2f} {movimiento.divisa}"
            f" {round(movimiento.valor, 2):11,.2f} EUR"
            f"  {round(movimiento.tipoDeCambio, 4):.4f}"
            f"  {round(movimiento.comision, 2):.2f} EUR"
            f" {round(movimiento.total, 2):11,.2f} EUR"
        )

    def divisa(self, movimiento: Movimiento) -> None:
        print(
            f"{movimiento.fecha}  {movimiento.hora}  {movimiento.activo[0:21]:22}"
            f" {round(movimiento.valorLocal, 2):11,.2f} {movimiento.divisa}"
            f" {round(movimiento.valor, 2):11,.2f} EUR"
            f"  {round(movimiento.tipoDeCambio, 4):.4f}"
            f"  {round(movimiento.comision, 2):>6.2f} EUR"
            f" {round(movimiento.total, 2):11,.2f} EUR"
        )
