import os

from conexion.oracle_queries import OracleQueries
from utils.interface import cabecalho, imprimir_tabela

PASTA_SQL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sql")


class Relatorios:

    def _ler_sql(self, nome_arquivo):
        caminho = os.path.join(PASTA_SQL, nome_arquivo)
        with open(caminho, encoding="utf-8") as arquivo:
            return arquivo.read().strip().rstrip(";")

    def _executar(self, nome_arquivo, titulo_relatorio):
        sql = self._ler_sql(nome_arquivo)
        with OracleQueries() as db:
            colunas, linhas = db.query(sql)
        cabecalho(titulo_relatorio)
        if not linhas:
            print("\nNenhum registro encontrado.")
            return
        print()
        imprimir_tabela(colunas, linhas)
        print("Total de linhas: {}".format(len(linhas)))

    def tarefas_por_usuario(self):
        self._executar("relatorio_tarefas_por_usuario.sql", "RESUMO DE TAREFAS POR USUÁRIO")

    def tarefas_por_categoria(self):
        self._executar("relatorio_tarefas_por_categoria.sql", "RESUMO DE TAREFAS POR CATEGORIA")

    def tarefas_detalhadas(self):
        self._executar("relatorio_tarefas_detalhadas.sql", "LISTAGEM DETALHADA DE TAREFAS")
