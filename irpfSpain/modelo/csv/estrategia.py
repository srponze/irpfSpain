from abc import ABC, abstractmethod
from datetime import date, time
from typing import List

from ..entidades.movimiento import Movimiento
from .constantes.columnas import *


class Estrategia(ABC):

    @abstractmethod
    def obtenerMovimientos(
        self,
        añoRenta: int,
        listaDivisas: List[str],
        Path: str,
    ) -> List[Movimiento]:
        pass

    def obtenerFecha(self, row) -> date:
        stringFecha = row[l(FECHA)]
        dia, mes, año = stringFecha.split("-")
        return date(int(año), int(mes), int(dia))

    def obtenerHora(self, row: List[str]) -> time:
        stringHora = row[l(HORA)]
        hora, minutos = stringHora.split(":")
        return time(int(hora), int(minutos))

    def borrarMovimientosPosterioresAlAño(
        self, listaMovimientos: List[Movimiento], añoRenta: int
    ):
        listaMovimientos[:] = [
            mov for mov in listaMovimientos if mov.fecha.year <= añoRenta
        ]
