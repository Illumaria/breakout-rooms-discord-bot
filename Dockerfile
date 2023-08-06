FROM python:3.10-slim

EXPOSE 8080

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./app.py ./app.py

CMD ["python", "app.py"]
