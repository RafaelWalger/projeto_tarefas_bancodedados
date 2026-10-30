from datetime import datetime

from utils.formatacao import formatar_data

STATUS_VALIDOS = ["Pendente", "Em andamento", "Concluida"]
PRIORIDADES_VALIDAS = ["Baixa", "Media", "Alta"]


def _somente_data(valor):
    if isinstance(valor, datetime):
        return valor.date()
    return valor


class Tarefa:
    def __init__(self, id_tarefa=None, titulo="", descricao=None, status="Pendente",
                 prioridade="Media", data_criacao=None, data_conclusao=None,
                 horas_gastas=0.0, usuario=None, categoria=None):
        self.__id_tarefa = id_tarefa
        self.__titulo = titulo
        self.__descricao = descricao
        self.__status = status
        self.__prioridade = prioridade
        self.__data_criacao = _somente_data(data_criacao)
        self.__data_conclusao = _somente_data(data_conclusao)
        self.__horas_gastas = float(horas_gastas) if horas_gastas is not None else 0.0
        self.__usuario = usuario        # instância de Usuario
        self.__categoria = categoria    # instância de Categoria

    # ---- getters ----
    def get_id_tarefa(self):
        return self.__id_tarefa

    def get_titulo(self):
        return self.__titulo

    def get_descricao(self):
        return self.__descricao

    def get_status(self):
        return self.__status

    def get_prioridade(self):
        return self.__prioridade

    def get_data_criacao(self):
        return self.__data_criacao

    def get_data_conclusao(self):
        return self.__data_conclusao

    def get_horas_gastas(self):
        return self.__horas_gastas

    def get_usuario(self):
        return self.__usuario

    def get_categoria(self):
        return self.__categoria

    # ---- setters ----
    def set_id_tarefa(self, id_tarefa):
        self.__id_tarefa = id_tarefa

    def set_titulo(self, titulo):
        self.__titulo = titulo

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def set_status(self, status):
        self.__status = status

    def set_prioridade(self, prioridade):
        self.__prioridade = prioridade

    def set_data_criacao(self, data_criacao):
        self.__data_criacao = _somente_data(data_criacao)

    def set_data_conclusao(self, data_conclusao):
        self.__data_conclusao = _somente_data(data_conclusao)

    def set_horas_gastas(self, horas_gastas):
        self.__horas_gastas = float(horas_gastas)

    def set_usuario(self, usuario):
        self.__usuario = usuario

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def to_string(self):
        return (
            "  ID.............: {}\n"
            "  Título.........: {}\n"
            "  Descrição......: {}\n"
            "  Status.........: {}\n"
            "  Prioridade.....: {}\n"
            "  Data de criação: {}\n"
            "  Data conclusão.: {}\n"
            "  Horas gastas...: {:.2f}\n"
            "  Usuário........: {} - {}\n"
            "  Categoria......: {} - {}"
        ).format(
            self.__id_tarefa, self.__titulo, self.__descricao or "-", self.__status,
            self.__prioridade, formatar_data(self.__data_criacao),
            formatar_data(self.__data_conclusao), self.__horas_gastas,
            self.__usuario.get_id_usuario(), self.__usuario.get_nome(),
            self.__categoria.get_id_categoria(), self.__categoria.get_nome(),
        )
