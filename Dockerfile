FROM python:3.12.3

RUN mkdir -p /metaDesignBot
WORKDIR /metaDesignBot

COPY . .
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="/root/.local/bin:$PATH"
RUN poetry install

CMD ["python3", "bot.py"]
