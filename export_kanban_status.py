import os
import sys
import sqlite3
import json
from datetime import datetime, timezone

DB_PATH = r"C:/Users/Jun/.hermes/kanban.db"
OUTPUT_PATH = r"D:/Workspace/03_Dev_Projects/wiki/kanban_status.json"

def map_assignee(raw_assignee):
    if not raw_assignee:
        return "未指派"
    val = raw_assignee.strip().lower()
    if val == "xiaoke":
        return "小克"
    elif val in ("xiaoheng", "heng"):
        return "小衡"
    return raw_assignee

def get_agent_id(raw_assignee):
    if not raw_assignee:
        return "unassigned"
    val = raw_assignee.strip().lower()
    if val == "xiaoke":
        return "xiaoke"
    elif val in ("xiaoheng", "heng"):
        return "xiaoheng"
    return val

def main():
    if not os.path.exists(DB_PATH):
        print("KANBAN_DB_MISSING")
        sys.exit(0)

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, assignee, status, priority, created_at, completed_at, block_kind FROM tasks")
        all_rows = cursor.fetchall()
    except Exception as e:
        print(f"Error accessing DB: {e}", file=sys.stderr)
        sys.exit(1)

    generated_at = datetime.now(timezone.utc).isoformat()

    # summary 包含所有任務 (含 archived)
    total_count = len(all_rows)
    done_count = 0
    blocked_count = 0
    ready_count = 0
    running_count = 0

    # Agent 統計 (含 archived)
    agent_map = {} # key: (agent_id, display_name) -> {"total": N, "by_status": {}}

    for row in all_rows:
        st = row["status"]
        if st == "done":
            done_count += 1
        elif st == "blocked":
            blocked_count += 1
        elif st == "ready":
            ready_count += 1
        elif st == "running":
            running_count += 1

        assignee_raw = row["assignee"]
        agent_disp = map_assignee(assignee_raw)
        agent_id = get_agent_id(assignee_raw)

        key = (agent_id, agent_disp)
        if key not in agent_map:
            agent_map[key] = {"total": 0, "by_status": {}}
        
        agent_map[key]["total"] += 1
        agent_map[key]["by_status"][st] = agent_map[key]["by_status"].get(st, 0) + 1

    in_progress_count = running_count + ready_count

    summary = {
        "total": total_count,
        "done": done_count,
        "blocked": blocked_count,
        "ready": ready_count,
        "running": running_count,
        "in_progress": in_progress_count
    }

    # 確保預設有 小衡 (xiaoheng) 與 小克 (xiaoke) 兩個 Agent 條目
    default_agents = [
        ("xiaoheng", "小衡"),
        ("xiaoke", "小克")
    ]
    for aid, aname in default_agents:
        if (aid, aname) not in agent_map:
            agent_map[(aid, aname)] = {"total": 0, "by_status": {}}

    agents = []
    for (aid, aname), data in agent_map.items():
        agents.append({
            "name": aname,
            "id": aid,
            "total": data["total"],
            "by_status": data["by_status"]
        })

    # tasks 只包含 status != 'archived' 的任務，並依 created_at 降序
    non_archived_rows = [r for r in all_rows if r["status"] != "archived"]
    non_archived_rows.sort(key=lambda r: r["created_at"] if r["created_at"] is not None else 0, reverse=True)

    tasks = []
    for r in non_archived_rows:
        tasks.append({
            "id": r["id"],
            "title": r["title"],
            "assignee": map_assignee(r["assignee"]),
            "status": r["status"],
            "priority": r["priority"],
            "created_at": r["created_at"],
            "completed_at": r["completed_at"],
            "block_kind": r["block_kind"]
        })

    out_data = {
        "generated_at": generated_at,
        "summary": summary,
        "agents": agents,
        "tasks": tasks
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    print(f"KANBAN_OK tasks={len(tasks)} agents={len(agents)}")

if __name__ == "__main__":
    main()
