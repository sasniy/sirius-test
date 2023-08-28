FROM python

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install -U python-dotenv
COPY . .

CMD ["python","main.py"]