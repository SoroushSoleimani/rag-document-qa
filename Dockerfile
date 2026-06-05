# Use the official Python lightweight image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files 
# and to ensure console output is not buffered
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# Copy the requirements file and install dependencies using a reliable mirror
# Copy the requirements file and install dependencies using Tsinghua mirror
COPY requirements.txt /app/
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# Copy the entire project source code into the container
COPY . /app/