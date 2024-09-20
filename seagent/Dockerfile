# Use the official Python image from the Docker Hub
# FROM python:3.10.12-slim
FROM python:3.10.12

# Set environment variables to prevent Python from writing .pyc files
# and to ensure the stdout and stderr streams are unbuffered
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /opt/bihua/reqgpt/seagent

# Copy the requirements.txt file into the container
COPY requirements.txt .

COPY .streamlit .streamlit

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "./oms_main_with_auth.py"]
