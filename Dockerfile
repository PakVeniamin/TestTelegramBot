FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3","main.py"]