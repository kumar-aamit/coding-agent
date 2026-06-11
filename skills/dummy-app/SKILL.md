---
name: "dummy-app"
description: "Write a dummy application to showcase dev-coding-agent functionality"
---

# Setup Instructions

This project contains setup steps for the OpenCode development environment. Follow these steps to configure and run the project.

## Prerequisites
- Node.js v18 or higher
- Git
- OpenCode CLI

## Installation
1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/openclaw/coding-agent.git
   cd coding-agent
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Configure environment variables:
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your preferred settings
   \`\`\`

4. Build the project:
   \`\`\`bash
   npm run build
   \`\`\`

## Usage
Run the application with:
\`\`\`bash
npm start
\`\`\`

For development with hot-reloading:
\`\`\`bash
npm run dev
\`\`\`

## Testing
Run tests with:
\`\`\`bash
npm test
\`\`\`
