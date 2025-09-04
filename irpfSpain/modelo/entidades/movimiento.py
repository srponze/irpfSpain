from datetime import date, time


class Movimiento:

    def __init__(
        self,
        fecha: date,
        hora: time,
        activo: str,
        bolsa: str,
        isin: str,
        numero: int,
        precio: float,
        divisa: str,
        valorLocal: float,
        valor: float,
        tipoDeCambio: float,
        comision: float,
        total: float,
    ):
        self.fecha: date = fecha
        self.hora: time = hora
        self.activo: str = activo
        self.bolsa: str = bolsa
        self.isin: str = isin
        self.numero: int = numero
        self.precio: float = precio
        self.divisa: str = divisa
        self.valorLocal: float = valorLocal
        self.valor: float = valor
        self.tipoDeCambio: float = tipoDeCambio
        self.comision: float = comision
        self.total: float = total

    def __str__(self):
        return (
            f"{self.fecha}  {self.hora}  {self.activo[0:21]:22}"
            f" {self.isin}  {self.numero:5}"
            f" {round(self.precio, 2):7,.2f} {self.divisa}"
            f" {round(self.valorLocal, 2):11,.2f} {self.divisa}"
            f" {round(self.valor, 2):11,.2f} EUR"
            f"  {round(self.tipoDeCambio, 4):.4f}"
            f"  {round(self.comision, 2):.2f} EUR"
            f" {round(self.total, 2):11,.2f} EUR"
        )
