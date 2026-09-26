# Achados e Perdidos

Sistema web para cadastrar objetos perdidos e registrar devoluções, com interface em HTML, API Flask e persistência em PostgreSQL.

Projeto desenvolvido na disciplina **Desenvolvimento de Software Integrado (DevOps)** — Pós-Unifor, Turma 4 / Z251, semestre 2026.2, professor Arimatéia Júnior. O projeto reúne práticas de versionamento, testes, integração contínua, containers e publicação de imagens.

O sistema tem finalidade exclusivamente acadêmica, para exercícios, demonstrações e avaliação da disciplina. Não há previsão de uso em uma operação real.

## Objetivos de aprendizagem

- Praticar colaboração com Git, branches e pull requests.
- Integrar interface web, API e banco de dados em uma aplicação simples.
- Automatizar verificações de código e testes no pipeline.
- Empacotar e executar a aplicação com Docker e Docker Compose.
- Exercitar publicação e versionamento de imagens e verificação de saúde da aplicação.

## Equipe

| Integrante | Matrícula |
| --- | --- |
| Alan | 2651409 |
| Evaldo | 2651472 |
| Helder | 2651656 |
| Levi | 2650527 |
| Murilo | 2650305 |

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de objetos perdidos, com nome, cor e data.
- Validação de datas no formato `DD/MM/AAAA`, sem permitir datas futuras.
- Registro e gerenciamento de devoluções, com nome da pessoa, CPF e contato.
- Interface web para listar todos os registros ou consultar pelo ID.
- Endpoint `/health` para verificar a conexão com o banco.
- Página extra **Tribunal DevOps**, em `/jogo`, com uma dinâmica da equipe e placar persistido no banco.

Ao registrar uma devolução, a API consulta o objeto perdido pelo `id_objeto` e copia seu nome e cor. Essa operação não exclui o objeto perdido nem mantém uma chave estrangeira entre as duas tabelas.

## Tecnologias

| Camada | Tecnologias |
| --- | --- |
| Backend | Python 3.11, Flask e Flask-CORS |
| Banco de dados | PostgreSQL 16 e psycopg2 |
| Interface | HTML, CSS, JavaScript e Bootstrap |
| Configuração | Variáveis de ambiente e python-dotenv |
| Testes e qualidade | pytest, requests e flake8 |
| Containers | Docker e Docker Compose |
| CI/CD | GitHub Actions e Docker Hub |

Python 3.11 é a versão utilizada no Dockerfile e no workflow. As dependências estão em [requirements.txt](requirements.txt) e [requirements-dev.txt](requirements-dev.txt).

## Estrutura do projeto

```text
.
├── App.py                         # Aplicação, páginas e health check
├── Controller/
│   ├── RotasObjetoP.py             # CRUD de objetos perdidos
│   └── RotasObjetoA.py             # CRUD de devoluções
├── Model/Database.py              # Conexão, consultas e criação das tabelas
├── View/                          # HTML, estilos, scripts e imagens
├── tests/
│   ├── conftest.py                # Configuração e preparação dos testes
│   ├── test_ci.py                 # Verificações básicas
│   └── test_integration.py        # Testes HTTP com aplicação e banco ativos
├── .github/workflows/ci.yml       # Pipeline de CI/CD
├── .env.example                   # Exemplo de configuração local
├── .flake8                        # Configuração da análise estática
├── Dockerfile
├── docker-compose.yml            # Build local e PostgreSQL
├── docker-compose.prod.yml       # Execução da imagem publicada
├── requirements.txt
└── requirements-dev.txt
```

## Executar com Docker Compose

Pré-requisitos: Git, Docker e Docker Compose. No Windows, o Docker Desktop deve estar em execução no modo **Linux containers**.

Clone o repositório e entre na pasta que contém `App.py`:

```bash
git clone https://github.com/achados-e-perdidos-unifor/main.git
cd main
```

