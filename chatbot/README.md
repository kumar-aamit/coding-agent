# Simple Chat Bot

This is a minimal chat bot project.

## Directory Structure

```
chatbot
├── app
│   └── bot.py          # Main bot entrypoint
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
└── README.md           # Project description
```

## Docker Deployment

To build and run the bot:

```bash
# Build the Docker image
docker build -t simple-chat-bot .
docker run -d -p 5000:5000 simple-chat-bot
```

The bot will be accessible at `http://localhost:5000`.