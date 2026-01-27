FROM python:3.9

RUN apt-get update -y && apt-get install -y \
    gcc \
    make 

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN make

CMD ./src/benchmark disk && ./src/benchmark cache && python3 src/plots.py