Construa a imagem e inicie a aplicação e o PostgreSQL:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f app
```

Acesse:

- Interface: [http://localhost:5000](http://localhost:5000).
- Saúde da aplicação: [http://localhost:5000/health](http://localhost:5000/health).
- Tribunal DevOps: [http://localhost:5000/jogo](http://localhost:5000/jogo).

O Compose aguarda o PostgreSQL ficar disponível antes de iniciar a aplicação. Na inicialização, a aplicação tenta criar automaticamente as tabelas `objetos_perdidos`, `objetos_achados` e `tribunal_devops`, caso ainda não existam. Não é necessário chamar as rotas de criação em uma instalação nova com o banco acessível.

O volume `db_data` mantém os dados entre execuções. Para parar os containers preservando esses dados:

```bash
docker compose down
```

Adicionar `-v` a esse comando remove também os volumes do Compose e apaga os dados armazenados neles.

### Executar a imagem publicada para demonstração e avaliação

O [docker-compose.prod.yml](docker-compose.prod.yml) permite demonstrar a entrega da aplicação usando a imagem `murilo751/achados-e-perdidos:latest`, sem construir o código local. Apesar do nome do arquivo, seu uso neste projeto é acadêmico:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

Use esse modo como alternativa ao Compose de desenvolvimento, sem executar ambos simultaneamente na porta 5000. Ele depende de uma imagem já publicada no Docker Hub e utiliza o mesmo nome de volume do banco quando executado no mesmo projeto Compose.

## Executar Python fora do Docker

Execute os comandos na pasta que contém `App.py`. É necessário ter Python 3.11 e um PostgreSQL acessível.

### 1. Criar o ambiente virtual

Linux/macOS, com Python 3.11 instalado:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
cp .env.example .env
```

Windows PowerShell, com Python 3.11 disponível no launcher:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
```

Com o ambiente ativado:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Configurar o banco

É possível iniciar apenas o PostgreSQL do Compose:

```bash
docker compose up -d db
```

Nesse caso, configure o `.env` assim:

```dotenv
DB_NAME=achados_perdidos
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
PORT=5000
```

Se usar outro PostgreSQL, crie previamente o banco e ajuste as credenciais. A aplicação cria as tabelas, mas não cria o banco de dados.

| Variável | Finalidade |
| --- | --- |
| `DB_NAME` | Nome do banco |
| `DB_USER` | Usuário do PostgreSQL |
| `DB_PASSWORD` | Senha do usuário |
| `DB_HOST` | `localhost` pelo host ou `db` entre containers do Compose |
| `DB_PORT` | Porta do PostgreSQL, normalmente `5432` |
| `PORT` | Porta HTTP do Flask, com padrão `5000` |

O `.env.example` usa `DB_HOST=db`; altere para `localhost` ao executar Python fora do container. O `.env` não deve ser versionado. Nos arquivos Compose, os valores estão definidos diretamente em `environment`; editar somente o `.env` não substitui esses valores.

### 3. Iniciar a aplicação

```bash
python App.py
```

Acesse [http://localhost:5000](http://localhost:5000). Para encerrar, pressione `Ctrl+C`.

## API

Requisições com corpo devem usar JSON e o cabeçalho `Content-Type: application/json`.

### Objetos perdidos

| Método | Rota | Função |
| --- | --- | --- |
| POST | `/inserir_objeto` | Cadastrar objeto |
| GET | `/listar_objetos` | Listar objetos |
| GET | `/listar_objeto/<id>` | Consultar pelo ID |
| PUT | `/atualizar_objeto` | Atualizar, com `id_objeto` no corpo |
| DELETE | `/deletar_objeto/<id>` | Excluir objeto |
| POST | `/criar_tabela_ObjetoP` | Criar tabela, caso ainda não exista |

Exemplo de cadastro:

```json
{
  "nome_objeto": "Mochila",
  "cor": "Preta",
  "data_perdido": "01/01/2026"
}
```

Na atualização, envie os mesmos campos e acrescente `id_objeto`. A data deve existir no calendário, seguir `DD/MM/AAAA` e ser igual ou anterior ao dia atual.

### Itens devolvidos

| Método | Rota | Função |
| --- | --- | --- |
| POST | `/inserir_objetoA` | Registrar devolução de um objeto perdido existente |
| GET | `/listar_objetosA` | Listar devoluções |
| GET | `/listar_objetoA/<id>` | Consultar devolução pelo ID |
| PUT | `/atualizar_objetoA` | Atualizar devolução |
| DELETE | `/deletar_objetoA/<id>` | Excluir devolução |
| POST | `/criar_tabela_ObjetoA` | Criar tabela, caso ainda não exista |

Exemplo de cadastro, substituindo `1` pelo ID de um objeto perdido existente:

```json
{
  "id_objeto": 1,
  "nome_pessoa": "Pessoa de Exemplo",
  "cpf": "000.000.000-00",
  "contato": "pessoa@example.com"
}
```

Para atualizar uma devolução, envie `id_objeto`, `nome_objeto`, `cor`, `nome_pessoa`, `cpf` e `contato`. Nesse endpoint, `id_objeto` representa o ID da **devolução** (`id_objetoA`), não o ID do objeto perdido original.

As consultas individuais dos dois módulos retornam o registro dentro da chave `Objeto-perdido`, conforme o contrato atual da API.

### Saúde e Tribunal DevOps

| Método | Rota | Função |
| --- | --- | --- |
| GET | `/health` | Retornar `200` com banco conectado ou `503` sem conexão |
| GET | `/jogo` | Abrir o Tribunal DevOps |
| POST | `/api/registrar_crime` | Registrar ocorrência da dinâmica, com `integrante` e `crime` |
| GET | `/api/placar_crimes` | Consultar placar por integrante |
| POST | `/api/zerar_crimes` | Apagar todos os registros do placar |

Exemplo de resposta saudável:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Testes e análise estática

No ambiente virtual, instale as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Execute a análise estática e as verificações básicas:

```bash
python -m flake8 . --count --show-source --statistics
python -m pytest tests/test_ci.py -v
```

`test_ci.py` contém verificações simples; elas não validam o funcionamento real da API ou a conexão com PostgreSQL.

### Testes de integração

Os testes em `test_integration.py` fazem requisições HTTP contra a aplicação ativa. **Use exclusivamente um banco de teste:** a fixture `clean_database` executa `TRUNCATE` nas tabelas de objetos perdidos e devoluções antes e depois dos testes que a utilizam.

Com um ambiente descartável e o `.env` apontando para seu banco de teste, inicie os serviços:

```bash
docker compose up -d --build
```

Confirme que `/health` responde com HTTP `200`. Depois, no ambiente virtual do host:

```bash
python -m pytest tests/test_integration.py -v --tb=short
```

A variável `APP_URL` altera o endereço da aplicação testada; o padrão é `http://localhost:5000`. As variáveis `DB_*` devem apontar para o mesmo banco usado por essa aplicação. Para o Compose local, o acesso pelo host utiliza `DB_HOST=localhost`.

