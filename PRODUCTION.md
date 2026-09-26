# Guia de Produção - Achados & Perdidos

Este documento explica como rodar a aplicação em **produção** usando a imagem publicada no Docker Hub.

## Pré-requisitos

- Docker e Docker Compose instalados
- Acesso ao Docker Hub (credenciais opcionais, imagem é pública)
- Arquivo `.env.prod` com variáveis de ambiente

## 1. Preparar variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.prod.example .env.prod
```

Edite `.env.prod` com seus valores reais:

```env
DOCKER_USERNAME=seu-usuario        # Seu username no Docker Hub
IMAGE_TAG=latest                   # Tag da imagem (latest ou versão específica)
APP_PORT=5000                      # Porta da aplicação no host
DB_NAME=achados_perdidos           # Nome do banco de dados
DB_USER=postgres                   # Usuário do PostgreSQL
DB_PASSWORD=sua-senha-super-segura # MUDAR EM PRODUÇÃO!
```

## 2. Iniciar a aplicação

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

Ou sem arquivo .env (usa padrões):

```bash
docker compose -f docker-compose.prod.yml up -d
```

## 3. Verificar status

```bash
# Ver containers rodando
docker ps

# Ver logs da aplicação
docker compose -f docker-compose.prod.yml logs -f app

# Verificar health
curl http://localhost:5000/health
```

## 4. Parar a aplicação

```bash
# Parar containers (mantém dados)
docker compose -f docker-compose.prod.yml down

# Parar e remover tudo (incluindo banco!)
docker compose -f docker-compose.prod.yml down -v
```

## Boas práticas em Produção

### 🔐 Segurança

- ✅ **Não commite `.env.prod`** — está em `.gitignore`
- ✅ **Mude a senha do PostgreSQL** — valor default (`postgres`) é inseguro
- ✅ **Use imagem com versão específica** — `latest` pode mudar
  ```bash
  docker compose -f docker-compose.prod.yml -e IMAGE_TAG=1.0.0 up -d
  ```

### 📊 Monitoramento

- ✅ **Health checks habilitados** — containers reiniciam se falharem
- ✅ **Logging configurado** — max 10MB por arquivo, 3 arquivos rotacionados
- ✅ **Restart policy** — `unless-stopped` = reinicia automaticamente se cair

```bash
# Ver logs formatados
docker compose -f docker-compose.prod.yml logs --follow --timestamps app

# Ver apenas erros
docker compose -f docker-compose.prod.yml logs app | grep -i error
```

### 🔄 Atualizações

Para atualizar para nova versão:

```bash
# 1. Parar containers
docker compose -f docker-compose.prod.yml down

# 2. Atualizar variável (ou editar .env.prod)
export IMAGE_TAG=1.1.0

# 3. Subir novamente
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d

# 4. Verificar
docker compose -f docker-compose.prod.yml logs app
```

### 💾 Backup do Banco

O volume `db_data` contém todos os dados do PostgreSQL. Para fazer backup:

```bash
# Fazer backup
docker exec achados-db pg_dump -U postgres achados_perdidos > backup.sql

# Restaurar
docker exec -i achados-db psql -U postgres achados_perdidos < backup.sql
```

## Troubleshooting

### Porta já está em uso

```bash
# Mudar porta no .env.prod
APP_PORT=8080
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

### Banco não conecta

```bash
# Ver logs do banco
docker compose -f docker-compose.prod.yml logs db

# Resetar (aviso: deleta dados!)
docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up -d
```

### Health check falhando

```bash
# Verificar manualmente
curl -v http://localhost:5000/health

# Ver logs da app
docker compose -f docker-compose.prod.yml logs app
```

## Variáveis de Ambiente Disponíveis

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DOCKER_USERNAME` | `murilo751` | Username no Docker Hub |
| `IMAGE_TAG` | `latest` | Tag da imagem |
| `APP_PORT` | `5000` | Porta da aplicação no host |
| `DB_NAME` | `achados_perdidos` | Nome do banco de dados |
| `DB_USER` | `postgres` | Usuário PostgreSQL |
| `DB_PASSWORD` | `postgres` | Senha PostgreSQL |

## Contato

Para questões sobre produção, consulte a documentação do [Encontro 5 - Entrega e Operação](./README.md).
