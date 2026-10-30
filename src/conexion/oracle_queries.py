
import os

import oracledb

_cliente_thick_iniciado = False


def _carregar_env():
    
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    caminho = os.path.join(raiz, ".env")
    if not os.path.isfile(caminho):
        return
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


class OracleQueries:
    

    def __init__(self):
        _carregar_env()
        self.usuario = os.getenv("ORACLE_USER", "")
        self.senha = os.getenv("ORACLE_PASSWORD", "")
        self.conn = None
        self.cursor = None

    def _dsn(self):
        dsn = os.getenv("ORACLE_DSN")
        if dsn:
            return dsn
        host = os.getenv("ORACLE_HOST", "localhost")
        porta = int(os.getenv("ORACLE_PORT", "1521"))
        sid = os.getenv("ORACLE_SID")
        if sid:
            return oracledb.makedsn(host, porta, sid=sid)
        return oracledb.makedsn(host, porta, service_name=os.getenv("ORACLE_SERVICE", "XEPDB1"))

    def connect(self):
        global _cliente_thick_iniciado
        if not self.usuario or not self.senha:
            raise RuntimeError(
                "Credenciais não configuradas. Crie o arquivo .env (copie o .env.example) "
                "com ORACLE_USER e ORACLE_PASSWORD."
            )
        # Modo 'thick' só é necessário para bancos Oracle antigos (11g). Veja o README.
        if os.getenv("ORACLE_THICK") == "1" and not _cliente_thick_iniciado:
            oracledb.init_oracle_client()
            _cliente_thick_iniciado = True
        self.conn = oracledb.connect(user=self.usuario, password=self.senha, dsn=self._dsn())
        self.cursor = self.conn.cursor()
        return self

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
        self.cursor = None
        self.conn = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, tipo_erro, erro, traceback):
        if tipo_erro is not None and self.conn is not None:
            try:
                self.conn.rollback()
            except Exception:
                pass
        self.close()
        return False

    def query(self, sql):
        
        self.cursor.execute(sql)
        colunas = [coluna[0] for coluna in self.cursor.description]
        return colunas, self.cursor.fetchall()

    def scalar(self, sql):
        
        self.cursor.execute(sql)
        linha = self.cursor.fetchone()
        return linha[0] if linha else None

    def execute(self, sql, commit=True):
        
        self.cursor.execute(sql)
        if commit:
            self.conn.commit()
        return self.cursor.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
