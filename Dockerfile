FROM frolvlad/alpine-python3:latest

RUN mkdir -p /data/out/tables /data/in/tables /data/out/files /data/in/files
RUN pip3 install --no-cache-dir --ignore-installed \
  pytest \
  requests \
  && pip3 install --upgrade --no-cache-dir --ignore-installed https://github.com/keboola/python-docker-application/archive/2.0.0.zip

COPY . /src/

CMD python3 -u /src/main.py
