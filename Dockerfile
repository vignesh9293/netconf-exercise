FROM python:3.8-slim

# Set the working directory
WORKDIR /usr/src/app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the application 
EXPOSE 5000

COPY app.py .
COPY resources ./resources
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

# Run app.py
CMD ["python3", "app.py"]

