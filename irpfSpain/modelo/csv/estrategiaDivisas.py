import csv
from typing import List

from ..entidades.movimiento import Movimiento
from .constantes.columnas import *
from .constantes.constantes import *
from .estrategia import Estrategia


class EstrategiaDivisas(Estrategia):

    def obtenerMovimientos(
        self,
        añoRenta: int,
        listaDivisas: List[str],
        Path: str,
    ) -> List[Movimiento]:

        listaMovimientos = []

        with open(Path, newline="") as csvaccount:
            reader = csv.reader(csvaccount)
            next(reader)
            for row in (row for row in reader if row[l(A_DIVISA)] in listaDivisas):
                if row[l(A_TIPODECAMBIO)] != "" and row[l(A_PRODUCTO)] != "":

                    if float(row[l(A_VARIACION)].replace(",", ".")) > 0:
                        activo = "Ingreso de " + row[l(A_DIVISA)]
                        numero = -1
                    else:
                        activo = "Retirada de " + row[l(A_DIVISA)]
                        numero = 1

                    listaMovimientos.append(self.crearMovimiento(row, activo, numero))

        super().borrarMovimientosPosterioresAlAño(listaMovimientos, añoRenta)

        listaMovimientos.reverse()
        return listaMovimientos

    def crearMovimiento(self, row: List[str], activo: str, numero: int) -> Movimiento:

        precio = abs(float(row[l(A_VARIACION)].replace(",", ".")))
        valorLocal = -precio * numero
        tipoDeCambio = 1 / float(row[l(A_TIPODECAMBIO)].replace(",", "."))
        valor = valorLocal * tipoDeCambio
        total = valor + COMISION_FIJA_CAMBIO
        return Movimiento(
            fecha=super().obtenerFecha(row),
            hora=super().obtenerHora(row),
            activo=activo,
            bolsa="",
            isin=row[l(A_ISIN)],
            numero=numero,
            precio=precio,
            divisa=row[l(A_DIVISA)],
            valorLocal=valorLocal,
            valor=valor,
            tipoDeCambio=tipoDeCambio,
            comision=-COMISION_FIJA_CAMBIO,
            total=total,
        )
