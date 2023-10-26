FROM python:3.10-slim

WORKDIR /app

COPY ./app .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD ["/bin/bash", "./run.sh"]


