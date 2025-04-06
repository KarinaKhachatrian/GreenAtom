FROM python:3.9-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=flydb
ENV POSTGRES_HOST=db

EXPOSE 8501

CMD ["python", "main.py"]