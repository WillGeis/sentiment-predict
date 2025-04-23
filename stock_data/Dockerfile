# Use a more secure base image
FROM python:3.13-slim

# Prevent interactive prompts and reduce output
ENV DEBIAN_FRONTEND=noninteractive
ENV JULIA_VERSION=1.10.2

# Set working directory
WORKDIR /app

# Install Python dependencies quietly
RUN pip install --no-cache-dir --quiet requests

# Copy source files
COPY programRunner.py . 
COPY stockAPIGetter.py . 
COPY topStockDisplayer.py . 
COPY stockCSVDownloader.py . 
COPY stock-tickers.csv /app/stock-tickers.csv

# Optional: compile Python bytecode (quietly)
RUN python -m compileall -q .

# Default entrypoint (ensure it's the Python entry point for your app)
CMD ["python", "programRunner.py"]
