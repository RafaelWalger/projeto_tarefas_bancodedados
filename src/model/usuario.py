

class Usuario:
    def __init__(self, id_usuario=None, nome="", email="", cargo=None):
        self.__id_usuario = id_usuario
        self.__nome = nome
        self.__email = email
        self.__cargo = cargo

    # ---- getters ----
    def get_id_usuario(self):
        return self.__id_usuario

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def get_cargo(self):
        return self.__cargo

    # ---- setters ----
    def set_id_usuario(self, id_usuario):
        self.__id_usuario = id_usuario

    def set_nome(self, nome):
        self.__nome = nome

    def set_email(self, email):
        self.__email = email

    def set_cargo(self, cargo):
        self.__cargo = cargo

    def to_string(self):
        return (
            "  ID.....: {}\n"
            "  Nome...: {}\n"
            "  E-mail.: {}\n"
            "  Cargo..: {}"
        ).format(self.__id_usuario, self.__nome, self.__email, self.__cargo or "-")
