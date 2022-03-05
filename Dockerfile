FROM python:3.9

WORKDIR /app
COPY . .
ENV PYTHONPATH "."

RUN python3.9 -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3.9"]
CMD ["web_service/src/main.py"]