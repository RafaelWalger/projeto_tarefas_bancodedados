from conexion.oracle_queries import OracleQueries
from controller.controller_categoria import ControllerCategoria
from controller.controller_usuario import ControllerUsuario
from model.categoria import Categoria
from model.tarefa import Tarefa
from model.usuario import Usuario
from utils import sql_utils as sq

_SELECT_TAREFA = (
    "select t.id_tarefa, t.titulo, t.descricao, t.status, t.prioridade, "
    "t.data_criacao, t.data_conclusao, t.horas_gastas, "
    "u.id_usuario, u.nome, u.email, u.cargo, "
    "c.id_categoria, c.nome, c.descricao "
    "from tarefa t "
    "join usuario u on u.id_usuario = t.id_usuario "
    "join categoria c on c.id_categoria = t.id_categoria "
)


class ControllerTarefa:

    def _montar(self, l):
        
        usuario = Usuario(l[8], l[9], l[10], l[11])
        categoria = Categoria(l[12], l[13], l[14])
        return Tarefa(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], usuario, categoria)

    def listar(self):
        with OracleQueries() as db:
            _, linhas = db.query(_SELECT_TAREFA + "order by t.id_tarefa")
        return [self._montar(l) for l in linhas]

    def buscar(self, id_tarefa):
        """Devolve a Tarefa ou None se não existir."""
        sql = _SELECT_TAREFA + "where t.id_tarefa = " + sq.inteiro(id_tarefa)
        with OracleQueries() as db:
            _, linhas = db.query(sql)
        return self._montar(linhas[0]) if linhas else None

    # ---- verificações de existência ----
    def existe_id(self, id_tarefa):
        sql = "select count(1) from tarefa where id_tarefa = " + sq.inteiro(id_tarefa)
        with OracleQueries() as db:
            return db.scalar(sql) > 0

    def contar_dependentes(self, id_tarefa):
        return 0

    def _validar_chaves_estrangeiras(self, tarefa):
        if not ControllerUsuario().existe_id(tarefa.get_usuario().get_id_usuario()):
            raise ValueError("O usuário informado não existe.")
        if not ControllerCategoria().existe_id(tarefa.get_categoria().get_id_categoria()):
            raise ValueError("A categoria informada não existe.")

    # ---- operações ----
    def inserir(self, tarefa):
        self._validar_chaves_estrangeiras(tarefa)
        with OracleQueries() as db:
            novo_id = db.scalar("select seq_tarefa.nextval from dual")
            sql = ("insert into tarefa (id_tarefa, titulo, descricao, status, prioridade, "
                   "data_criacao, data_conclusao, horas_gastas, id_usuario, id_categoria) values ("
                   + sq.inteiro(novo_id) + ", "
                   + sq.texto(tarefa.get_titulo()) + ", "
                   + sq.texto(tarefa.get_descricao()) + ", "
                   + sq.texto(tarefa.get_status()) + ", "
                   + sq.texto(tarefa.get_prioridade()) + ", "
                   + sq.data(tarefa.get_data_criacao()) + ", "
                   + sq.data(tarefa.get_data_conclusao()) + ", "
                   + sq.decimal(tarefa.get_horas_gastas()) + ", "
                   + sq.inteiro(tarefa.get_usuario().get_id_usuario()) + ", "
                   + sq.inteiro(tarefa.get_categoria().get_id_categoria()) + ")")
            db.execute(sql)
        tarefa.set_id_tarefa(novo_id)
        return tarefa

    def atualizar(self, tarefa):
        if not self.existe_id(tarefa.get_id_tarefa()):
            raise ValueError("Tarefa não encontrada.")
        self._validar_chaves_estrangeiras(tarefa)
        sql = ("update tarefa set titulo = " + sq.texto(tarefa.get_titulo())
               + ", descricao = " + sq.texto(tarefa.get_descricao())
               + ", status = " + sq.texto(tarefa.get_status())
               + ", prioridade = " + sq.texto(tarefa.get_prioridade())
               + ", data_criacao = " + sq.data(tarefa.get_data_criacao())
               + ", data_conclusao = " + sq.data(tarefa.get_data_conclusao())
               + ", horas_gastas = " + sq.decimal(tarefa.get_horas_gastas())
               + ", id_usuario = " + sq.inteiro(tarefa.get_usuario().get_id_usuario())
               + ", id_categoria = " + sq.inteiro(tarefa.get_categoria().get_id_categoria())
               + " where id_tarefa = " + sq.inteiro(tarefa.get_id_tarefa()))
        with OracleQueries() as db:
            db.execute(sql)
        return tarefa

    def excluir(self, id_tarefa, excluir_dependentes=False):
        if not self.existe_id(id_tarefa):
            raise ValueError("Tarefa não encontrada.")
        with OracleQueries() as db:
            db.execute("delete from tarefa where id_tarefa = " + sq.inteiro(id_tarefa))
