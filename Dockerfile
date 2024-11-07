FROM python:3.12.3

RUN mkdir -p /metaDesignBot
WORKDIR /metaDesignBot

COPY . .

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN export PATH="/root/.local/bin:$PATH" \
    && poetry config virtualenvs.create false \
    && poetry install

CMD ["python3", "bot.py"]
