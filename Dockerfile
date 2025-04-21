# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Julia dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libxrender1 \
    libsm6 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Julia
ENV JULIA_VERSION=1.10.2
RUN wget https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-$JULIA_VERSION-linux-x86_64.tar.gz && \
    tar -xvzf julia-$JULIA_VERSION-linux-x86_64.tar.gz && \
    mv julia-$JULIA_VERSION /opt/ && \
    ln -s /opt/julia-$JULIA_VERSION/bin/julia /usr/local/bin/julia && \
    rm julia-$JULIA_VERSION-linux-x86_64.tar.gz

# Install Python dependency
RUN pip install requests

# Copy your Python source files
COPY programRunner.py . 
COPY stockAPIGetter.py . 
COPY topStockDisplayer.py . 
COPY stockCSVDownloader.py . 

# Copy your CSV
COPY stock-tickers.csv /app/stock-tickers.csv

# Copy the Julia optimizer script from the 'julia' folder
COPY julia/stock_optimizer.jl /app/stock_optimizer.jl

# Optional: compile Python bytecode
RUN python -m compileall .

# Default to running your Python entrypoint
CMD ["python", "programRunner.py"]
