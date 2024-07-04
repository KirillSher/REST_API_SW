FROM python:3.12

WORKDIR /app

COPY app/requirements.txt /app

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app .

EXPOSE 5000

CMD [ "python", "run.py", "--host=127.0.0.1", "--port=5000", "--debug=True"]