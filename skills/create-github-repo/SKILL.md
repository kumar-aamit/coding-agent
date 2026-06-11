---
name: "create-github-repo"
description: "Create GitHub repository for Simple LLM Chat Bot"
---

# Create GitHub Repository

This skill creates a GitHub repository for the Simple LLM Chat Bot:

**Prerequisites**
- GitHub CLI (`gh`) installed and authenticated
- Repository name: `chat-bot`
- Visibility: public

**Steps**
1. Create new repository:
   ```bash
   gh repo create chat-bot --public --source=/home/dcloud/coding-agent/chat-bot --remote=origin
   ```
2. Push initial commit:
   ```bash
   git push -u origin master
   ```
