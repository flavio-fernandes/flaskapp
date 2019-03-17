FROM python:alpine 

LABEL maintainer="Flavio Fernandes"

RUN pip install flask

COPY src /src/

WORKDIR /src
ENV RELEASE=0.0.0
ENV FLASK_DEBUG=1
ENV FLASK_APP=app.py
ENV TARGET=

ENTRYPOINT ["python", "/src/app.py"]
