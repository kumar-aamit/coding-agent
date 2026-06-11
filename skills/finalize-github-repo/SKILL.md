---
name: "finalize-github-repo"
description: "Finalize GitHub repository creation and push code"
---

# Finalize GitHub Repository

Update remote URL and push code:

```bash
# Set correct remote URL (replace USER with your GitHub username)
git remote set-url origin https://github.com/USER/chat-bot.git

# Push initial commit
git push -u origin master
```
