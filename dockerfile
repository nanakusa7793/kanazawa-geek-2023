FROM python:3.11

RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0

RUN pip install --upgrade pip


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .