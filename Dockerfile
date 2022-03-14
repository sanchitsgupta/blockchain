FROM python:3.10-slim-buster

WORKDIR /app

# Install dependencies.
RUN apt-get update && apt-get -y install gcc

COPY requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt

# Add actual source code.
COPY src ./src

CMD ["uvicorn", "src.node_server:app", "--port", "8000", "--host", "0.0.0.0"]
