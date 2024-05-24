# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN apt-get update \
&& apt-get install -y --no-install-recommends --no-install-suggests \
&& pip3 install --no-cache-dir --upgrade pip

RUN pip3 install --default-timeout=200 future 
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the FastAPI app into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
