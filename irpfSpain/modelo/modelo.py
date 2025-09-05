import copy
import os
import sys
from bisect import insort
from collections import defaultdict, deque
from pathlib import Path
from typing import DefaultDict, Deque, Dict, List, Tuple

from irpfSpain.modelo.csv.csv import Csv
from irpfSpain.modelo.csv.estrategiaActivos import (
    EstrategiaActivos as Csv_EstrategiaActivos,
)
from irpfSpain.modelo.csv.estrategiaActivosDivisas import (
    EstrategiaActivosDivisas as Csv_EstrategiaActivosDivisas,
)
from irpfSpain.modelo.csv.estrategiaDivisas import (
    EstrategiaDivisas as Csv_EstrategiaDivisas,
)
from irpfSpain.modelo.entidades.movimiento import Movimiento
from irpfSpain.modelo.entidades.transaccion import Transaccion
from irpfSpain.modelo.fifo.estrategiaActivos import (
    EstrategiaActivos as Fifo_EstrategiaActivos,
)
from irpfSpain.modelo.fifo.estrategiaDivisas import (
    EstrategiaDivisas as Fifo_EstrategiaDivisas,
)
from irpfSpain.modelo.fifo.fifo import Fifo
from irpfSpain.modelo.funciones import Funciones
from irpfSpain.modelo.mensajes.mensajesErroresDocumentos import *


class Modelo:

    def __init__(self):
        self.csv = Csv()
        self.fifo = Fifo()
        self.rutaTransaction = Path(os.path.dirname(sys.argv[0])) / "Transactions.csv"
        self.rutaAccount = Path(os.path.dirname(sys.argv[0])) / "Account.csv"

        self.transaccionesActivos: DefaultDict[Tuple[str, str], List[Transaccion]] = (
            defaultdict(list)
        )
        self.listaPosicionesActivos: DefaultDict[Tuple[str, str], Deque[Movimiento]] = (
            defaultdict(deque)
        )
        self.listaMovimientosSinCompraActivos: List[Movimiento] = []

        self.transaccionesDivisas: DefaultDict[str, List[Transaccion]] = defaultdict(
            list
        )
        self.listaPosicionesDivisas: DefaultDict[str, Deque[Movimiento]] = defaultdict(
            deque
        )
        self.listaMovimientosSinCompraDivisas: List[Movimiento] = []

    def comprobarTransactions(self) -> List[str]:
        errores = []
        if not self.rutaTransaction.is_file():
            errores.append(MENSAJE_TRANSACTION_NO_ENCONTRADO)
        return errores

    def comprobarAccount(self) -> List[str]:
        errores = []
        if not self.rutaAccount.is_file():
            errores.append(MENSAJE_ACCOUNT_NO_ENCONTRADO)
        return errores

    def comprobarAñoRenta(self, añoRenta: str) -> List[str]:
        errores = []
        if not añoRenta.isdigit() or len(añoRenta) != 4:
            errores.append(MENSAJE_AÑO_RENTA_NO_VALIDO)
        elif int(añoRenta) > 2100:
            errores.append(MENSAJE_AÑO_RENTA_SUPERIOR)
        elif int(añoRenta) < 1978:
            errores.append(MENSAJE_AÑO_RENTA_INFERIOR)
        self.añoRenta = int(añoRenta)
        return errores

    def obtenerDatos(self) -> Dict:
        return {
            "transaccionesActivos": self.transaccionesActivos,
            "transaccionesDivisas": self.transaccionesDivisas,
            "transaccionesAgrupadas": self.transaccionesAgrupadas,
            "listaMovimientosActivos": self.listaMovimientosActivos,
            "listaPosicionesActivos": self.listaPosicionesActivos,
            "listaMovimientosSinCompraActivos": self.listaMovimientosSinCompraActivos,
            "listaMovimientosDivisas": self.listaMovimientosCompletaDivisas,
            "listaPosicionesDivisas": self.listaPosicionesDivisas,
            "listaMovimientosSinCompraDivisas": self.listaMovimientosSinCompraDivisas,
        }

    def realizarCalculos(self) -> None:

        self.listaDivisas = Funciones.obtenerListaDivisas(self.rutaTransaction)
        self.listaDivisasExtranjeras = self.listaDivisas
        if "EUR" in self.listaDivisasExtranjeras:
            self.listaDivisasExtranjeras.remove("EUR")

        self.calcularActivos()
        self.calcularDivisas()

    def calcularActivos(self) -> None:
        self.csv.establecerEstrategia(Csv_EstrategiaActivos())
        self.listaMovimientosActivos = self.csv.obtenerMovimientos(
            self.añoRenta, self.listaDivisas, self.rutaTransaction
        )

        if self.listaMovimientosActivos:
            Funciones.prorratearComisiones(self.listaMovimientosActivos)

        self.fifo.establecerEstrategia(Fifo_EstrategiaActivos())
        (
            self.transaccionesActivos,
            self.listaPosicionesActivos,
            self.listaMovimientosSinCompraActivos,
        ) = self.fifo.obtenerTransacciones(
            self.añoRenta, copy.deepcopy(self.listaMovimientosActivos)
        )

        self.transaccionesAgrupadas = Funciones.AgruparActivos(
            self.transaccionesActivos
        )

        Funciones.borrarMovimientosNoNecesarios(
            self.listaMovimientosActivos, self.transaccionesActivos, self.añoRenta
        )

    def calcularDivisas(self) -> None:
        self.csv.establecerEstrategia(Csv_EstrategiaDivisas())
        self.listaMovimientosDivisas = self.csv.obtenerMovimientos(
            self.añoRenta, self.listaDivisasExtranjeras, self.rutaAccount
        )
        self.csv.establecerEstrategia(Csv_EstrategiaActivosDivisas())
        self.listaMovimientosActivosParaDivisas = self.csv.obtenerMovimientos(
            self.añoRenta, self.listaDivisasExtranjeras, self.rutaTransaction
        )

        self.listaMovimientosCompletaDivisas = self.listaMovimientosActivosParaDivisas
        for flujo in self.listaMovimientosDivisas:
            insort(
                self.listaMovimientosCompletaDivisas,
                flujo,
                key=lambda x: (x.fecha, x.hora),
            )

        self.fifo.establecerEstrategia(Fifo_EstrategiaDivisas())
        (
            self.transaccionesDivisas,
            self.listaPosicionesDivisas,
            self.listaMovimientosSinCompraDivisas,
        ) = self.fifo.obtenerTransacciones(
            self.añoRenta, copy.deepcopy(self.listaMovimientosCompletaDivisas)
        )
