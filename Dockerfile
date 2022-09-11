FROM python:3.8.14-alpine

LABEL org.opencontainers.image.authors="sven.steinheisser@gmail.com"

RUN adduser -D app
USER app
WORKDIR /home/app

COPY --chown=app:app ./requirements.txt requirements.txt

RUN pip install --user --no-cache-dir -r requirements.txt
ENV PATH="/home/app/.local/bin:${PATH}"

COPY ./shortener /home/app/shortener

EXPOSE 8000

CMD ["uvicorn", "shortener.app:app", "--host", "0.0.0.0", "--port", "8000"]
