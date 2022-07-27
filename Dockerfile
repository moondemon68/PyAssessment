FROM python:3.10

WORKDIR /app
COPY . .
ENV PYTHONPATH "."

RUN python3.10 -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3.10"]
CMD ["web_service/src/main.py"]

# ENTRYPOINT ["sh", "entrypoint.sh"]