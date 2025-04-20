FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "conference.conference_service:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
