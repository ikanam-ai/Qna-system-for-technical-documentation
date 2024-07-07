FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install httpx fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload"]
