FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y gdal-bin libgdal-dev libproj-dev build-essential python3-dev && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt


# Copy project files
COPY . .

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal

ENV C_INCLUDE_PATH=/usr/include/gdal

ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so


# Run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]