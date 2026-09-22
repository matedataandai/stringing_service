FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir  boto3>=1.43.99 dotenv>=0.9.9 requests>=2.34.2 streamlit>=1.64.0

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]