Com aplicação e banco de teste disponíveis, execute toda a suíte:

```bash
python -m pytest tests/ -v --tb=short
```

## CI/CD

O workflow [ci.yml](.github/workflows/ci.yml) utiliza Ubuntu hospedado pelo GitHub e Python 3.11. É acionado por pushes em `main`, `develop` e `feature/*`, pull requests para `main` e `develop`, tags no padrão `v*.*.*` e execução manual.

As etapas dependem da conclusão bem-sucedida da anterior:

1. **Build:** instala dependências, verifica a importação da aplicação e gera um ZIP.
2. **Lint:** executa flake8 com a configuração do projeto.
3. **Test:** executa pytest, constrói a imagem Docker e prevê um smoke test de `/health` com Compose, seguido do armazenamento da imagem como artefato.
4. **Deploy:** publica a imagem no Docker Hub após push em `main` ou execução elegível em tag `v*`.

A publicação usa os secrets `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`. As imagens recebem tags com o SHA do commit e `latest`; em releases por tag, recebem também a versão correspondente. Neste trabalho, o job `deploy` demonstra a entrega por publicação da imagem, que pode ser executada para avaliação com `docker-compose.prod.yml`.

**Limitação atual:** o comando `pytest tests/` inclui os testes de integração, porém aparece antes de `docker compose up`. Em um ambiente limpo, esses testes dependem de aplicação e banco que ainda não foram iniciados. Essa ordem precisa ser ajustada no CI; a existência do workflow não significa que a suíte esteja passando.

## Escopo acadêmico

O foco é demonstrar o fluxo de desenvolvimento e entrega estudado na disciplina. Autenticação, controle de acesso e operação em produção estão fora do escopo. Use nomes, CPFs e contatos fictícios; as credenciais do Compose são destinadas às demonstrações.

Para reproduzir o trabalho, considere estas características:

- As telas de CRUD acessam `http://localhost:5000`; execute a demonstração nesse endereço. Outro computador, domínio ou porta exige ajustar as URLs da interface.
- A aplicação utiliza o servidor de desenvolvimento do Flask.
- A criação automática de tabelas não altera a estrutura de tabelas já existentes.
- Recursos visuais externos, como Bootstrap e ícones, podem depender de acesso à internet.

## Diagnóstico rápido

| Sintoma | O que verificar |
| --- | --- |
| `/health` retorna `503` | Conexão PostgreSQL, credenciais e `DB_HOST` |
| Host `db` não é encontrado fora do Docker | Usar `localhost` no `.env` do host |
| Porta 5000 ou 5432 ocupada | Outra aplicação ou instância de PostgreSQL/Compose em execução |
| Testes HTTP não conectam | Aplicação ativa, resposta de `/health` e valor de `APP_URL` |
| Página abre, mas formulários falham remotamente | URLs de API apontando para `localhost` no navegador |

Para acompanhar os serviços:

```bash
docker compose ps
docker compose logs app db
```

## Uso de IA

A disciplina exige registrar onde a IA foi utilizada e como o resultado foi validado. Esta documentação foi revisada com auxílio de IA a partir do código, dos testes e das configurações presentes no repositório. A revisão documental não equivale à execução bem-sucedida da aplicação ou do pipeline; os resultados de execução devem ser registrados nas evidências da equipe.
