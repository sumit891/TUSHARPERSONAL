import asyncio
from datetime import datetime, timedelta
import pytz
from motor.motor_asyncio import AsyncIOMotorClient

# ================= CONFIG =================
MONGO_URI = "mongodb+srv://tusharmongodbtxt16_db_user:SiaFZqFLpaXruqwr@cluster0.79oq0zc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "sample_mflix"
COLLECTION_NAME = "sudos"

IST = pytz.timezone("Asia/Kolkata")
# ==========================================

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
sudos = db[COLLECTION_NAME]

# Memory defaults
OWNER_ID = 6053889491
SUDO_USERS = [6053889491]
AUTH_CHANNELS = [-1003102889819, -1002663510614]

# -------- HELPERS ---------
def parse_multiple_durations(duration_str: str):
    days = hours = minutes = 0
    for p in duration_str.split():
        if p.endswith("d"): days += int(p[:-1])
        elif p.endswith("h"): hours += int(p[:-1])
        elif p.endswith("m"): minutes += int(p[:-1])
    return timedelta(days=days, hours=hours, minutes=minutes)

async def add_sudo(user_id: int, duration: timedelta = None):
    if duration is None:
        await sudos.update_one(
            {"id": user_id},
            {"$set": {"id": user_id, "permanent": True}},
            upsert=True
        )
    else:
        expiry = (datetime.now(IST) + duration).timestamp()
        await sudos.update_one(
            {"id": user_id},
            {"$set": {"id": user_id, "permanent": False, "expiry": expiry}},
            upsert=True
        )

async def remove_sudo(user_id: int):
    await sudos.delete_one({"id": user_id})

async def is_authorized(user_id: int = None, chat_id: int = None):
    # Memory check
    if user_id == OWNER_ID or user_id in SUDO_USERS:
        return True
    if chat_id in AUTH_CHANNELS:
        return True

    # Mongo check
    check_id = user_id or chat_id
    sudo = await sudos.find_one({"id": check_id})
    if not sudo: return False
    if sudo.get("permanent"): return True
    expiry = sudo.get("expiry", 0)
    return expiry > datetime.now(IST).timestamp()

def format_remaining(expiry_ts: float):
    now_ts = datetime.now(IST).timestamp()
    diff = int(expiry_ts - now_ts)
    if diff <= 0: return "❌ Expired"
    mins, sec = divmod(diff, 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    return f"{days}d {hrs}h {mins}m"

async def list_sudo():
    text = "📝 **Sudo List**\n\n"

    # Permanent sudo (merge memory + Mongo)
    all_perm = set(SUDO_USERS + AUTH_CHANNELS)
    async for s in sudos.find({"permanent": True}):
        all_perm.add(s["id"])

    if all_perm:
        text += "🔒 **Permanent Sudo:**\n"
        for uid in all_perm:
            if uid == OWNER_ID:
                text += f"👑 Owner → `{uid}`\n"
            elif str(uid).startswith("-100"):
                text += f"📢 Channel → `{uid}`\n"
            else:
                text += f"👤 User → `{uid}`\n"
    else:
        text += "🔒 No permanent sudo.\n"

    # Temporary sudo
    now = datetime.now(IST).timestamp()
    temp_list = []
    async for s in sudos.find({"permanent": False}):
        expiry = s.get("expiry", 0)
        if expiry <= now:  # expired
            continue
        exp_dt = datetime.fromtimestamp(expiry, IST)
        exp_str = exp_dt.strftime("%d-%m-%Y (%A) %I:%M %p")
        rem = format_remaining(expiry)
        if str(s["id"]).startswith("-100"):
            temp_list.append(f"📢 `{s['id']}` → ⏳ {rem} (till {exp_str})")
        else:
            temp_list.append(f"👤 `{s['id']}` → ⏳ {rem} (till {exp_str})")

    if temp_list:
        text += "\n⏳ **Temporary Sudo:**\n" + "\n".join(temp_list)
    else:
        text += "\n⛔ No temporary sudo users."

    return text

async def auto_cleanup_loop():
    while True:
        now = datetime.now(IST).timestamp()
        await sudos.delete_many({"permanent": False, "expiry": {"$lte": now}})
        await asyncio.sleep(60)
        
