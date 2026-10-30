
import re
import sys
from datetime import date

import oracledb

from controller.controller_categoria import ControllerCategoria
from controller.controller_tarefa import ControllerTarefa
from controller.controller_usuario import ControllerUsuario
from model.categoria import Categoria
from model.tarefa import PRIORIDADES_VALIDAS, STATUS_VALIDOS, Tarefa
from model.usuario import Usuario
from reports.relatorios import Relatorios
from utils import config
from utils.interface import (cabecalho, confirmar, escolher_da_lista, escolher_id,
                             exibir_menu, imprimir_tabela, ler_data, ler_decimal,
                             ler_texto, limpar_tela, pausar)
from utils.splash_screen import SplashScreen

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")



def tabela_usuarios(usuarios):
    colunas = ["ID", "NOME", "E-MAIL", "CARGO"]
    linhas = [[u.get_id_usuario(), u.get_nome(), u.get_email(), u.get_cargo()] for u in usuarios]
    return colunas, linhas


def tabela_categorias(categorias):
    colunas = ["ID", "NOME", "DESCRIÇÃO"]
    linhas = [[c.get_id_categoria(), c.get_nome(), c.get_descricao()] for c in categorias]
    return colunas, linhas


def tabela_tarefas(tarefas):
    colunas = ["ID", "TÍTULO", "USUÁRIO", "CATEGORIA", "STATUS"]
    linhas = [[t.get_id_tarefa(), t.get_titulo(), t.get_usuario().get_nome(),
               t.get_categoria().get_nome(), t.get_status()] for t in tarefas]
    return colunas, linhas



def executar_seguro(acao, *args):
    """Executa a ação tratando erros. Em caso de erro, devolve True (segue o fluxo normal)."""
    try:
        return acao(*args)
    except ValueError as erro:
        print("\n⚠ {}".format(erro))
    except oracledb.IntegrityError as erro:
        print("\n✖ O banco recusou a operação (restrição de integridade):\n  {}".format(erro))
    except oracledb.Error as erro:
        print("\n✖ Erro no banco de dados:\n  {}".format(erro))
    return True



def ler_email(controller, atual=None, ignorar_id=None):
    while True:
        email = ler_texto("E-mail", 100, atual=atual)
        if not EMAIL_REGEX.match(email):
            print("⚠ E-mail inválido (exemplo: nome@dominio.com).")
            continue
        if controller.existe_email(email, ignorar_id=ignorar_id):
            print("⚠ Já existe um usuário com este e-mail.")
            continue
        return email


def ler_nome_categoria(controller, atual=None, ignorar_id=None):
    while True:
        nome = ler_texto("Nome da categoria", 50, atual=atual)
        if controller.existe_nome(nome, ignorar_id=ignorar_id):
            print("⚠ Já existe uma categoria com este nome.")
            continue
        return nome



def menu_relatorios():
    relatorios = Relatorios()
    acoes = {
        "1": relatorios.tarefas_por_usuario,
        "2": relatorios.tarefas_por_categoria,
        "3": relatorios.tarefas_detalhadas,
    }
    while True:
        opcao = exibir_menu("RELATÓRIOS", config.MENU_RELATORIOS)
        if opcao == "0":
            return
        limpar_tela()
        executar_seguro(acoes[opcao])
        pausar()



def inserir_usuario():
    cabecalho("NOVO USUÁRIO")
    controller = ControllerUsuario()
    nome = ler_texto("Nome", 100)
    email = ler_email(controller)
    cargo = ler_texto("Cargo", 50, obrigatorio=False)
    usuario = controller.inserir(Usuario(None, nome, email, cargo))
    print("\n✔ Usuário cadastrado com sucesso.")
    print(usuario.to_string())
    return True


def inserir_categoria():
    cabecalho("NOVA CATEGORIA")
    controller = ControllerCategoria()
    nome = ler_nome_categoria(controller)
    descricao = ler_texto("Descrição", 200, obrigatorio=False)
    categoria = controller.inserir(Categoria(None, nome, descricao))
    print("\n✔ Categoria cadastrada com sucesso.")
    print(categoria.to_string())
    return True


def inserir_tarefa():
    cabecalho("NOVA TAREFA")
    usuarios = ControllerUsuario().listar()
    categorias = ControllerCategoria().listar()
    if not usuarios or not categorias:
        raise ValueError("Cadastre ao menos 1 usuário e 1 categoria antes de criar tarefas.")

    titulo = ler_texto("Título", 150)
    descricao = ler_texto("Descrição", 500, obrigatorio=False)
    status = escolher_da_lista("Status", STATUS_VALIDOS, padrao="Pendente")
    prioridade = escolher_da_lista("Prioridade", PRIORIDADES_VALIDAS, padrao="Media")
    data_criacao = ler_data("Data de criação", padrao=date.today())
    data_conclusao = None
    if status == "Concluida":
        data_conclusao = ler_data("Data de conclusão", padrao=max(date.today(), data_criacao),
                                  minimo=data_criacao)
    horas = ler_decimal("Horas gastas", padrao=0.0)

    print("\nUsuários disponíveis:")
    imprimir_tabela(*tabela_usuarios(usuarios))
    id_usuario = escolher_id("ID do usuário responsável", [u.get_id_usuario() for u in usuarios])
    print("\nCategorias disponíveis:")
    imprimir_tabela(*tabela_categorias(categorias))
    id_categoria = escolher_id("ID da categoria", [c.get_id_categoria() for c in categorias])

    usuario = next(u for u in usuarios if u.get_id_usuario() == id_usuario)
    categoria = next(c for c in categorias if c.get_id_categoria() == id_categoria)
    tarefa = Tarefa(None, titulo, descricao, status, prioridade, data_criacao,
                    data_conclusao, horas, usuario, categoria)
    tarefa = ControllerTarefa().inserir(tarefa)
    print("\n✔ Tarefa cadastrada com sucesso.")
    print(tarefa.to_string())
    return True


