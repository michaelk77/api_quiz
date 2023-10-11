FROM python:3.11
WORKDIR /backend
COPY requirements.txt /backend
RUN pip install --no-cache-dir -r requirements.txt
COPY . /backend
EXPOSE 5000