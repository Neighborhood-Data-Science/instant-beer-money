FROM ibmfunctions/action-python-v3.11:1.0.0

RUN apt-get update

RUN apt-get install -y wget

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

RUN mkdir /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app