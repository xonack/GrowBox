FROM python:3.8-buster

RUN pip install "poetry==1.1.4"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

RUN poetry install

COPY main.py ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]
