# Use official Python 3.10 image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy files to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (Render will override these if set in dashboard)
ENV BOT_TOKEN=default
ENV ADMIN_CHAT_ID=0

# Start the bot
CMD ["python", "bot.py"]
