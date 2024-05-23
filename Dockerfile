# Use the official Python base image
FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    && pip install --no-cache-dir --upgrade pip

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple

# Copy the FastAPI app into the container
COPY . /app

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
