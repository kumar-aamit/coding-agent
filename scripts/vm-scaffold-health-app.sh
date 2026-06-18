#!/usr/bin/env bash
#
# VM one-shot: create git branch + health app placeholder files + OpenCode build config.
#
# Usage (on OpenClaw VM):
#   chmod +x scripts/vm-scaffold-health-app.sh
#   ./scripts/vm-scaffold-health-app.sh
#
# Or without cloning first:
#   curl -fsSL https://raw.githubusercontent.com/kumar-aamit/coding-agent/health-bot/scripts/vm-scaffold-health-app.sh | bash
#
# Env overrides:
#   WORKDIR=/home/dcloud/openclaw/workspace/coding-agent
#   BRANCH=health-bot
#   SKIP_OPENCODE_GLOBAL=1    # skip ~/.config/opencode/opencode.json patch
#   SKIP_GIT_COMMIT=1         # write files only, no commit

set -euo pipefail

WORKDIR="${WORKDIR:-/home/dcloud/openclaw/workspace/coding-agent}"
BRANCH="${BRANCH:-health-bot}"
VLLM_BASE_URL="${VLLM_BASE_URL:-http://127.0.0.1:8000/v1}"
VLLM_MODEL="${VLLM_MODEL:-nvidia/llama-3.1-nemotron-nano-8b-v1}"

log()  { printf '\033[1;34m[scaffold]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m[ok]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[warn]\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31m[error]\033[0m %s\n' "$*" >&2; exit 1; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "Missing command: $1"
}

need_cmd git

if [[ ! -d "$WORKDIR/.git" ]]; then
  die "Not a git repo: $WORKDIR (clone or set WORKDIR=...)"
fi

cd "$WORKDIR"
log "Workdir: $WORKDIR"
log "Branch:  $BRANCH"

# --- git branch ---
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  log "Branch $BRANCH exists — checking out"
  git checkout "$BRANCH"
else
  CURRENT="$(git branch --show-current || true)"
  if [[ -n "$CURRENT" ]]; then
    git checkout -b "$BRANCH"
  else
    git checkout -b "$BRANCH"
  fi
  ok "Created branch $BRANCH"
fi

# --- placeholder files ---
log "Writing scaffold files..."

cat > requirements.txt <<'EOF'
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
sqlalchemy>=2.0.0
httpx>=0.27.0
pydantic>=2.0.0
EOF

cat > database.py <<'EOF'
"""SQLite database setup. TODO: implement engine, session factory, and init."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./health.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session."""
    # TODO: yield session and ensure close in finally block
    raise NotImplementedError("Implement get_db()")


def init_db() -> None:
    """Create tables on startup."""
    # TODO: import models and call Base.metadata.create_all(bind=engine)
    raise NotImplementedError("Implement init_db()")
EOF

