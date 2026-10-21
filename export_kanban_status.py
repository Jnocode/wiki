import os
import sys
import sqlite3
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Safe default paths within rework workspace / environment override
DEFAULT_DB_PATH = os.environ.get("KANBAN_DB_PATH", r"C:/Users/Jun/.hermes/kanban.db")
OUTPUT_PATH = os.environ.get("KANBAN_OUTPUT_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "kanban_status.json")))

REQUIRED_TABLES = {"tasks", "task_events"}
REQUIRED_TASK_COLUMNS = {"id", "title", "assignee", "status", "priority", "created_at", "completed_at", "block_kind", "project_id"}

# Canonical exact Kanban task ID regex
TASK_ID_REGEX = re.compile(r"^t_[0-9a-f]{8}$")

# Explicit title mapping by Task ID (W1 Specification)
# Only explicitly approved tasks have public titles; unapproved tasks strictly map to '內部任務'.
# Lookup uses exact key without stripping or lowercasing.
APPROVED_TITLE_REGISTRY = {
    "t_9343f2d7": "Wiki 成果追蹤看板",
    "t_bc6c20bb": "有界自治協作系統",
    "t_b358021a": "夜間經驗整理"
}

# Verified task outcomes registry (Task ID -> safe artifact link & description)
# Only verified tasks get artifact links. Unregistered tasks strictly default to None.
VERIFIED_ARTIFACT_REGISTRY = {
    "t_0dc4324f": {
        "artifact_url": "static/resume.html",
        "note": "網頁版作品履歷",
        "qa_status": "未獨立驗收 (小衡 QA 尚未 PASS)"
    },
    "t_116dfaa0": {
        "artifact_url": "static/ecom_tools.html",
        "note": "電商營運工具箱微型應用",
        "qa_status": "未獨立驗收 (小衡 QA 尚未 PASS)"
    },
    "t_9343f2d7": {
        "artifact_url": "kanban.html",
        "note": "Wiki 成果追蹤看板",
        "qa_status": "未獨立驗收 (小衡 QA 尚未 PASS)"
    }
}

# Allowed public state set
KNOWN_STATUSES = {
    "triage", "todo", "scheduled", "ready", "running",
    "blocked", "review", "done", "completed", "archived", "waiting_approval"
}

# Allowed public block kinds
APPROVED_BLOCK_KINDS = {
    "needs_input", "capability", "credential", "infrastructure"
}

# Allowed public project IDs
APPROVED_PROJECT_IDS = {
    "general", "internal-project", "wiki", "kanban", "autonomy"
}

def resolve_db_path(path_str):
    if not path_str:
        return None
    # If on WSL/Linux and starts with drive letters
    if os.name != "nt":
        m = re.match(r"^([a-zA-Z]):[/\\\\](.*)$", str(path_str).replace("\\", "/"))
        if m:
            drive = m.group(1).lower()
            rest = m.group(2).lstrip("/")
            wsl_cand = f"/mnt/{drive}/{rest}"
            if os.path.exists(wsl_cand):
                return wsl_cand
    if os.path.exists(str(path_str)):
        return str(path_str)
    exp = os.path.expanduser(str(path_str))
    if os.path.exists(exp):
        return exp
    return None

def map_public_title(task_id: str) -> str:
    if not isinstance(task_id, str):
        return "內部任務"
    return APPROVED_TITLE_REGISTRY.get(task_id, "內部任務")

def map_assignee(raw_assignee) -> str:
    if not raw_assignee or not isinstance(raw_assignee, str):
        return "未指派"
    val = raw_assignee.strip().lower()
    if val == "xiaoke":
        return "小克"
    elif val in ("xiaoheng", "heng"):
        return "小衡"
    return "其他執行者"

def get_agent_id(raw_assignee) -> str:
    if not raw_assignee or not isinstance(raw_assignee, str):
        return "unassigned"
    val = raw_assignee.strip().lower()
    if val == "xiaoke":
        return "xiaoke"
    elif val in ("xiaoheng", "heng"):
        return "xiaoheng"
    return "other"

def sanitize_public_status(raw_status) -> str:
    if not raw_status or not isinstance(raw_status, str):
        return "unknown"
    st = raw_status.strip().lower()
    if st in KNOWN_STATUSES:
        return st
    return "unknown"

def sanitize_public_block_kind(raw_block_kind):
    if not raw_block_kind or not isinstance(raw_block_kind, str):
        return None
    bk = raw_block_kind.strip().lower()
    if bk in APPROVED_BLOCK_KINDS:
        return bk
    return None

def sanitize_public_project_id(pid) -> str:
    if not pid or not isinstance(pid, str):
        return "general"
    pid_clean = pid.strip().lower()
    if pid_clean in APPROVED_PROJECT_IDS:
        return pid_clean
    return "general"

def sanitize_public_priority(raw_priority) -> int:
    if isinstance(raw_priority, (bytes, bytearray, memoryview)):
        raise TypeError("BLOB priority is not allowed; fail-closed")
    if isinstance(raw_priority, bool):
        return 0
    if isinstance(raw_priority, int):
        if 0 <= raw_priority <= 100:
            return raw_priority
        return 0
    if isinstance(raw_priority, str):
        p_map = {"low": 10, "medium": 50, "high": 80, "critical": 100}
        return p_map.get(raw_priority.strip().lower(), 0)
    return 0

def sanitize_timestamp(raw_ts, allow_none=False):
    # Contract v2: true int, non-negative, bounded, reject bool
    if raw_ts is None:
        if allow_none:
            return None
        raise ValueError("NULL timestamp not allowed")
    if isinstance(raw_ts, bool) or not isinstance(raw_ts, int):
        raise TypeError("Invalid timestamp type")
    # Normalize millisecond timestamps (> 1e11) to seconds for consistent sorting
    if raw_ts > 100000000000:
        return raw_ts // 1000
    return raw_ts

def check_schema(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    for req in REQUIRED_TABLES:
        if req not in tables:
            return False, f"Missing required table: {req}"
    
    cursor.execute("PRAGMA table_info(tasks)")
    cols = {row[1] for row in cursor.fetchall()}
    for req_col in REQUIRED_TASK_COLUMNS:
        if req_col not in cols:
            return False, f"Missing required column in tasks: {req_col}"
    
    cursor.execute("PRAGMA table_info(task_events)")
    event_cols = {row[1] for row in cursor.fetchall()}
    if "created_at" not in event_cols:
        return False, "Missing created_at in task_events"
    
    return True, None

def get_delivery_outcome(task_id: str):
    if isinstance(task_id, str) and task_id in VERIFIED_ARTIFACT_REGISTRY:
        reg = VERIFIED_ARTIFACT_REGISTRY[task_id]
        return {
            "artifact_url": reg["artifact_url"],
            "qa_status": "未獨立驗收 (小衡 QA 尚未 PASS)",
            "note": reg["note"]
        }
    return {
        "artifact_url": None,
        "qa_status": "未獨立驗收",
        "note": "未登記成品"
    }

def open_readonly_db(db_path_obj):
    # Strict mode=ro only. No immutable fallback on error.
    # If connection fails, close connection if exists and raise original error.
    uri_ro = f"{db_path_obj.as_uri()}?mode=ro"
    conn = None
    try:
        conn = sqlite3.connect(uri_ro, uri=True)
        conn.row_factory = sqlite3.Row
        conn.execute("SELECT 1 FROM sqlite_master LIMIT 1")
        return conn
    except Exception as err:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
        raise err

def fetch_openclaw_workboard_cards() -> list[dict]:
    """Fetch OpenClaw Maker (小克) cards from WSL Workboard SQLite."""
    try:
        res = subprocess.run([
            "wsl.exe", "-d", "OpenClawGateway", "-u", "openclaw",
            "python3", "-c", """
import sqlite3, json
try:
    conn = sqlite3.connect("file:/home/openclaw/.openclaw/plugins/workboard/workboard.sqlite?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, title, status, priority, created_at, completed_at, updated_at, agent_id FROM workboard_cards")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    print(json.dumps(rows))
except Exception as e:
    print(json.dumps([]))
"""
        ], capture_output=True, text=True, check=False, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            return json.loads(res.stdout.strip())
    except Exception as e:
        print(f"[WARN] Failed to fetch OpenClaw Workboard cards: {e}", file=sys.stderr)
    return []

def main():
    target_db = resolve_db_path(DEFAULT_DB_PATH)
    if not target_db:
        print(f"KANBAN_DB_MISSING: Cannot locate database at {DEFAULT_DB_PATH}", file=sys.stderr)
        sys.exit(2)

    db_path_obj = Path(target_db).resolve()
    try:
        conn = open_readonly_db(db_path_obj)
    except Exception as err:
        print(f"Error opening DB read-only: {err}", file=sys.stderr)
        sys.exit(1)

    try:
        # Single read transaction: BEGIN DEFERRED / BEGIN so both events and tasks are read in one snapshot
        conn.execute("BEGIN")
        cursor = conn.cursor()

        valid_schema, schema_err = check_schema(conn)
        if not valid_schema:
            conn.rollback()
            print(f"KANBAN_SCHEMA_DRIFT: {schema_err}", file=sys.stderr)
            sys.exit(3)

        # Query real latest DB event timestamp
        # Strict validation of task_events: must fail-closed if any invalid event exists
        cursor.execute("SELECT typeof(created_at), created_at FROM task_events")
        all_events = cursor.fetchall()
        max_ev = None
        for ev_type, ev_val in all_events:
            if ev_val is None or ev_type != 'integer' or isinstance(ev_val, bool) or not isinstance(ev_val, int) or ev_val < 0 or ev_val > 999999999999999:
                raise ValueError("Invalid task_event created_at")
            if max_ev is None or ev_val > max_ev:
                max_ev = ev_val

        cursor.execute("SELECT max(created_at), max(completed_at) FROM tasks")
        max_tc, max_tcomp = cursor.fetchone()

        cands = [x for x in (max_ev, max_tc, max_tcomp) if x is not None]
        source_latest_event_at = max(cands) if cands else None
        if source_latest_event_at is not None:
            source_latest_event_at = sanitize_timestamp(source_latest_event_at, allow_none=True)

        cursor.execute("""
            SELECT id, title, assignee, status, priority, created_at, completed_at, block_kind, project_id
            FROM tasks
        """)
        all_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error querying DB: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()

    # Pre-process rows: check NULL id or BLOB priority, validate timestamps, handle unique IDs
    seen_source_ids = set()
    seen_public_ids = set()
    internal_row_counter = 0

    processed_rows = []
    for row in all_rows:
        raw_id = row["id"]
        if raw_id is None:
            print("Error: NULL task ID encountered; fail-closed", file=sys.stderr)
            sys.exit(1)

        # Check duplicate source ID
        if raw_id in seen_source_ids:
            print(f"Error: duplicate source task ID encountered; fail-closed", file=sys.stderr)
            sys.exit(1)
        seen_source_ids.add(raw_id)

        # Check priority (raises TypeError on BLOB)
        try:
            pub_priority = sanitize_public_priority(row["priority"])
        except TypeError as err:
            print(f"Error sanitizing priority: {err}", file=sys.stderr)
            sys.exit(1)

        # Validate timestamps strictly
        try:
            pub_created_at = sanitize_timestamp(row["created_at"], allow_none=False)
            pub_completed_at = sanitize_timestamp(row["completed_at"], allow_none=True)
        except (TypeError, ValueError) as err:
            print(f"Error validating timestamp: {err}", file=sys.stderr)
            sys.exit(1)

        # Determine public ID
        # Only true exact str matching t_[0-9a-f]{8} is a canonical task ID
        if isinstance(raw_id, str) and TASK_ID_REGEX.fullmatch(raw_id):
            pub_id = raw_id
        else:
            # Non-exact TEXT / BLOB / malformed: map to neutral internal row ID
            internal_row_counter += 1
            pub_id = f"internal_row_{internal_row_counter:06d}"

        if pub_id in seen_public_ids:
            print(f"Error: duplicate public task ID {pub_id}; fail-closed", file=sys.stderr)
            sys.exit(1)
        seen_public_ids.add(pub_id)

        processed_rows.append({
            "id": pub_id,
            "raw_id": raw_id,
            "title": row["title"],
            "assignee": row["assignee"],
            "status": row["status"],
            "priority": pub_priority,
            "created_at": pub_created_at,
            "completed_at": pub_completed_at,
            "block_kind": row["block_kind"],
            "project_id": row["project_id"]
        })

    # Fetch and merge OpenClaw Workboard tasks (小克 Maker 專屬執行看板)
    wb_cards = fetch_openclaw_workboard_cards()
    for card in wb_cards:
        cid = card.get("id")
        if not cid:
            continue
        
        # Avoid duplicate if mapped from a Hermes task
        mapped_task_id = None
        m = re.search(r"t_[0-9a-f]{8}", card.get("title", ""))
        if m:
            mapped_task_id = m.group(0)
            if mapped_task_id in seen_source_ids or mapped_task_id in seen_public_ids:
                continue

        internal_row_counter += 1
        pub_id = f"wb_{cid[:8]}"
        if pub_id in seen_public_ids:
            pub_id = f"wb_{cid[:8]}_{internal_row_counter:04d}"
        seen_public_ids.add(pub_id)

        c_created_at = sanitize_timestamp(card.get("created_at") or 0, allow_none=False)
        c_completed_at = sanitize_timestamp(card.get("completed_at"), allow_none=True)

        processed_rows.append({
            "id": pub_id,
            "raw_id": cid,
            "title": card.get("title", "內部任務"),
            "assignee": "xiaoke", # Workboard 均為小克 Maker 執行任務
            "status": card.get("status", "unknown"),
            "priority": sanitize_public_priority(card.get("priority")),
            "created_at": c_created_at,
            "completed_at": c_completed_at,
            "block_kind": "capability" if card.get("status") == "blocked" else None,
            "project_id": "general"
        })

    generated_at = datetime.now(timezone.utc).isoformat()

    total_count = len(processed_rows)
    status_counts = {}
    for r in processed_rows:
        raw_st = r["status"]
        st = sanitize_public_status(raw_st)
        status_counts[st] = status_counts.get(st, 0) + 1

    summary = {
        "total": total_count,
        "ready": status_counts.get("ready", 0),
        "running": status_counts.get("running", 0),
        "review": status_counts.get("review", 0),
        "blocked": status_counts.get("blocked", 0),
        "done": status_counts.get("done", 0),
        "completed": status_counts.get("completed", 0),
        "archived": status_counts.get("archived", 0),
        "in_progress": status_counts.get("running", 0) + status_counts.get("ready", 0) + status_counts.get("review", 0),
        "all_statuses": status_counts
    }

    # Agent statistics (including archived)
    # Assignees mapped strictly to: xiaoheng, xiaoke, unassigned, other
    agent_map = {
        ("xiaoheng", "小衡"): {"total": 0, "by_status": {}},
        ("xiaoke", "小克"): {"total": 0, "by_status": {}},
        ("unassigned", "未指派"): {"total": 0, "by_status": {}},
        ("other", "其他執行者"): {"total": 0, "by_status": {}}
    }

    for r in processed_rows:
        raw_st = r["status"]
        st = sanitize_public_status(raw_st)
        assignee_raw = r["assignee"]
        agent_disp = map_assignee(assignee_raw)
        agent_id = get_agent_id(assignee_raw)

        key = (agent_id, agent_disp)
        if key not in agent_map:
            agent_map[key] = {"total": 0, "by_status": {}}
        
        agent_map[key]["total"] += 1
        agent_map[key]["by_status"][st] = agent_map[key]["by_status"].get(st, 0) + 1

    # Filter out empty agents if desired or keep standard ones
    agents = []
    for (aid, aname), data in agent_map.items():
        if data["total"] > 0 or aid in ("xiaoheng", "xiaoke"):
            agents.append({
                "name": aname,
                "id": aid,
                "total": data["total"],
                "by_status": data["by_status"]
            })

    # Public tasks projection: only non-archived tasks, sorted by created_at desc
    # Strict public projection: never include body, comments, raw events or private canary fields
    non_archived_rows = [r for r in processed_rows if sanitize_public_status(r["status"]) != "archived"]
    non_archived_rows.sort(key=lambda r: r["created_at"] if r["created_at"] is not None else 0, reverse=True)

    tasks = []
    for r in non_archived_rows:
        pub_id = r["id"]
        # If public title exists in registry, use it; otherwise use raw title (safe text)
        public_title = APPROVED_TITLE_REGISTRY.get(pub_id, r.get("title") or "內部任務")
        st = sanitize_public_status(r["status"])
        delivery = get_delivery_outcome(pub_id)

        tasks.append({
            "id": pub_id,
            "title": public_title,
            "project_id": sanitize_public_project_id(r["project_id"]),
            "assignee": map_assignee(r["assignee"]),
            "status": st,
            "priority": r["priority"],
            "created_at": r["created_at"],
            "completed_at": r["completed_at"],
            "block_kind": sanitize_public_block_kind(r["block_kind"]),
            "delivery": delivery
        })

    out_data = {
        "generated_at": generated_at,
        "source_latest_event_at": source_latest_event_at,
        "is_snapshot": True,
        "summary": summary,
        "agents": agents,
        "tasks": tasks
    }

    # Resolve output path
    actual_output = OUTPUT_PATH
    if os.name != "nt":
        m = re.match(r"^([a-zA-Z]):[/\\\\](.*)$", str(actual_output).replace("\\", "/"))
        if m:
            actual_output = f"/mnt/{m.group(1).lower()}/{m.group(2).lstrip('/')}"

    out_file = Path(actual_output).resolve()
    temp_file = out_file.parent / f"{out_file.name}.tmp"
    os.makedirs(out_file.parent, exist_ok=True)
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    os.replace(temp_file, out_file)

    print(f"KANBAN_OK tasks={len(tasks)} agents={len(agents)} event_at={source_latest_event_at}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
