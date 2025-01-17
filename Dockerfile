# Use OpenJDK 17 slim as the base image
FROM python:3.11-slim

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install OpenJDK 17 and other dependencies
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    wget \
    git \
    maven \
    && rm -rf /var/lib/apt/lists/*

# Clone and build Timefold from source
WORKDIR /tmp
RUN git clone https://github.com/TimefoldAI/timefold-solver.git && \
    cd timefold-solver && \
    mvn clean install -Dquickly

# Install Python packages
RUN pip install --no-cache-dir \
    requests \
    pytz \
    pandas \
    numpy \
    python-dateutil \
    pyyaml \
    pydantic \
    git+https://github.com/TimefoldAI/timefold-solver.git

# Set working directory for the application
WORKDIR /app

# Command to run when container starts
# CMD ["python3", "main.py"]
CMD ["/bin/bash"]