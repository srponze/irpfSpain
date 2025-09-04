import csv
from typing import List

from irpfSpain.modelo.csv.constantes.columnas import *
from irpfSpain.modelo.csv.estrategia import Estrategia
from irpfSpain.modelo.entidades.movimiento import Movimiento


class EstrategiaActivos(Estrategia):

    def obtenerMovimientos(
        self,
        añoRenta: int,
        listaDivisas: List[str],
        Path: str,
    ) -> List[Movimiento]:

        listaMovimientos = []

        with open(Path, newline="") as csvtransactions:
            reader = csv.reader(csvtransactions)
            next(reader)
            for row in (row for row in reader if row[l(T_DIVISA)] in listaDivisas):
                tipoDeCambio = (
                    1 / float(row[l(T_TIPODECAMBIO)].replace(",", "."))
                    if row[l(T_TIPODECAMBIO)]
                    else 1
                )
                comision = (
                    float(row[l(T_COMISION)].replace(",", "."))
                    if row[l(T_COMISION)]
                    else 0.0
                )
                numero = round(float(row[l(T_NUMERO)]))
                precio = float(row[l(T_PRECIO)].replace(",", "."))

                listaMovimientos.append(
                    self.crearMovimiento(row, tipoDeCambio, comision, numero, precio)
                )

        super().borrarMovimientosPosterioresAlAño(listaMovimientos, añoRenta)

        listaMovimientos.reverse()
        return listaMovimientos

    def crearMovimiento(
        self,
        row: List[str],
        tipoDeCambio: float,
        comision: float,
        numero: int,
        precio: float,
    ) -> Movimiento:

        return Movimiento(
            fecha=super().obtenerFecha(row),
            hora=super().obtenerHora(row),
            activo=row[l(T_PRODUCTO)],
            bolsa=row[l(T_BOLSA)],
            isin=row[l(T_ISIN)],
            numero=numero,
            precio=precio,
            divisa=row[l(T_DIVISA)],
            valorLocal=float(row[l(T_VALORLOCAL)].replace(",", ".")),
            valor=float(row[l(T_VALOR)].replace(",", ".")),
            tipoDeCambio=tipoDeCambio,
            comision=comision,
            total=float(row[l(T_TOTAL)].replace(",", ".")),
        )
