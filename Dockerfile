####################################################################
# BUILD PACKAGE WHEELS
FROM --platform=linux/arm64 arm64v8/python:3.11-buster as build
RUN   apt-get update && apt-get upgrade -y --no-install-recommends

WORKDIR /wheels
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 wheel -r requirements.txt

####################################################################
# INSTALL DEPENDENCIES
FROM --platform=linux/arm64 arm64v8/python:3.11-slim-buster as application
RUN   apt-get update && apt-get upgrade -y --no-install-recommends
COPY --from=build /wheels /wheels

RUN pip3 install --upgrade pip
RUN pip3 install wheel
COPY requirements.txt .
RUN pip3 install -r requirements.txt -f /wheels && \
    rm -rf wheels && \
    rm -rf /root/.cache/pip/*
WORKDIR /src
