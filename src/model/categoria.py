

class Categoria:
    def __init__(self, id_categoria=None, nome="", descricao=None):
        self.__id_categoria = id_categoria
        self.__nome = nome
        self.__descricao = descricao

    # ---- getters ----
    def get_id_categoria(self):
        return self.__id_categoria

    def get_nome(self):
        return self.__nome

    def get_descricao(self):
        return self.__descricao

    # ---- setters ----
    def set_id_categoria(self, id_categoria):
        self.__id_categoria = id_categoria

    def set_nome(self, nome):
        self.__nome = nome

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def to_string(self):
        return (
            "  ID.........: {}\n"
            "  Nome.......: {}\n"
            "  Descrição..: {}"
        ).format(self.__id_categoria, self.__nome, self.__descricao or "-")
