FROM python:3.11.3

WORKDIR /opt/app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY cash_machine /cash_machine

CMD ["python", "bot.py"]