FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Atualiza pacotes (reduz vulnerabilidades)
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Instala dependências primeiro (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY . .

# Usuário não-root (segurança)
RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]