FROM python:3.10-slim

EXPOSE 8080  # Exposing port 8080 for TCP traffic

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./app.py ./app.py

CMD ["python", "app.py"]
