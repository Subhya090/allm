# Use a Python-based slim image as the base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies: GCC for compiling C code, and Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && pip install --no-cache-dir -r requirements.txt

# Copy the current directory content into the container
COPY . /app

# Compile the sharp.C file into the executable "sharp"
RUN gcc -o sharp sharp.C

# Set environment variables for the bot
# These can be overwritten by environment variables at runtime (for security)
ENV BOT_TOKEN=your-bot-token-here
ENV FLASK_PORT=5000

# Expose the Flask port
EXPOSE 5000

# Run the bot
CMD ["python", "bot.py"]
