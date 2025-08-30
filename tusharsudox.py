import json
import os
import asyncio
from datetime import datetime, timedelta
import pytz

# =============== CONFIG ===============
OWNER_ID = 5840594311
SUDO_USERS = [5840594311]  # manually add karne ke liye
AUTH_CHANNELS = []  # apne channels/groups IDs
DB_FILE = "sudo_db.json"
IST = pytz.timezone("Asia/Kolkata")
# ======================================

# ensure db file exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"permanent": [], "temporary": []}, f)


def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def parse_multiple_durations(duration_str: str):
    """Parse string like '2d 3h 5m' into timedelta"""
    days, hours, minutes = 0, 0, 0
    parts = duration_str.split()
    for p in parts:
        if p.endswith("d"):
            days += int(p[:-1])
        elif p.endswith("h"):
            hours += int(p[:-1])
        elif p.endswith("m"):
            minutes += int(p[:-1])
    return timedelta(days=days, hours=hours, minutes=minutes)


def add_sudo(user_id: int, duration: timedelta = None):
    db = load_db()
    if duration is None:
        if user_id not in db["permanent"]:
            db["permanent"].append(user_id)
    else:
        expiry = (datetime.now(IST) + duration).timestamp()
        db["temporary"] = [t for t in db["temporary"] if t["id"] != user_id]
        db["temporary"].append({"id": user_id, "expiry": expiry})
    save_db(db)


def remove_sudo(user_id: int):
    db = load_db()
    if user_id in db["permanent"]:
        db["permanent"].remove(user_id)
    db["temporary"] = [t for t in db["temporary"] if t["id"] != user_id]
    save_db(db)


def is_authorized(user_id: int):
    if user_id == OWNER_ID:
        return True

    if user_id in SUDO_USERS or user_id in AUTH_CHANNELS:
        return True

    db = load_db()
    if user_id in db["permanent"]:
        return True

    now = datetime.now(IST).timestamp()
    for t in db["temporary"]:
        if t["id"] == user_id and t["expiry"] > now:
            return True
    return False


def format_remaining(expiry_ts: float):
    """Expiry तक कितना टाइम बचा है readable format में"""
    now_ts = datetime.now(IST).timestamp()
    diff = int(expiry_ts - now_ts)
    if diff <= 0:
        return "❌ Expired"
    mins, sec = divmod(diff, 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    return f"{days}d {hrs}h {mins}m"


def list_sudo():
    db = load_db()
    text = "📝 **Sudo List**\n\n"

    # Permanent
    all_perm = list(set(db["permanent"] + SUDO_USERS + AUTH_CHANNELS))
    if all_perm:
        text += "🔒 **Permanent Sudo:**\n"
        for uid in all_perm:
            if uid == OWNER_ID:
                text += f"👑 Owner → `{uid}` (Permanent)\n"
            elif str(uid).startswith("-100"):
                text += f"📢 Channel/Group → `{uid}` (Permanent)\n"
            else:
                text += f"👤 User → `{uid}` (Permanent)\n"
    else:
        text += "🔒 No permanent sudo.\n"

    # Temporary
    now = datetime.now(IST).timestamp()
    active_temp = []
    for t in db["temporary"]:
        expiry_ts = t["expiry"]
        exp_dt = datetime.fromtimestamp(expiry_ts, IST)
        exp_str = exp_dt.strftime("%d-%m-%Y (%A) %I:%M %p")
        if expiry_ts > now:
            rem = format_remaining(expiry_ts)
            if str(t["id"]).startswith("-100"):
                active_temp.append(f"📢 `{t['id']}` → ⏳ {rem} (till {exp_str})")
            else:
                active_temp.append(f"👤 `{t['id']}` → ⏳ {rem} (till {exp_str})")

    if active_temp:
        text += "\n⏳ **Temporary Sudo:**\n" + "\n".join(active_temp)
    else:
        text += "\n⛔ No temporary sudo users."

    return text


async def auto_cleanup_loop():
    while True:
        db = load_db()
        now = datetime.now(IST).timestamp()
        db["temporary"] = [t for t in db["temporary"] if t["expiry"] > now]
        save_db(db)
        await asyncio.sleep(60)  # every 1 min cleanup
            
