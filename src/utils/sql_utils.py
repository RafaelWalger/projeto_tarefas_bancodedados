

def texto(valor):
    if valor is None or str(valor).strip() == "":
        return "NULL"
    return "'" + str(valor).replace("'", "''") + "'"


def inteiro(valor):
    if valor is None:
        return "NULL"
    return str(int(valor))


def decimal(valor):
    if valor is None:
        return "NULL"
    return "{:.2f}".format(round(float(valor), 2))


def data(valor):
    if valor is None:
        return "NULL"
    return "TO_DATE('" + valor.strftime("%d/%m/%Y") + "', 'DD/MM/YYYY')"
