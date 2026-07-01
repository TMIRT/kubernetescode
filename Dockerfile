# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

RUN groupadd -r appgroup && useradd -r -g appgroup -m -s /sbin/nologin flaskuser

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R flaskuser:appgroup /app

USER flaskuser

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
