---
name: "demo-dev-coding-agent"
description: "Demo skill that uses dev-coding-agent functionality."
---

## Demo Skill

This is a minimal example of a reusable skill for OpenClaw agents. It shows the structure and basic content required for a skill proposal.

## Usage

Agents can import and call this skill to perform common coding tasks such as background feature builds, PR reviews, and issue-to-PR loops.

## Hard Rules

1. Always launch with `background:true`.
2. Use `pty:true` for Codex and OpenCode, and `claude --permission-mode bypassPermissions --print` for Claude Code.
3. Capture notification route before spawning.
4. Send completion/failure via `openclaw message send`.
5. Never run inside `~/.openclaw` or `$OPENCLAW_STATE_DIR`.

## Prompt Template

Fill in the notification route and task details before spawning a worker.

``` 
Notification route:
- channel: <notifyChannel>
- target: <notifyTarget>
- account: <notifyAccount or omit>
- reply_to: <notifyReplyTo or omit>
- thread_id: <notifyThreadId or omit>

Task: <brief description>
Instructions: <any special constraints>
```

## Dependencies

Ensure required CLI tools are installed and in `$PATH`.

## Installation

Add this skill to the agent's skills directory and enable it in `skills.json`.