def menu_inserir():
    acoes = {"1": inserir_usuario, "2": inserir_categoria, "3": inserir_tarefa}
    while True:
        opcao = exibir_menu("INSERIR REGISTROS - escolha a entidade", config.MENU_ENTIDADES)
        if opcao == "0":
            return
        limpar_tela()
        executar_seguro(acoes[opcao])
        if not confirmar("\nDeseja inserir mais algum registro?"):
            return



def remover_registro(rotulo, controller, montar_tabela):
    """Fluxo de remoção genérico. Devolve False se o usuário desistiu
    (volta ao menu principal) e True para perguntar se quer remover mais."""
    cabecalho("REMOVER - {}".format(rotulo.upper()))
    registros = controller.listar()
    if not registros:
        print("\nNão há registros cadastrados nesta entidade.")
        return True

    colunas, linhas = montar_tabela(registros)
    print()
    imprimir_tabela(colunas, linhas)
    id_escolhido = escolher_id("\nID do registro que deseja remover",
                               [linha[0] for linha in linhas], permitir_cancelar=True)
    if id_escolhido is None:
        print("\nOperação cancelada.")
        return False

    print("\nRegistro selecionado:")
    print(controller.buscar(id_escolhido).to_string())
    if not confirmar("\nTem certeza que deseja remover este registro?"):
        print("\nRemoção cancelada.")
        return False

    
    dependentes = controller.contar_dependentes(id_escolhido)
    excluir_dependentes = False
    if dependentes > 0:
        print("\n⚠ Este registro está vinculado a {} tarefa(s) (chave estrangeira).".format(dependentes))
        if not confirmar("Deseja remover também essas tarefas para poder excluir o registro?"):
            print("\nO registro NÃO foi removido, pois possui tarefas vinculadas.")
            return True
        excluir_dependentes = True

    controller.excluir(id_escolhido, excluir_dependentes)
    if excluir_dependentes:
        print("\n✔ Registro e tarefas vinculadas removidos com sucesso.")
    else:
        print("\n✔ Registro removido com sucesso.")
    return True


def menu_remover():
    entidades = {
        "1": ("Usuários", ControllerUsuario(), tabela_usuarios),
        "2": ("Categorias", ControllerCategoria(), tabela_categorias),
        "3": ("Tarefas", ControllerTarefa(), tabela_tarefas),
    }
    while True:
        opcao = exibir_menu("REMOVER REGISTROS - escolha a entidade", config.MENU_ENTIDADES)
        if opcao == "0":
            return
        limpar_tela()
        continuar = executar_seguro(remover_registro, *entidades[opcao])
        if not continuar:
            pausar()
            return
        if not confirmar("\nDeseja remover mais algum registro?"):
            return



def atualizar_usuario():
    cabecalho("ATUALIZAR - USUÁRIOS")
    controller = ControllerUsuario()
    usuarios = controller.listar()
    if not usuarios:
        print("\nNão há usuários cadastrados.")
        return True
    print()
    imprimir_tabela(*tabela_usuarios(usuarios))
    id_usuario = escolher_id("\nID do usuário que deseja atualizar",
                             [u.get_id_usuario() for u in usuarios], permitir_cancelar=True)
    if id_usuario is None:
        print("\nOperação cancelada.")
        return False

    atual = controller.buscar(id_usuario)
    print("\nRegistro atual:")
    print(atual.to_string())
    print("\nInforme os novos dados (ENTER mantém o valor atual):\n")
    nome = ler_texto("Nome", 100, atual=atual.get_nome())
    email = ler_email(controller, atual=atual.get_email(), ignorar_id=id_usuario)
    cargo = ler_texto("Cargo", 50, obrigatorio=False, atual=atual.get_cargo())

    controller.atualizar(Usuario(id_usuario, nome, email, cargo))
    print("\n✔ Usuário atualizado. Dados atuais:")
    print(controller.buscar(id_usuario).to_string())
    return True


