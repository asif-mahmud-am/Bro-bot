FROM python:3.10.0-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install -r requirements.txt 
RUN pip install tiktoken 
COPY .env ./.env
COPY main.py ./main.py
COPY Dockerfile ./Dockerfile
COPY nginx.conf ./nginx.conf
COPY faiss_openai ./faiss_openai
# EXPOSE 8084 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]