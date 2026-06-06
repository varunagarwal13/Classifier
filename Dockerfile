FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY main.py .
COPY database.py .
COPY model_rf_v2.pkl .
COPY model_xgb_v2.pkl .
COPY feature_cols_v2.pkl .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]