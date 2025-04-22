# Use a more secure base image
FROM python:3.13-slim

# Prevent interactive prompts and reduce output
ENV DEBIAN_FRONTEND=noninteractive
ENV JULIA_VERSION=1.10.2

# Set working directory
WORKDIR /app

# Update & install quietly with fewer layers
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
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
RUN wget -q https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-$JULIA_VERSION-linux-x86_64.tar.gz && \
    tar -xzf julia-$JULIA_VERSION-linux-x86_64.tar.gz && \
    mv julia-$JULIA_VERSION /opt/ && \
    ln -s /opt/julia-$JULIA_VERSION/bin/julia /usr/local/bin/julia && \
    rm julia-$JULIA_VERSION-linux-x86_64.tar.gz

# Install Python dependencies quietly
RUN pip install --no-cache-dir --quiet requests

# Copy source files
COPY programRunner.py . 
COPY stockAPIGetter.py . 
COPY topStockDisplayer.py . 
COPY stockCSVDownloader.py . 
COPY stock-tickers.csv /app/stock-tickers.csv
COPY stock_optimizer.jl /app/stock_optimizer.jl

# Optional: compile Python bytecode (quietly)
RUN python -m compileall -q .

# Default entrypoint
CMD ["python", "programRunner.py"]
