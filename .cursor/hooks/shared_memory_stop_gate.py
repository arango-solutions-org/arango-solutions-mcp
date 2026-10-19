#!/usr/bin/env python3
"""Cursor stop gate for PRD drift and missing pattern-application attribution."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from typing import Any

STATE_DIR = os.path.join(".cursor", ".shared-memory-sessions")


def _event_id(payload: dict[str, Any]) -> str:
    raw = payload.get("conversation_id") or payload.get("generation_id") or "unknown"
    return re.sub(r"[^A-Za-z0-9_.-]", "-", str(raw))[:120]


def _state_path(payload: dict[str, Any]) -> str:
    return os.path.join(STATE_DIR, f"{_event_id(payload)}.json")


def _pending_keys(payload: dict[str, Any]) -> list[str]:
    try:
        with open(_state_path(payload), encoding="utf-8") as fh:
            state = json.load(fh)
        surfaced = state.get("surfaced_keys", [])
        # A surfaced key is RESOLVED when it was either applied (reuse attributed) or
        # explicitly dismissed (reviewed, deliberately not reused). Counting only
        # applied_keys made this nudge unsatisfiable: it demanded that every surfaced
        # key be applied while its own message forbids marking every result as applied.
        # Kept identical to the Claude gate in drift_stop_gate.sh — see that file.
        resolved = set(state.get("applied_keys", [])) | set(state.get("dismissed_keys", []))
        return [key for key in surfaced if key not in resolved]
    except (OSError, json.JSONDecodeError, AttributeError):
        return []


def _drift_counts() -> tuple[int, int]:
    if os.path.exists(".no-drift-gate"):
        return 0, 0
    try:
        names = os.listdir(".prd-drift-queue")
    except OSError:
        return 0, 0
    return len(names), sum(name.startswith("prd_") for name in names)


def _mine_capture_candidates(payload: dict[str, Any]) -> None:
    """Best-effort reuse of the Claude miner when transcript shapes are compatible."""
    try:
        subprocess.run(
            [sys.executable, ".claude/hooks/capture_candidates.py"],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=7,
            check=False,
        )
    except Exception:  # noqa: BLE001
        pass


def _cleanup_state(payload: dict[str, Any]) -> None:
    try:
        os.remove(_state_path(payload))
    except OSError:
        pass


def followup(payload: dict[str, Any]) -> str:
    drift_count, prd_count = _drift_counts()
    pending = _pending_keys(payload)
    parts: list[str] = []

    if drift_count:
        extra = f", including {prd_count} PRD edit(s)" if prd_count else ""
        parts.append(
            f"[PRD-DRIFT GATE] {drift_count} change(s) are queued{extra}. "
            "Run /prd-sync now; it audits the changes and clears the queue."
        )
    if pending:
        # Both halves must be actionable: prose ("state that explicitly") has no effect
        # on the state file, so a message that only says that cannot be satisfied. The
        # dismissal tool is shared with the Claude runtime and locates this session's
        # state under .cursor/ on its own.
        parts.append(
            f"[SHARED-MEMORY APPLY GATE] {len(pending)} surfaced pattern(s) unresolved. "
            "For any result that informed the solution, call pattern-applied with only "
            "those key(s). For the rest — reviewed and deliberately not reused — record "
            "that decision: python3 .claude/hooks/dismiss_surfaced.py "
            f"{_event_id(payload)} {' '.join(pending)} "
            "Never mark every search result as applied."
        )
    return " ".join(parts)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        print("{}")
        return 0

    _mine_capture_candidates(payload)
    loop_count = payload.get("loop_count", 0)
    if not isinstance(loop_count, int) or loop_count > 0:
        _cleanup_state(payload)
        print("{}")
        return 0

    message = followup(payload)
    print(json.dumps({"followup_message": message} if message else {}))
    if not message:
        _cleanup_state(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
