# USE python 3 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy your Java source files into the container
COPY programRunner.py .
COPY stockAPIGetter.py .
COPY topStockDisplayer.py .
COPY stockCSVDownloader.py .

# Copy the CSV file into the container
COPY stock-tickers.csv /app/stock-tickers.csv

# Create a directory for dependencies
RUN mkdir -p lib

# Install dependencies (optional: requests is used)
RUN pip install requests

# Compile the Python files to bytecode (.pyc)
RUN python -m compileall .

# Run the program
CMD ["python", "programRunner.py"]