# NOTE: This doesn't work yet -- last ran into an issue building wheel for "cffi"
# ```  
# c/_cffi_backend.c:15:10: fatal error: ffi.h: No such file or directory
#    15 | #include <ffi.h>
#       |          ^~~~~~~
# compilation terminated.
# error: command '/usr/bin/gcc' failed with exit code 1
# ```

####################################################################
# BUILD PACKAGE WHEELS
FROM --platform=linux/arm64 arm64v8/python:3.10-alpine as build
RUN apk add build-base libffi-dev

WORKDIR /wheels
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 wheel -r requirements.txt

####################################################################
# INSTALL DEPENDENCIES
FROM --platform=linux/arm64 arm64v8/python:3.10-alpine as final
COPY --from=build /wheels /wheels

RUN pip3 install --upgrade pip
RUN pip3 install wheel
COPY requirements.txt .
RUN pip3 install -r requirements.txt -f /wheels && \
    rm -rf wheels && \
    rm -rf /root/.cache/pip/*
WORKDIR /src
