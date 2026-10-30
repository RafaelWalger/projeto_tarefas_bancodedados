# Sistema de Gerenciamento de Tarefas

Aplicação de console em **Python + Oracle** para gerenciar usuários, categorias e
tarefas, com relatórios, inserção, remoção e atualização de registros.

- **Disciplina:** Banco de Dados — **Professor:** Howard Roatti
- **Grupo:** *Bernardo Pinotti Calenzani Simões, Rafael Walger Tovar, Kaua de Freitas*

## O que o sistema faz

| Menu | Funcionalidade |
|------|----------------|
| **Relatórios** | Resumo por usuário e por categoria (`GROUP BY`) e listagem detalhada de tarefas (`JOIN` de 3 tabelas). |
| **Inserir** | Cadastra usuários, categorias e tarefas, perguntando se deseja inserir mais. |
| **Remover** | Lista, confirma e trata chave estrangeira (avisa e oferece remover as tarefas vinculadas). |
| **Atualizar** | Lista, permite alterar os campos (ENTER mantém o valor atual) e mostra o registro atualizado. |
| **Sair** | Encerra o programa. |

## Nota sobre o histórico de commits (esclarecimento)

Este é o nosso primeiro projeto no Github, estávamos perdidos quanto a funcionalidade do git.
No primeiro envio, o projeto completo foi enviado por um único integrante por falta de experiência 
(pensávamos que o projeto deveria ser enviado apenas na conclusão de todo o projeto), 
o que não refletia quem desenvolveu cada parte. Para corrigir isso, cada integrante enviou, 
com a própria conta, a parte que desenvolveu. Por isso todos os commits têm a mesma data.

## Modelo de dados

Diagrama relacional: [`diagrams/diagrama_relacional.mmd`](diagrams/diagrama_relacional.mmd)
(Mermaid) e a imagem exportada `ImagemDiagramaRelacional.pdf`, também em `diagrams/`.

- **USUARIO** (`id_usuario` PK, nome, email único, cargo)
- **CATEGORIA** (`id_categoria` PK, nome, descricao)
- **TAREFA** (`id_tarefa` PK, titulo, descricao, status, prioridade, data_criacao,
  data_conclusao, horas_gastas, `id_usuario` FK, `id_categoria` FK)

Relacionamentos: um usuário tem várias tarefas (1:N); uma categoria tem várias tarefas (1:N).

## Bibliotecas utilizadas

As dependências estão listadas em `requirements.txt` e são instaladas com:

```bash
pip install -r requirements.txt
```

## Como executar no Linux

### 1. Subir os bancos de dados (caso na VM da disciplina)

```bash
cd ~/database_services
docker compose up -d
```

### 2. Acessar a pasta do projeto

Coloque a pasta do projeto no Desktop e entre nela:

```bash
cd ~/Desktop/projeto_tarefas
```

### 3. Criar e ativar o ambiente virtual Python

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar as credenciais do Oracle

Abra o arquivo `.env`:

```bash
nano .env
```

Preencha com os dados da conexão (sem espaços):

```
ORACLE_USER=system
ORACLE_PASSWORD=oracle
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
```

Salve com `Ctrl + O`, pressione `Enter` e saia com `Ctrl + X`.

### 6. Criar as tabelas do banco de dados

Certifique-se de que o contêiner do Oracle esteja em execução. Depois:

1. Abra o DBeaver e pressione `Shift + Ctrl + N`.
2. Selecione o banco de dados Oracle.
3. Altere as opções: **Password** = `oracle` e **Database** = `XEPDB1`.
4. Clique em **Finish**.
5. No projeto, abra o arquivo `database/criar_tabelas.sql` e copie todo o texto.
6. Clique uma vez no banco de dados `XEPDB1` e pressione `F3`.
7. Cole o script e pressione `Alt + X`.

### 7. Executar o sistema

Pelo terminal, dentro da pasta do projeto e com o ambiente virtual ativado:

```bash
python3 src/principal.py
```

## Observações

- Ajuste as credenciais do `.env` conforme o seu ambiente.
