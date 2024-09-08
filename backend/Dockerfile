FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN pip install numpy --force

COPY . .

CMD ["uvicorn", "src.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8002"]
