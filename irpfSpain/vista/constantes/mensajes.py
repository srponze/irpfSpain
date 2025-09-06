## Mensajes Generales

MENSAJE_OPCIONES = "Selecciona una opción"
SEPARACION = "-" * 30

## Mensajes Menu Principal

TITULO_PRINCIPAL = "\n########## IRPF SPAIN ##########"
OPCIONES_PRINCIPALES = ["Analizar documentos", "Salir"]

## Mensajes Analisis

TITULO_ANALISIS = "########## ANALISIS ##########"
MENSAJE_COMPROBACIONES = "Realizando comprobaciones..."

MENSAJE_TRANSACTIONS = "Transactions.csv detectado y sin errores.\n"
MENSAJE_ERRORES_TRANSACTIONS = "Errores en el archivo Transactions.csv"
MENSAJE_ACCOUNT = "Account.csv detectado y sin errores.\n"
MENSAJE_ERRORES_ACCOUNT = "Errores en el archivo Account.csv"
MENSAJE_AÑO_RENTA = "Año de renta correcto.\n"
MENSAJE_ERRORES_AÑO_RENTA = "Errores en el año de renta"
PREGUNTA_AÑO_RENTA = "Introduce el año a calcular"

OPCIONES_ANALISIS = ["Reintentar", "Atras"]

## Mensajes Ayuda

TITULO_AYUDA = "########## AYUDA ##########"

# Mensajes Resultados

TITULO_RESULTADOS = "\n########## RESULTADOS ##########"
MENSAJE_ERRORES_MOVIMIENTOS_ACTIVOS = (
    "Errores en los movimientos de activos, consulta la sección para verlos"
)
MENSAJE_ERRORES_MOVIMIENTOS_DIVISAS = (
    "Errores en los movimientos de divisas extranjeras, consulta la sección para verlos"
)
MENSAJE_OPCIONES_RESULTADOS = "Selecciona una opción para mostrar"
OPCIONES_RESULTADOS = [
    "Movimientos de Activos",
    "Movimientos de Divisas Extranjeras",
    "Transacciones de Activos",
    "Transacciones de Divisas Extranjeras",
    "Volver a menu principal",
    "Salir",
]

OPCIONES_AUXILIARES_RESULTADOS = ["Volver", "Salir"]

TITULO_MOVIMIENTOS_ACTIVOS = "\n########## MOVIMIENTOS DE ACTIVOS ##########"
TITULO_MOVIMIENTOS_DIVISAS = "\n########## MOVIMIENTOS DE DIVISAS EXTRANJERA ##########"
TITULO_TRANSACCIONES_ACTIVOS = "\n########## TRANSACCIONES DE ACTIVOS ##########"
TITULO_TRANSACCIONES_DIVISAS = (
    "\n########## TRANSACCIONES DE DIVISAS EXTRANJERAS ##########"
)

TITULO_POSICIONES_ACTIVOS = (
    "\n########## POSICIONES DE ACTIVOS A FINAL DEL PERIODO ##########"
)
TITULO_POSICIONES_DIVISAS = (
    "\n########## POSICIONES DE DIVISAS A FINAL DEL PERIODO ##########"
)

TITULO_VENTAS_SIN_COMPRA_PREVIA = "\n########## VENTAS SIN COMPRA PREVIA ##########"


MENSAJE_CABECERA_ACTIVOS = (
    f"{"FECHA":-<10}  {"HORA":-<8}  {"ACTIVO":-<22}"
    f" {"ISIN":-<12} {"NUMERO":->5}"
    f" {"PRECIO":->11}"
    f" {"VALOR LOCAL":->15}"
    f" {"VALOR":->15}"
    f" {"TIPO":->7}"
    f" {"COMISION":->10}"
    f" {"TOTAL":->15}"
)

MENSAJE_CABECERA_DIVISAS = (
    f"{"FECHA":-<10}  {"HORA":-<8}  {"ACTIVO":-<22}"
    f" {"VALOR LOCAL":->15}"
    f" {"VALOR":->15}"
    f" {"TIPO":->7}"
    f" {"COMISION":->11}"
    f" {"TOTAL":->15}"
)
