# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the source and misc directories into the container
COPY scripts /app/scripts
COPY misc /app/misc

# Install required Python packages (adjust if needed)
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Set the default entrypoint
ENTRYPOINT ["python3"]
