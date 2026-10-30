from conexion.oracle_queries import OracleQueries
from model.usuario import Usuario
from utils import sql_utils as sq


class ControllerUsuario:

    def listar(self):
        sql = "select id_usuario, nome, email, cargo from usuario order by id_usuario"
        with OracleQueries() as db:
            _, linhas = db.query(sql)
        return [Usuario(l[0], l[1], l[2], l[3]) for l in linhas]

    def buscar(self, id_usuario):
        """Devolve o Usuario ou None se não existir."""
        sql = ("select id_usuario, nome, email, cargo from usuario where id_usuario = "
               + sq.inteiro(id_usuario))
        with OracleQueries() as db:
            _, linhas = db.query(sql)
        if not linhas:
            return None
        l = linhas[0]
        return Usuario(l[0], l[1], l[2], l[3])

    # ---- verificações de existência ----
    def existe_id(self, id_usuario):
        sql = "select count(1) from usuario where id_usuario = " + sq.inteiro(id_usuario)
        with OracleQueries() as db:
            return db.scalar(sql) > 0

    def existe_email(self, email, ignorar_id=None):
        sql = "select count(1) from usuario where lower(email) = lower(" + sq.texto(email) + ")"
        if ignorar_id is not None:
            sql += " and id_usuario <> " + sq.inteiro(ignorar_id)
        with OracleQueries() as db:
            return db.scalar(sql) > 0

    def contar_dependentes(self, id_usuario):
        """Quantas tarefas referenciam este usuário (FK)."""
        sql = "select count(1) from tarefa where id_usuario = " + sq.inteiro(id_usuario)
        with OracleQueries() as db:
            return db.scalar(sql)

    # ---- operações ----
    def inserir(self, usuario):
        if self.existe_email(usuario.get_email()):
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")
        with OracleQueries() as db:
            novo_id = db.scalar("select seq_usuario.nextval from dual")
            sql = ("insert into usuario (id_usuario, nome, email, cargo) values ("
                   + sq.inteiro(novo_id) + ", "
                   + sq.texto(usuario.get_nome()) + ", "
                   + sq.texto(usuario.get_email()) + ", "
                   + sq.texto(usuario.get_cargo()) + ")")
            db.execute(sql)
        usuario.set_id_usuario(novo_id)
        return usuario

    def atualizar(self, usuario):
        if not self.existe_id(usuario.get_id_usuario()):
            raise ValueError("Usuário não encontrado.")
        if self.existe_email(usuario.get_email(), ignorar_id=usuario.get_id_usuario()):
            raise ValueError("Já existe outro usuário com este e-mail.")
        sql = ("update usuario set nome = " + sq.texto(usuario.get_nome())
               + ", email = " + sq.texto(usuario.get_email())
               + ", cargo = " + sq.texto(usuario.get_cargo())
               + " where id_usuario = " + sq.inteiro(usuario.get_id_usuario()))
        with OracleQueries() as db:
            db.execute(sql)
        return usuario

    def excluir(self, id_usuario, excluir_dependentes=False):
        if not self.existe_id(id_usuario):
            raise ValueError("Usuário não encontrado.")
        if self.contar_dependentes(id_usuario) > 0 and not excluir_dependentes:
            raise ValueError("Este usuário possui tarefas vinculadas e não pode ser removido.")
        with OracleQueries() as db:
            # as duas exclusões ficam na mesma transação (tudo ou nada)
            if excluir_dependentes:
                db.execute("delete from tarefa where id_usuario = " + sq.inteiro(id_usuario),
                           commit=False)
            db.execute("delete from usuario where id_usuario = " + sq.inteiro(id_usuario),
                       commit=False)
            db.commit()
