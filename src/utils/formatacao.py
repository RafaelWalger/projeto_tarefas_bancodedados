from datetime import date, datetime
from decimal import Decimal


def formatar_data(valor):
    if valor is None:
        return "-"
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%d/%m/%Y")
    return str(valor)


def formatar_valor(valor, duas_casas=False):
    if valor is None:
        return "-"
    if isinstance(valor, (date, datetime)):
        return formatar_data(valor)
    if isinstance(valor, (int, float, Decimal)) and not isinstance(valor, bool):
        if duas_casas or isinstance(valor, (float, Decimal)):
            return "{:.2f}".format(float(valor))
        return str(valor)
    return str(valor)
