#!/usr/bin/env python3
"""Publish the canonical shared-brain projection to GitHub Pages.

Designed for OpenClaw's WSL cron. It never stages unrelated files and fails closed
when push or public read-back fails.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

REPO = Path(__file__).resolve().parent
SYNC = REPO / "sync_shared_brain_to_github.py"
EXPORTER = REPO / "export_kanban_status.py"
COMPILER = REPO / "compile_hot_cache.py"
ASKPASS = REPO / "git_askpass_env.sh"
TARGETS = [
    "index.html",
    "hot.md",
    "kanban.html",
    "kanban_status.json",
    "projects/publishing_matrix.md",
    "matrix/index.html",
    "matrix/graph_data.json",
    "concepts/agent-collaboration-contract.md",
    "concepts/codex-context-management.md",
    "concepts/data-source-integrity-and-fallback.md",
    "concepts/discord-ai-digest-presentation.md",
    "concepts/podcast-current-production-contract.md",
    "concepts/runtime-environment-map.md",
    "concepts/workspace-architecture.md",
    "concepts/public_apis_free_data_source_index.md",
]
PROBE = "https://jnocode.github.io/wiki/concepts/codex-context-management.md"
MARKER = "Codex 上下文管理與跨 Agent 帳本"
KANBAN_JSON_PROBE = "https://jnocode.github.io/wiki/kanban_status.json"
REQUIRED_READBACK_SURFACES = [
    "https://jnocode.github.io/wiki/index.html",
    "https://jnocode.github.io/wiki/hot.md",
    "https://jnocode.github.io/wiki/kanban.html",
]


def run(*args: str, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=REPO, text=True, capture_output=True, check=check, env=env)


def main() -> int:
    # 1. First sync projection from canonical shared brain
    sync = run(sys.executable, str(SYNC), check=False)
    if sync.returncode != 0:
        print("PUBLISH_BLOCKED shared_brain_sync_failed=true", file=sys.stderr)
        return 1
    changed = [line.removeprefix("UPDATED ") for line in sync.stdout.splitlines() if line.startswith("UPDATED ")]

    # 2. Export fresh kanban snapshot right before compilation and staging
    exporter = run(sys.executable, str(EXPORTER), check=False)
    if exporter.returncode != 0:
        print("PUBLISH_BLOCKED kanban_export_failed=true", file=sys.stderr)
        return 1

    # Read and strictly validate local kanban_status.json before any commit/push
    kanban_json_path = REPO / "kanban_status.json"
    if not kanban_json_path.exists():
        print("PUBLISH_BLOCKED local_kanban_json_missing=true", file=sys.stderr)
        return 1

    try:
        with open(kanban_json_path, encoding="utf-8") as f:
            local_kanban_data = json.load(f)
    except Exception as e:
        print(f"PUBLISH_BLOCKED local_kanban_json_unreadable={e}", file=sys.stderr)
        return 1

    if not local_kanban_data.get("is_snapshot"):
        print("PUBLISH_BLOCKED local_kanban_missing_snapshot_identity=true", file=sys.stderr)
        return 1

    expected_generated_at = local_kanban_data.get("generated_at")
    if not expected_generated_at or not isinstance(expected_generated_at, str) or not expected_generated_at.strip():
        print("PUBLISH_BLOCKED local_kanban_missing_generated_at=true", file=sys.stderr)
        return 1

    try:
        from datetime import datetime, timezone, timedelta
        gen_dt = datetime.fromisoformat(expected_generated_at)
        now_dt = datetime.now(timezone.utc)
        # Check future timestamp (> 1 hour) or stale timestamp (> 30 hours)
        if gen_dt > now_dt + timedelta(hours=1):
            print(f"PUBLISH_BLOCKED local_kanban_future_timestamp={expected_generated_at}", file=sys.stderr)
            return 1
        if now_dt - gen_dt > timedelta(hours=30):
            print(f"PUBLISH_BLOCKED local_kanban_stale_timestamp={expected_generated_at}", file=sys.stderr)
            return 1
    except Exception as te:
        print(f"PUBLISH_BLOCKED local_kanban_invalid_timestamp={te}", file=sys.stderr)
        return 1

    if not isinstance(local_kanban_data.get("tasks"), list):
        print("PUBLISH_BLOCKED local_kanban_tasks_not_list=true", file=sys.stderr)
        return 1

    summary_obj = local_kanban_data.get("summary")
    if not isinstance(summary_obj, dict) or not summary_obj:
        print("PUBLISH_BLOCKED local_kanban_summary_empty=true", file=sys.stderr)
        return 1

    expected_tasks = local_kanban_data.get("tasks", [])
    expected_task_ids = {str(t.get("id")) for t in expected_tasks if isinstance(t, dict)}

    # 3. Compile hot cache only after projection sync & export
    compiled = run(sys.executable, str(COMPILER), check=False)
    if compiled.returncode != 0:
        print("PUBLISH_BLOCKED hot_cache_compile_failed=true", file=sys.stderr)
        return 1

    # 3.5 重新生成全息決鬥場 3D 圖譜資料
    duel_script = REPO / "scripts/generate_duel_graph_data.py"
    if duel_script.exists():
        run(sys.executable, str(duel_script), check=False)

    # 4. Stage strictly the allow-listed projection
    run("git", "add", *TARGETS)
    staged = [x for x in run("git", "diff", "--cached", "--name-only").stdout.splitlines() if x]
    if any(x not in TARGETS for x in staged):
        print("PUBLISH_BLOCKED staged_scope_violation=true", file=sys.stderr)
        return 2

    pending = run("git", "rev-list", "--count", "origin/main..HEAD").stdout.strip()
    if not staged and pending == "0":
        print("PUBLISH_NOOP shared_brain_unchanged=true")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if staged:
        commit = run(
            "git", "-c", "user.name=jnocode", "-c",
            "user.email=78481666+Jnocode@users.noreply.github.com",
            "commit", "-m", f"docs: sync shared brain and kanban to GitHub Pages ({stamp})", check=False,
        )
        if commit.returncode != 0:
            print("PUBLISH_BLOCKED commit_failed=true", file=sys.stderr)
            return 3
    push_env = os.environ.copy()
    if os.name != "nt":
        if not push_env.get("GITHUB_TOKEN"):
            print("PUBLISH_BLOCKED github_token_missing=true", file=sys.stderr)
            return 4
        push_env.update({
            "GIT_ASKPASS": str(ASKPASS),
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "credential.helper",
            "GIT_CONFIG_VALUE_0": "",
        })
    push = run("git", "push", "origin", "main", check=False, env=push_env)
    if push.returncode != 0:
        print("PUBLISH_BLOCKED push_failed=true", file=sys.stderr)
        return 4

    # 5. Read-back verification: verify all required surfaces AND exact kanban_status.json equality
    for surface_url in REQUIRED_READBACK_SURFACES:
        try:
            with urlopen(surface_url + "?sync=" + stamp, timeout=30) as s_resp:
                if s_resp.status != 200:
                    print(f"PUBLISH_BLOCKED surface_readback_failed status={s_resp.status} url={surface_url}", file=sys.stderr)
                    return 5
        except Exception as e:
            print(f"PUBLISH_BLOCKED surface_readback_error url={surface_url} error={e}", file=sys.stderr)
            return 5

    with urlopen(PROBE + "?sync=" + stamp, timeout=30) as response:
        body = response.read().decode("utf-8", "replace")
        status = response.status
    if status != 200 or MARKER not in body:
        print("PUBLISH_BLOCKED public_readback_failed=true", file=sys.stderr)
        return 5

    try:
        with urlopen(KANBAN_JSON_PROBE + "?sync=" + stamp, timeout=30) as k_resp:
            remote_k_data = json.loads(k_resp.read().decode("utf-8", "replace"))

        # Exact equality check: summary, tasks count, IDs, task titles, delivery, generated_at
        if remote_k_data != local_kanban_data:
            # Check specific fields for precise logging
            if remote_k_data.get("generated_at") != expected_generated_at:
                print(f"PUBLISH_BLOCKED remote_kanban_timestamp_mismatch remote={remote_k_data.get('generated_at')} expected={expected_generated_at}", file=sys.stderr)
                return 5
            remote_tasks = remote_k_data.get("tasks", [])
            remote_ids = [t.get("id") for t in remote_tasks if isinstance(t, dict)]
            local_ids = [t.get("id") for t in expected_tasks if isinstance(t, dict)]
            if remote_ids != local_ids:
                print(f"PUBLISH_BLOCKED remote_kanban_ids_mismatch remote={remote_ids} expected={local_ids}", file=sys.stderr)
                return 5
            print("PUBLISH_BLOCKED remote_kanban_content_mismatch", file=sys.stderr)
            return 5
    except Exception as e:
        print(f"PUBLISH_BLOCKED remote_kanban_readback_error={e}", file=sys.stderr)
        return 5

    print(f"PUBLISH_OK changed={len(changed)} committed={len(staged)} public_readback=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
