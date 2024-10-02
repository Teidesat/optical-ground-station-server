FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt update \
    && apt install --yes \
        ffmpeg \
        libgtk2.0-dev \
        libgl1-mesa-glx \
        libsm6 \
        libxext6 \
        pkg-config \
    && apt clean

# Set the working directory
COPY . /app
WORKDIR /app

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --requirement /app/requirements.txt

# Run the flask application
CMD ["flask", "run"]
