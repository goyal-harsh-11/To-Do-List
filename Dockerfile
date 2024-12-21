FROM python:3.12.2

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 8080

CMD ["python","app.py"]