def atualizar_categoria():
    cabecalho("ATUALIZAR - CATEGORIAS")
    controller = ControllerCategoria()
    categorias = controller.listar()
    if not categorias:
        print("\nNão há categorias cadastradas.")
        return True
    print()
    imprimir_tabela(*tabela_categorias(categorias))
    id_categoria = escolher_id("\nID da categoria que deseja atualizar",
                               [c.get_id_categoria() for c in categorias], permitir_cancelar=True)
    if id_categoria is None:
        print("\nOperação cancelada.")
        return False

    atual = controller.buscar(id_categoria)
    print("\nRegistro atual:")
    print(atual.to_string())
    print("\nInforme os novos dados (ENTER mantém o valor atual):\n")
    nome = ler_nome_categoria(controller, atual=atual.get_nome(), ignorar_id=id_categoria)
    descricao = ler_texto("Descrição", 200, obrigatorio=False, atual=atual.get_descricao())

    controller.atualizar(Categoria(id_categoria, nome, descricao))
    print("\n✔ Categoria atualizada. Dados atuais:")
    print(controller.buscar(id_categoria).to_string())
    return True


def atualizar_tarefa():
    cabecalho("ATUALIZAR - TAREFAS")
    controller = ControllerTarefa()
    tarefas = controller.listar()
    if not tarefas:
        print("\nNão há tarefas cadastradas.")
        return True
    print()
    imprimir_tabela(*tabela_tarefas(tarefas))
    id_tarefa = escolher_id("\nID da tarefa que deseja atualizar",
                            [t.get_id_tarefa() for t in tarefas], permitir_cancelar=True)
    if id_tarefa is None:
        print("\nOperação cancelada.")
        return False

    atual = controller.buscar(id_tarefa)
    print("\nRegistro atual:")
    print(atual.to_string())
    print("\nInforme os novos dados (ENTER mantém o valor atual):\n")

    titulo = ler_texto("Título", 150, atual=atual.get_titulo())
    descricao = ler_texto("Descrição", 500, obrigatorio=False, atual=atual.get_descricao())
    status = escolher_da_lista("Status", STATUS_VALIDOS, atual=atual.get_status())
    prioridade = escolher_da_lista("Prioridade", PRIORIDADES_VALIDAS, atual=atual.get_prioridade())
    data_criacao = ler_data("Data de criação", padrao=atual.get_data_criacao())
    data_conclusao = None
    if status == "Concluida":
        padrao = atual.get_data_conclusao() or max(date.today(), data_criacao)
        data_conclusao = ler_data("Data de conclusão", padrao=max(padrao, data_criacao),
                                  minimo=data_criacao)
    horas = ler_decimal("Horas gastas", atual=atual.get_horas_gastas())

    usuarios = ControllerUsuario().listar()
    print("\nUsuários disponíveis:")
    imprimir_tabela(*tabela_usuarios(usuarios))
    id_usuario = escolher_id("ID do usuário responsável", [u.get_id_usuario() for u in usuarios],
                             atual=atual.get_usuario().get_id_usuario())
    categorias = ControllerCategoria().listar()
    print("\nCategorias disponíveis:")
    imprimir_tabela(*tabela_categorias(categorias))
    id_categoria = escolher_id("ID da categoria", [c.get_id_categoria() for c in categorias],
                               atual=atual.get_categoria().get_id_categoria())

    usuario = next(u for u in usuarios if u.get_id_usuario() == id_usuario)
    categoria = next(c for c in categorias if c.get_id_categoria() == id_categoria)
    controller.atualizar(Tarefa(id_tarefa, titulo, descricao, status, prioridade,
                                data_criacao, data_conclusao, horas, usuario, categoria))
    print("\n✔ Tarefa atualizada. Dados atuais:")
    print(controller.buscar(id_tarefa).to_string())
    return True


def menu_atualizar():
    acoes = {"1": atualizar_usuario, "2": atualizar_categoria, "3": atualizar_tarefa}
    while True:
        opcao = exibir_menu("ATUALIZAR REGISTROS - escolha a entidade", config.MENU_ENTIDADES)
        if opcao == "0":
            return
        limpar_tela()
        continuar = executar_seguro(acoes[opcao])
        if not continuar:
            pausar()
            return
        if not confirmar("\nDeseja atualizar mais algum registro?"):
            return



def mostrar_splash():
    limpar_tela()
    print(SplashScreen().get_updated_screen())
    pausar()


def executar():
    try:
        mostrar_splash()
    except (RuntimeError, oracledb.Error) as erro:
        print("\n✖ Não foi possível conectar ao banco de dados Oracle:\n  {}".format(erro))
        print("\nConfira o arquivo .env (usuário, senha, host, porta e serviço) e se")
        print("as tabelas foram criadas com o script database/criar_tabelas.sql.")
        sys.exit(1)

    while True:
        opcao = exibir_menu("{} - MENU PRINCIPAL".format(config.NOME_SISTEMA), config.MENU_PRINCIPAL)
        if opcao == "1":
            menu_relatorios()
        elif opcao == "2":
            menu_inserir()
        elif opcao == "3":
            menu_remover()
        elif opcao == "4":
            menu_atualizar()
        elif opcao == "5":
            print("\nObrigado por utilizar o sistema. Até logo.\n")
            break


if __name__ == "__main__":
    try:
        executar()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSistema encerrado pelo usuário.\n")
