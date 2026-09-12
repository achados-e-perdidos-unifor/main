# Achados e Perdidos

Projeto desenvolvido pelo nosso grupo na disciplina **Desenvolvimento de Software Integrado
(DevOps)** — Pós-Unifor, Turma 4 / Z251, semestre 2026.2, professor Arimatéia Júnior.

A aplicação é um CRUD de objetos perdidos e achados. O foco da disciplina não está na aplicação em
si, e sim no que a cerca: Git, CI, containers, release e observabilidade. Por isso o mesmo projeto
evolui a cada encontro.

Escolhemos esse tema por ser pequeno, mas ainda assim realista: reúne API e banco de dados, roda
localmente e não depende de uma stack complexa que consumisse o tempo das aulas.

## Equipe

| Integrante | Matrícula |
| --- | --- |
| Alan | 2651409 |
| Evaldo | 2651472 |
| Helder | 2651656 |
| Levi | 2650527 |
| Murilo | 2650305 |

## O que o sistema faz

São duas telas principais:

- **Objetos perdidos** — cadastro do que foi perdido (nome, cor, data).
- **Itens devolvidos** — quando um objeto é devolvido, registra a pessoa responsável
  (nome, CPF, contato) associada ao objeto perdido correspondente.

Em ambos os casos é possível criar, listar (todos ou por ID), atualizar e excluir registros.

## Stack

- **Python + Flask** — API REST
- **PostgreSQL** (via `psycopg2`) — banco de dados
- **HTML + Bootstrap** — interface simples, servida como estático pelo próprio Flask
- **python-dotenv** — mantém as credenciais do banco fora do código

A organização segue o padrão MVC:

```
App.py            # sobe o Flask e registra as rotas
Controller/       # as rotas da API
Model/Database.py # conexão e execução de queries
View/             # as telas em HTML
```

## Como rodar

**1. Clonar o repositório e criar o ambiente virtual**

```bash
git clone <url-do-repo> && cd main && python3 -m venv venv && source venv/bin/activate
```

**2. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**3. Configurar o banco**

Copie o `.env.example` para `.env` e preencha com os dados do seu PostgreSQL:

```bash
cp .env.example .env
```

```
DB_NAME=achados_perdidos
DB_USER=postgres
DB_PASSWORD=suasenha
DB_HOST=localhost
DB_PORT=5432
```

> O `.env` está no `.gitignore` e não deve ser versionado.

**4. Subir a aplicação**

```bash
python App.py
```

A aplicação fica disponível em http://localhost:5000.

**5. Criar as tabelas (apenas na primeira execução)**

As tabelas não são criadas automaticamente. É necessário chamar as duas rotas:

```bash
curl -X POST http://localhost:5000/criar_tabela_ObjetoP
```

```bash
curl -X POST http://localhost:5000/criar_tabela_ObjetoA
```

## Endpoints

**Objetos perdidos**

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/criar_tabela_ObjetoP` | cria a tabela |
| POST | `/inserir_objeto` | cadastra um objeto perdido |
| GET | `/listar_objetos` | lista todos |
| GET | `/listar_objeto/<id>` | lista um registro específico |
| PUT | `/atualizar_objeto` | atualiza (o id vai no corpo da requisição) |
| DELETE | `/deletar_objeto/<id>` | exclui |

**Itens devolvidos**

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/criar_tabela_ObjetoA` | cria a tabela |
| POST | `/inserir_objetoA` | registra a devolução (usa o `id_objeto` do objeto perdido) |
| GET | `/listar_objetosA` | lista todos |
| GET | `/listar_objetoA/<id>` | lista um registro específico |
| PUT | `/atualizar_objetoA` | atualiza |
| DELETE | `/deletar_objetoA/<id>` | exclui |

## A parte DevOps

- [x] **E1** — Diagnóstico DevOps e proposta priorizada
- [x] **E2** — Repositório, PRs e tag inicial
- [ ] **E3** — Pipeline de CI com testes
- [ ] **E4** — Docker e docker-compose
- [ ] **E5** — Release, rollback e segurança básica
- [ ] **E6** — Observabilidade e defesa final

## Sobre uso de IA

A disciplina exige o registro de onde a IA foi utilizada e do que foi validado manualmente. À
medida que o projeto avançar, anotamos aqui o que foi solicitado, o que foi aceito, o que foi
descartado e qual teste ou revisão confirmou o funcionamento.