cat > models.py <<'EOF'
"""SQLAlchemy models. TODO: implement Appointment model and any helpers."""

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), nullable=False)
    provider_name = Column(String(255), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    reason = Column(String(512), nullable=True)
    status = Column(String(50), nullable=False, default="scheduled")
EOF

cat > schemas.py <<'EOF'
"""Pydantic schemas. TODO: complete validation and response models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    patient_name: str
    provider_name: str
    scheduled_at: datetime
    reason: Optional[str] = None
    status: str = "scheduled"


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_name: Optional[str] = None
    provider_name: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None


class Appointment(AppointmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BestTimeRequest(BaseModel):
    provider_name: str
    preferred_date: Optional[str] = None
    reason: Optional[str] = None


class BestTimeResponse(BaseModel):
    recommended_time: str
    explanation: str


class WaitingTimeRequest(BaseModel):
    provider_name: str
    scheduled_at: datetime
    reason: Optional[str] = None


class WaitingTimeResponse(BaseModel):
    estimated_wait_minutes: int
    explanation: str
EOF

cat > llm_client.py <<EOF
"""OpenAI-compatible vLLM client for app runtime (not OpenCode). TODO: implement."""

import httpx

VLLM_BASE_URL = "${VLLM_BASE_URL}"
VLLM_MODEL = "${VLLM_MODEL}"


async def chat_completion(system: str, user: str) -> str:
    """Call vLLM /chat/completions and return assistant message content."""
    # TODO: POST to f"{VLLM_BASE_URL}/chat/completions" with model VLLM_MODEL
    raise NotImplementedError("Implement chat_completion()")
EOF

cat > main.py <<'EOF'
"""FastAPI health appointment app. TODO: wire CRUD + LLM endpoints."""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import schemas
from database import get_db, init_db

app = FastAPI(title="Health Appointment Tracker", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    # TODO: call init_db()
    pass


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/appointments", response_model=list[schemas.Appointment])
def list_appointments(db: Session = Depends(get_db)):
    raise NotImplementedError


@app.post("/appointments", response_model=schemas.Appointment, status_code=201)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    raise NotImplementedError


@app.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    raise NotImplementedError


@app.patch("/appointments/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(
    appointment_id: int,
    payload: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
):
    raise NotImplementedError


@app.delete("/appointments/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    raise NotImplementedError


@app.post("/best-time", response_model=schemas.BestTimeResponse)
async def suggest_best_time(payload: schemas.BestTimeRequest):
    raise NotImplementedError


@app.post("/waiting-time", response_model=schemas.WaitingTimeResponse)
async def estimate_waiting_time(payload: schemas.WaitingTimeRequest):
    raise NotImplementedError
EOF

cat > HEALTH_APP.md <<EOF
# Health appointment app ($BRANCH)

Scaffold only — coding agent implements TODOs; do not recreate structure.

## Stack
- FastAPI + SQLite (\`health.db\`)
- \`database.py\`, \`models.py\`, \`schemas.py\`, \`llm_client.py\`, \`main.py\`

## App LLM (not OpenCode)
- Base URL: \`${VLLM_BASE_URL}\`
- Model: \`${VLLM_MODEL}\`

## Done when
\`\`\`bash
pip install -r requirements.txt
python -c "import main"
uvicorn main:app --host 0.0.0.0 --port 8080
curl http://127.0.0.1:8080/health
\`\`\`
EOF

cat > opencode.json <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "build",
  "permission": {
    "edit": "allow",
    "bash": "allow",
    "doom_loop": "allow",
    "external_directory": "allow"
  }
}
EOF

ok "Scaffold files written"

ls -la database.py models.py schemas.py llm_client.py main.py requirements.txt HEALTH_APP.md opencode.json

# --- git commit ---
if [[ "${SKIP_GIT_COMMIT:-0}" != "1" ]]; then
  git add database.py models.py schemas.py llm_client.py main.py requirements.txt HEALTH_APP.md opencode.json
  if git diff --cached --quiet; then
    warn "No changes to commit (files unchanged)"
  else
    git commit -m "scaffold: health app placeholders on branch ${BRANCH}"
    ok "Committed on $(git branch --show-current): $(git log -1 --oneline)"
  fi
fi

# --- OpenCode global config (headless OCA needs build + allow) ---
if [[ "${SKIP_OPENCODE_GLOBAL:-0}" != "1" ]] && command -v python3 >/dev/null 2>&1; then
  OPENCODE_CFG="${HOME}/.config/opencode/opencode.json"
  log "Patching $OPENCODE_CFG (default_agent=build, permission=allow)"
  python3 <<'PY'
import json, pathlib, os
p = pathlib.Path(os.environ["HOME"]) / ".config/opencode/opencode.json"
cfg = json.loads(p.read_text()) if p.exists() else {}
cfg["default_agent"] = "build"
cfg["permission"] = {
    "edit": "allow",
    "bash": "allow",
    "doom_loop": "allow",
    "external_directory": "allow",
}
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(cfg, indent=2) + "\n")
print("Updated", p)
PY
  ok "OpenCode global config patched"
fi

# --- next steps ---
cat <<EOF

══════════════════════════════════════════════════════════════
  Scaffold ready on branch: ${BRANCH}
  Workdir: ${WORKDIR}
══════════════════════════════════════════════════════════════

1) Optional — restart gateway after OpenCode config change:
   openclaw gateway restart

2) Launch coding agent (OpenClaw chat / TUI):

/agent --name ${BRANCH} --harness opencode --workdir ${WORKDIR} --worktree-strategy off --permission-mode bypassPermissions

Branch ${BRANCH} is checked out. Scaffold files exist — DO NOT recreate project structure.
Read HEALTH_APP.md. Implement every TODO in:
  database.py, models.py, schemas.py, llm_client.py, main.py

Rules:
- Keep filenames and layout
- Replace NotImplementedError with working code
- App LLM only in llm_client.py: ${VLLM_BASE_URL} model ${VLLM_MODEL}
- Use build agent and edit/write tools (no planning-only output)
- When done run: pip install -r requirements.txt && python -c "import main"

3) Fallback if OCA loops — direct OpenCode:

   cd ${WORKDIR}
   opencode run --agent build "Implement all TODOs per HEALTH_APP.md. Use tools; do not replan."

EOF
