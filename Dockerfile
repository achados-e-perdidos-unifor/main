# ==========================================
# Dockerfile da Aplicação Flask (Achados e Perdidos)
# Padrão técnico obrigatório - Turma DevOps Unifor
# ==========================================

# 1. Imagem base oficial, fixada e leve (versão slim)
FROM python:3.11-slim

# Metadados OCI exibidos por registries como o Docker Hub
LABEL org.opencontainers.image.title="Achados e Perdidos" \
      org.opencontainers.image.description="Aplicação Flask para cadastro de objetos perdidos e devolvidos."

# 2. Variáveis de ambiente para o Python em containers
# PYTHONDONTWRITEBYTECODE: impede a criação de arquivos .pyc no container
# PYTHONUNBUFFERED: envia prints/logs direto para o terminal em tempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# 3. Diretório de trabalho dentro do container
WORKDIR /app

# 4. Criação de usuário não-privilegiado (REGRA: "Nunca rodar como root")
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# 5. Cache de camadas: copia SÓ as dependências e instala primeiro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o restante do código já atribuindo a posse ao usuário não-root
COPY --chown=appuser:appgroup . .

# 7. Ativa o usuário não-root
USER appuser

# 8. Exposição da porta da aplicação
EXPOSE 5000

# 9. Healthcheck nativo consultando o endpoint /health criado na Etapa 1
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# 10. Comando principal para iniciar a aplicação
CMD ["python", "App.py"]
