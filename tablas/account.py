from pathlib import Path

import pandas as pd
from pandas import DataFrame

from constantes import (
    DIVISA,
    FECHA,
    HORA,
    ORDEN_ACCOUNT,
    ORDEN_ACCOUNT_CSV,
    PRODUCTO,
    SALDO,
    TIPO,
    USECOLS_ACCOUNT_CSV,
    VARIACION,
)
from tablas.funciones import fecha, fecha_hora, punto_x_coma
from tablas.usdeur import obtener_tipos_usdeur


def leer_account(ruta: Path) -> DataFrame:

    account: DataFrame = pd.read_csv(
        ruta,
        header=0,
        names=ORDEN_ACCOUNT_CSV,
        usecols=USECOLS_ACCOUNT_CSV,
        converters={
            FECHA: fecha,
            TIPO: punto_x_coma,
            VARIACION: punto_x_coma,
            SALDO: punto_x_coma,
        },
    )[ORDEN_ACCOUNT]

    account: DataFrame = account.dropna(subset=[HORA]).reset_index(drop=True)
    account: DataFrame = fecha_hora(account)

    return account


def leer_account_bce(ruta: Path) -> DataFrame:

    account: DataFrame = pd.read_csv(
        ruta,
        header=0,
        names=ORDEN_ACCOUNT_CSV,
        usecols=USECOLS_ACCOUNT_CSV,
        converters={
            FECHA: fecha,
            TIPO: punto_x_coma,
            VARIACION: punto_x_coma,
            SALDO: punto_x_coma,
        },
    )[ORDEN_ACCOUNT]

    account: DataFrame = account.dropna(subset=[HORA]).reset_index(drop=True)
    account: DataFrame = aplicar_tipos_bce(account)
    account: DataFrame = fecha_hora(account)

    return account


def aplicar_tipos_bce(account: DataFrame) -> DataFrame:
    tipos_bce: DataFrame = obtener_tipos_usdeur()
    mask_usd = (account[PRODUCTO].str.startswith("EUR/")) & (account[DIVISA] == "USD")
    if mask_usd.any():
        fx = (
            account.loc[mask_usd, [FECHA]]
            .assign(
                **{
                    FECHA: pd.to_datetime(
                        account.loc[mask_usd, FECHA],
                        format="%Y-%m-%d",
                        errors="coerce",
                    ),
                },
            )
            .merge(tipos_bce, on=FECHA, how="left")
        )

        account.loc[mask_usd, TIPO] = fx[TIPO].to_numpy()

    return account
