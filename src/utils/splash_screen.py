from conexion.oracle_queries import OracleQueries
from utils import config


class SplashScreen:
    LARGURA = 54

    def __init__(self):
        self.nome_sistema = config.NOME_SISTEMA
        self.integrantes = config.INTEGRANTES
        self.disciplina = config.DISCIPLINA
        self.semestre = config.SEMESTRE
        self.professor = config.PROFESSOR

    def get_total_registros(self):
        totais = []
        with OracleQueries() as db:
            for rotulo, tabela in config.ENTIDADES_SPLASH:
                sql = "select count(1) total_" + tabela + " from " + tabela
                totais.append((rotulo, db.scalar(sql)))
        return totais

    def _linha(self, texto=""):
        return "# " + texto.ljust(self.LARGURA - 4) + " #"

    def get_updated_screen(self):
        borda = "#" * self.LARGURA
        linhas = [
            borda,
            "# " + self.nome_sistema.center(self.LARGURA - 4) + " #",
            self._linha(),
            self._linha("TOTAL DE REGISTROS EXISTENTES"),
        ]
        for indice, (rotulo, total) in enumerate(self.get_total_registros(), 1):
            linhas.append(self._linha("   {} - {:<12}{:>8}".format(indice, rotulo + ":", total)))
        linhas.append(self._linha())
        for indice, nome in enumerate(self.integrantes):
            prefixo = "CRIADO POR: " if indice == 0 else " " * 12
            linhas.append(self._linha(prefixo + nome))
        linhas.append(self._linha())
        linhas.append(self._linha("DISCIPLINA: " + self.disciplina))
        linhas.append(self._linha(" " * 12 + self.semestre))
        linhas.append(self._linha("PROFESSOR: " + self.professor))
        linhas.append(borda)
        return "\n".join(linhas)
