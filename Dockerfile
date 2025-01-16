# Use a Python base image
FROM python:3.9-slim

# Install dependencies for C program compilation and other required libraries
RUN apt-get update && apt-get install -y gcc make && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install pyTelegramBotAPI flask

# Copy the application code (including sharp.c and bot.py)
COPY . /app
WORKDIR /app

# Compile sharp.c to create the sharp executable
RUN gcc -o sharp sharp.c -lpthread && chmod +x sharp

# Switch to a non-root user for security reasons
RUN useradd -m nonrootuser
USER nonrootuser

# Expose the port for Flask
EXPOSE 5000

# Run the bot script
CMD ["python", "bot.py"]
