from abc import ABC, abstractmethod
from typing import Deque, List, Tuple

from ..entidades.movimiento import Movimiento


class Estrategia(ABC):

    def algoritmoFifo(
        self,
        listaMovimientos: List[Movimiento],
    ) -> None:
        self.crearDiccionarios()
        self.listaMovimientosSinCompra: List[Movimiento] = []

        for entrada in listaMovimientos:

            # Compra
            if self.obtencionCompraOVenta(entrada):
                # Se introduce la compra en el diccionario de posiciones
                self.introducirPosicion(entrada)

            # Venta
            else:
                deq = self.obtencionDeque(entrada)
                while deq:
                    # Todavia queda valores o divisas en el movimiento entrada
                    if self.condicionPositiva(deq[-1], entrada):
                        self.transaccionPositiva(deq.pop(), entrada)

                        # El movimiento entrada se compensa con un movimiento compra
                    elif self.condicionIgual(deq[-1], entrada):
                        self.transaccionIgual(deq.pop(), entrada)
                        break

                        # Todavia queda valores o divisas en el movimiento compra
                    else:
                        self.transaccionNegativa(deq[-1], entrada)
                        break

                else:
                    self.listaMovimientosSinCompra.append(entrada)

        # Eliminar las transacciones no transmitidas en el año
        self.borrarTransFueraDeAño()

    def recalcularMovimiento(self, movimiento: Movimiento) -> None:
        movimiento.valorLocal = -movimiento.numero * movimiento.precio
        movimiento.valor = movimiento.valorLocal * movimiento.tipoDeCambio
        movimiento.total = movimiento.valor + movimiento.comision

    def borrarTransFueraDeAño(self) -> None:
        """
        for key in self.transacciones:  # type: ignore
            transaccionesBorrar = []
            for transaccion in self.transacciones[key]:  # type: ignore
                if transaccion.transmision.fecha.year != self.añoRenta:  # type: ignore
                    transaccionesBorrar.append(transaccion)

            if transaccionesBorrar:
                for fila in transaccionesBorrar:
                    self.transacciones[key].remove(fila)  # type: ignore
        """
        for key in self.transacciones:  # type: ignore
            self.transacciones[key][:] = [  # type: ignore
                trans
                for trans in self.transacciones[key]  # type: ignore
                if trans.transmision.fecha.year == self.añoRenta  # type: ignore
            ]

    @abstractmethod
    def obtenerTransacciones(
        self, añoRenta: int, listaMovimientos: List[Movimiento]
    ) -> Tuple:
        pass

    @abstractmethod
    def crearDiccionarios(self) -> None:
        pass

    @abstractmethod
    def obtencionCompraOVenta(self, entrada: Movimiento) -> bool:
        pass

    @abstractmethod
    def introducirPosicion(self, entrada: Movimiento) -> None:
        pass

    @abstractmethod
    def obtencionDeque(self, entrada: Movimiento) -> Deque[Movimiento]:
        pass

    @abstractmethod
    def condicionPositiva(self, compra: Movimiento, entrada: Movimiento) -> bool:
        pass

    @abstractmethod
    def condicionIgual(self, compra: Movimiento, entrada: Movimiento) -> bool:
        pass

    @abstractmethod
    def transaccionPositiva(self, compra: Movimiento, entrada: Movimiento) -> None:
        pass

    @abstractmethod
    def transaccionIgual(self, compra: Movimiento, entrada: Movimiento) -> None:
        pass

    @abstractmethod
    def transaccionNegativa(self, compra: Movimiento, entrada: Movimiento) -> None:
        pass
