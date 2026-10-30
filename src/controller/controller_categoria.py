
from conexion.oracle_queries import OracleQueries
from model.categoria import Categoria
from utils import sql_utils as sq


class ControllerCategoria:

    def listar(self):
        sql = "select id_categoria, nome, descricao from categoria order by id_categoria"
        with OracleQueries() as db:
            _, linhas = db.query(sql)
        return [Categoria(l[0], l[1], l[2]) for l in linhas]

    def buscar(self, id_categoria):
        """Devolve a Categoria ou None se não existir."""
        sql = ("select id_categoria, nome, descricao from categoria where id_categoria = "
               + sq.inteiro(id_categoria))
        with OracleQueries() as db:
            _, linhas = db.query(sql)
        if not linhas:
            return None
        l = linhas[0]
        return Categoria(l[0], l[1], l[2])

    # ---- verificações de existência ----
    def existe_id(self, id_categoria):
        sql = "select count(1) from categoria where id_categoria = " + sq.inteiro(id_categoria)
        with OracleQueries() as db:
            return db.scalar(sql) > 0

    def existe_nome(self, nome, ignorar_id=None):
        sql = "select count(1) from categoria where upper(nome) = upper(" + sq.texto(nome) + ")"
        if ignorar_id is not None:
            sql += " and id_categoria <> " + sq.inteiro(ignorar_id)
        with OracleQueries() as db:
            return db.scalar(sql) > 0

    def contar_dependentes(self, id_categoria):
        sql = "select count(1) from tarefa where id_categoria = " + sq.inteiro(id_categoria)
        with OracleQueries() as db:
            return db.scalar(sql)

    # ---- operações ----
    def inserir(self, categoria):
        if self.existe_nome(categoria.get_nome()):
            raise ValueError("Já existe uma categoria com este nome.")
        with OracleQueries() as db:
            novo_id = db.scalar("select seq_categoria.nextval from dual")
            sql = ("insert into categoria (id_categoria, nome, descricao) values ("
                   + sq.inteiro(novo_id) + ", "
                   + sq.texto(categoria.get_nome()) + ", "
                   + sq.texto(categoria.get_descricao()) + ")")
            db.execute(sql)
        categoria.set_id_categoria(novo_id)
        return categoria

    def atualizar(self, categoria):
        if not self.existe_id(categoria.get_id_categoria()):
            raise ValueError("Categoria não encontrada.")
        if self.existe_nome(categoria.get_nome(), ignorar_id=categoria.get_id_categoria()):
            raise ValueError("Já existe outra categoria com este nome.")
        sql = ("update categoria set nome = " + sq.texto(categoria.get_nome())
               + ", descricao = " + sq.texto(categoria.get_descricao())
               + " where id_categoria = " + sq.inteiro(categoria.get_id_categoria()))
        with OracleQueries() as db:
            db.execute(sql)
        return categoria

    def excluir(self, id_categoria, excluir_dependentes=False):
        if not self.existe_id(id_categoria):
            raise ValueError("Categoria não encontrada.")
        if self.contar_dependentes(id_categoria) > 0 and not excluir_dependentes:
            raise ValueError("Esta categoria possui tarefas vinculadas e não pode ser removida.")
        with OracleQueries() as db:
            if excluir_dependentes:
                db.execute("delete from tarefa where id_categoria = " + sq.inteiro(id_categoria),
                           commit=False)
            db.execute("delete from categoria where id_categoria = " + sq.inteiro(id_categoria),
                       commit=False)
            db.commit()
