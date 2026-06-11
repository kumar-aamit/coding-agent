#!/bin/bash
# Setup script for chat bot repository

# Create new repository directory
mkdir -p /home/dcloud/coding-agent/chat-bot
cd /home/dcloud/coding-agent/chat-bot

# Copy necessary files
cp ../Dockerfile .
cp ../requirements.txt .
cp ../bot.py .

# Initialize git repository
git init
git add .
git commit -m "Initial commit: Simple LLM Chat Bot"

# Create GitHub repository (would use GitHub CLI in real scenario)
echo "# Simple LLM Chat Bot" > README.md
git add README.md
git commit -m "Add README"

echo "Repository setup complete in /home/dcloud/coding-agent/chat-bot"