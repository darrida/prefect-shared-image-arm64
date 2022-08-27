FROM --platform=linux/arm64 prefecthq/prefect:2.1.1-python3.10

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip
RUN pip install poetry
RUN pip install wheel
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
WORKDIR /src