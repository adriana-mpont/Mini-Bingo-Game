FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP--NO_CACHE_DIR=1

WORKDIR /mini_bingo_app

#copy the dependency list to the container in mini_bingo_app/requirements.txt
COPY requirements.txt .

#we install the libraries but keep the image smaller by not storing downloaded images. 
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the application source code into the image
COPY src/ ./src/

# Create a directory for history files (can be backed by a volume)
RUN mkdir -p /app/data

# Sets an environment variable and exposes it to the python code 
ENV HISTORY_DIR=/app/data


CMD ["python", "src/main.py"]

