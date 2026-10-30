import math
import os
from datetime import date, datetime

from utils.formatacao import formatar_data, formatar_valor

LARGURA = 64


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar(mensagem="Pressione ENTER para continuar..."):
    input("\n" + mensagem)


def cabecalho(texto):
    print("=" * LARGURA)
    print(texto.center(LARGURA))
    print("=" * LARGURA)


def exibir_menu(titulo_menu, opcoes):
    limpar_tela()
    while True:
        cabecalho(titulo_menu)
        for chave, descricao in opcoes.items():
            print("  {} - {}".format(chave, descricao))
        print("-" * LARGURA)
        escolha = input("Escolha uma opção: ").strip()
        if escolha in opcoes:
            return escolha
        print("\n⚠ Opção inválida! Tente novamente.\n")


def confirmar(pergunta):
    while True:
        resposta = input("{} (s/n): ".format(pergunta)).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("⚠ Responda com 's' para sim ou 'n' para não.")


def ler_texto(rotulo, max_bytes, obrigatorio=True, atual=None):
    while True:
        dica = ""
        if atual is not None:
            dica = " [atual: {}] (ENTER mantém{})".format(atual, "" if obrigatorio else ", - limpa")
        elif not obrigatorio:
            dica = " (opcional)"
        entrada = input("{}{}: ".format(rotulo, dica)).strip()
        if entrada == "":
            if atual is not None:
                return atual
            if not obrigatorio:
                return None
            print("⚠ Este campo é obrigatório.")
            continue
        if entrada == "-" and not obrigatorio:
            return None
        tamanho = len(entrada.encode("utf-8"))
        if tamanho > max_bytes:
            print("⚠ Texto muito longo (máximo de {} caracteres).".format(max_bytes))
            continue
        return entrada


def ler_decimal(rotulo, minimo=0.0, maximo=9999.99, atual=None, padrao=None):
    referencia = atual if atual is not None else padrao
    while True:
        dica = ""
        if referencia is not None:
            dica = " [{:.2f}, ENTER {}]".format(referencia, "mantém" if atual is not None else "usa este valor")
        entrada = input("{}{}: ".format(rotulo, dica)).strip().replace(",", ".")
        if entrada == "" and referencia is not None:
            return float(referencia)
        try:
            valor = float(entrada)
        except ValueError:
            print("⚠ Digite um número válido (ex.: 2.5).")
            continue
        if not math.isfinite(valor) or valor < minimo or valor > maximo:
            print("⚠ O valor deve estar entre {} e {}.".format(minimo, maximo))
            continue
        return round(valor, 2)


def ler_data(rotulo, padrao=None, minimo=None):
    if isinstance(padrao, datetime):
        padrao = padrao.date()
    while True:
        dica = " (DD/MM/AAAA)"
        if padrao is not None:
            dica += " [ENTER = {}]".format(formatar_data(padrao))
        entrada = input("{}{}: ".format(rotulo, dica)).strip()
        if entrada == "" and padrao is not None:
            valor = padrao
        else:
            try:
                valor = datetime.strptime(entrada, "%d/%m/%Y").date()
            except ValueError:
                print("⚠ Data inválida. Use o formato DD/MM/AAAA.")
                continue
        if minimo is not None and valor < minimo:
            print("⚠ A data não pode ser anterior a {}.".format(formatar_data(minimo)))
            continue
        return valor


def escolher_da_lista(rotulo, opcoes, atual=None, padrao=None):
    print("{}:".format(rotulo))
    for indice, opcao in enumerate(opcoes, 1):
        print("  {} - {}".format(indice, opcao))
    referencia = atual if atual is not None else padrao
    while True:
        dica = ""
        if referencia is not None:
            if atual is not None:
                dica = " [atual: {}, ENTER mantém]".format(referencia)
            else:
                dica = " [padrão: {}, ENTER usa o padrão]".format(referencia)
        entrada = input("Escolha{}: ".format(dica)).strip()
        if entrada == "" and referencia is not None:
            return referencia
        if entrada.isdigit() and 1 <= int(entrada) <= len(opcoes):
            return opcoes[int(entrada) - 1]
        print("⚠ Opção inválida.")


def escolher_id(rotulo, ids_validos, atual=None, permitir_cancelar=False):
    while True:
        dica = ""
        if atual is not None:
            dica = " [atual: {}, ENTER mantém]".format(atual)
        elif permitir_cancelar:
            dica = " (0 = cancelar)"
        entrada = input("{}{}: ".format(rotulo, dica)).strip()
        if entrada == "" and atual is not None:
            return atual
        if entrada.isdigit():
            numero = int(entrada)
            if numero == 0 and permitir_cancelar:
                return None
            if numero in ids_validos:
                return numero
        print("⚠ ID inválido. Escolha um dos IDs listados.")


def imprimir_tabela(colunas, linhas, largura_max=34):
    cabecalhos = [str(coluna).replace("_", " ") for coluna in colunas]
    colunas_horas = ["HORAS" in cab.upper() for cab in cabecalhos]
    dados = [
        [formatar_valor(valor, colunas_horas[i]) for i, valor in enumerate(linha)]
        for linha in linhas
    ]
    larguras = []
    for i, cab in enumerate(cabecalhos):
        maior = max([len(cab)] + [len(linha[i]) for linha in dados])
        larguras.append(min(maior, largura_max))

    def cortar(texto, largura):
        return texto if len(texto) <= largura else texto[: largura - 1] + "…"

    separador = "+-" + "-+-".join("-" * largura for largura in larguras) + "-+"
    print(separador)
    print("| " + " | ".join(cortar(c, l).ljust(l) for c, l in zip(cabecalhos, larguras)) + " |")
    print(separador)
    for linha in dados:
        print("| " + " | ".join(cortar(v, l).ljust(l) for v, l in zip(linha, larguras)) + " |")
    print(separador)


def hoje():
    return date.today()
