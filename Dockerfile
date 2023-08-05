
FROM python:3.10-slim

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080  # Exposing port 8080 for TCP traffic

CMD ["python", "app.py"]
