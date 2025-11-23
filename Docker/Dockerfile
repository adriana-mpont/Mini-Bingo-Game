#sets the base image
FROM python:3.11-slim

#first we are making the program to run in a smoother way (it avoids that things are displayed with delay)
#then we make sure that we do not keep downloaded packages in the container as it uses a lot of space and provides no benefit to having it in the container. 
ENV PYTHONUNBUFFERED=1 \
    PIP--NO_CACHE_DIR=1

# Install Tkinter (GUI) system dependencies
RUN apt-get update && \
    apt-get install -y python3-tk tk && \
    rm -rf /var/lib/apt/lists/*

#set the working directory inside the container 
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

