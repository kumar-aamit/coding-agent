# Dockerfile for Simple LLM Chat Bot

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000 for LLM
EXPOSE 8000

# Run the bot
CMD ["python", "bot.py"]