FROM python:3.6

RUN touch /etc/app-env

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gfortran \
    git \
    liblapack-dev \
    libopenblas-dev \
    wget

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["script/server"]
