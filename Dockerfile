FROM python:3.9

RUN apt-get update -y && apt-get install -y \
    gcc \
    make \
    dos2unix

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN make

RUN dos2unix src/launcher.sh && chmod +x /app/launcher.sh

CMD ["./src/launcher.sh"]