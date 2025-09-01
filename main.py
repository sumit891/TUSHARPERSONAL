# Don't Remove Credit Tg - @Tushar0125
# Ask Doubt on telegram @Tushar0125

import os
import re
import sys
import json
import time
import m3u8
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import cloudscraper
import datetime
import random
import ffmpeg
import logging 
import yt_dlp 

from subprocess import getstatusoutput
from aiohttp import web
from core import *
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
import cloudscraper
import m3u8
import core as helper
from zoneinfo import ZoneInfo
from datetime import datetime
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

#pwimg = "https://graph.org/file/8add8d382169e326f67e0-3bf38f92e52955e977.jpg"
#ytimg = "https://graph.org/file/3aa806c302ceec62e6264-60ced740281395f68f.jpg"
cpimg = "https://graph.org/file/5ed50675df0faf833efef-e102210eb72c1d5a17.jpg"  
DEFAULT_QUOTE = "▭▬▭▬▭▬▭▬▭▬▭▬▭▭\n😊 हंसते रहो मुस्कुराते रहो और पढ़ाई करते रहो , reaction bhi de diya kro ताकि हमें भी अच्छा लगे .....❤️❤️\n▭▬▭▬▭▬▭▬▭▬▭▬▭▭"

async def show_random_emojis(message):
    emojis = ['🎊', '🔮', '😎', '⚡️', '🚀', '✨', '💥', '🎉', '🥂', '🍾', '🦠', '🤖', '❤️‍🔥', '🕊️', '💃', '🥳','🐅','🦁']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message
    

# Define the owner's user ID
OWNER_ID = 5840594311 # Replace with the actual owner's user ID

# List of sudo users (initially empty or pre-populated)
SUDO_USERS = [5840594311]

# ✅ Multiple AUTH CHANNELS allowed
AUTH_CHANNELS = [-1002605113558,-1002663510614]  # Add more channel IDs here

# Function to check if a user is authorized
def is_authorized(user_id: int) -> bool:
    return (
        user_id == OWNER_ID
        or user_id in SUDO_USERS
        or user_id in AUTH_CHANNELS  # ✅ Checks if user_id matches any channel ID
    )
    
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

# Sudo command to add/remove sudo users
@bot.on_message(filters.command("sudo"))
async def sudo_command(bot: Client, message: Message):
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.**")
        return

    try:
        args = message.text.split(" ", 2)
        if len(args) < 2:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
            return

        action = args[1].lower()
        target_user_id = int(args[2])

        if action == "add":
            if target_user_id not in SUDO_USERS:
                SUDO_USERS.append(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} added to sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is already in the sudo list.**")
        elif action == "remove":
            if target_user_id == OWNER_ID:
                await message.reply_text("**🚫 The owner cannot be removed from the sudo list.**")
            elif target_user_id in SUDO_USERS:
                SUDO_USERS.remove(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} removed from sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is not in the sudo list.**")
        else:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}")


# Start command handler
start_images = [
    "https://graph.org/file/996e7252ff3ffc679b3ea-ffc78c21ecf8396f98.jpg",
    "https://graph.org/file/439c62c6244b05050c93b-f02497c99181cdead5.jpg",
    "https://graph.org/file/b3ee971e4a341694e08bd-27795f759bb3275bd3.jpg",
    "https://graph.org/file/1050e771a23f79f5f5071-6622ca8eeb3464a28a.jpg",
]

def get_greeting_with_emoji():
    ist_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    hour = ist_time.hour

    if 0 <= hour < 12:  # 12:00 AM to 11:59 AM
        return "🌞 𝖦𝗈𝗈𝖽 𝖬𝗈𝗋𝗇𝗂𝗇𝗀"
    elif 12 <= hour < 17:  # 12:00 PM to 4:59 PM
        return "☀️ 𝖦𝗈𝗈𝖽 𝖠𝖿𝗍𝖾𝗋𝗇𝗈𝗈𝗇"
    elif 17 <= hour < 20:  # 5:00 PM to 7:59 PM
        return "🌇 𝖦𝗈𝗈𝖽 𝖤𝗏𝖾𝗇𝗂𝗇𝗀"
    else:  # 8:00 PM to 11:59 PM
        return "🌙 𝖦𝗈𝗈𝖽 𝖭𝗂𝗀𝗁𝗍"


@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m):
    img = random.choice(start_images)

    first_name = m.from_user.first_name or ""
    last_name = m.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip() or "User"
    clickable_name = f"[{full_name}](tg://user?id={m.from_user.id})"
    greeting = get_greeting_with_emoji()

    # ---------- Fast Butterfly/Confetti Animation ----------
    try:
        anim_msg = await m.reply_text("🦋✨🎉")
        confetti_emoji_sequences = ["🦋✨🎉", "🎉🦋✨", "✨🎉🦋", "🦋🎉✨", "🎆🦋✨", "🌈🦋✨"]
        last_text = None

        for _ in range(8):  # number of frames
            # select new text different from last
            new_text = random.choice([t for t in confetti_emoji_sequences if t != last_text])
            try:
                await anim_msg.edit(new_text)
                last_text = new_text
            except Exception as e:
                # ignore MESSAGE_NOT_MODIFIED errors
                if "MESSAGE_NOT_MODIFIED" not in str(e).upper():
                    print(f"Animation edit error: {e}")
            await asyncio.sleep(0.12)  # very fast flash

        await anim_msg.delete()  # remove animation after flash

    except Exception as e:
        print(f"Animation error: {e}")

    # ---------- Original Image & Caption Section ----------
    await bot.send_photo(
        chat_id=m.chat.id,
        photo=img,
        caption=(
            f"**{greeting} {clickable_name}**\n\n"
            "➠ **ɪ ᴀᴍ ᴛxᴛ ᴛᴏ ᴠɪᴅᴇᴏ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ.**\n"
            "➠ **ғᴏʀ ᴜsᴇ ᴍᴇ sᴇɴᴅ /upload.**\n"
            "➠ **ғᴏʀ ɢᴜɪᴅᴇ sᴇɴᴅ /help.**"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🇮🇳ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ🇮🇳", url="https://t.me/+dXRSrF1762o5NmRl")],
                [InlineKeyboardButton("🔔ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ🔔", url="https://t.me/+dXRSrF1762o5NmRl")],
                [InlineKeyboardButton("🦋ғᴏʟʟᴏᴡ ᴜs🦋", url="https://t.me/+dXRSrF1762o5NmRl")]
            ]
        ),
    )
    


# List users command
@bot.on_message(filters.command("sudolist") & filters.user(OWNER_ID))
async def list_users(client: Client, msg: Message):
    if SUDO_USERS:
        sudo_list = "\n".join([f"• `{user_id}`" for user_id in SUDO_USERS])
    else:
        sudo_list = "No sudo users found."

    if AUTH_CHANNELS:
        auth_list = "\n".join([f"• `{channel_id}`" for channel_id in AUTH_CHANNELS])
    else:
        auth_list = "No auth channels found."

    text = (
        f"**🔑 SUDO USERS :**\n{sudo_list}\n\n"
        f"**📢 AUTH CHANNELS :**\n{auth_list}"
    )
    await msg.reply_text(text)


# Stop command handler
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m: Message):
    await m.reply_text("**🛑 𝗦𝘁𝗼𝗽𝗽𝗲𝗱 🛑**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
    
# Restart Bot
@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not is_authorized(m.from_user.id):
        await m.reply_text("**🚫 You are not authorized to use this command.**")
        return
    await m.reply_text("🔮Restarted🔮", True)
    os.execl(sys.executable, sys.executable, *sys.argv)



COOKIES_FILE_PATH = "youtube_cookies.txt"
# helper function to validate cookies
async def validate_cookies():
    test_url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
    cmd = ["yt-dlp", "--cookies", COOKIES_FILE_PATH, "-F", test_url]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    output = stdout.decode() + stderr.decode()

    if "HTTP Error 403" in output or "Login required" in output or "cookies" in output.lower():
        return False
    return True

# Cookies upload & validation check command
@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    if not is_authorized(m.from_user.id):
        return await m.reply_text("🚫 You are not authorized to use this command.")

    # delete command msg
    try: await m.delete()
    except: pass

    prompt = await m.reply_text("**📂 Please upload the cookies file in txt format**")

    try:
        input_message: Message = await client.listen(m.chat.id)

        # delete prompt + file msg
        try: await prompt.delete()
        except: pass
        try: await input_message.delete()
        except: pass

        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            return await m.reply_text("**❌ Invalid file. Please upload a .txt file.**")

        # download file
        downloaded_path = await input_message.download()
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()
        with open(COOKIES_FILE_PATH, "w") as target_file:
            target_file.write(cookies_content)
        os.remove(downloaded_path)

        # countdown msg
        status_msg = await m.reply_text("**⏳ Validating cookies... (00:00 elapsed)**")

        start_time = asyncio.get_event_loop().time()

        async def countdown(done_event):
            sec = 0
            while not done_event.is_set():
                mm, ss = divmod(sec, 60)
                try:
                    await status_msg.edit_text(
                        f"**⏳ Validating cookies... ({mm:02d}:{ss:02d} elapsed)**"
                    )
                except:
                    pass
                await asyncio.sleep(1)
                sec += 1

        # run countdown + validation in parallel
        done_event = asyncio.Event()
        task_countdown = asyncio.create_task(countdown(done_event))
        is_valid = await validate_cookies()
        done_event.set()
        await asyncio.sleep(0.5)
        task_countdown.cancel()

        # calculate elapsed time
        elapsed = int(asyncio.get_event_loop().time() - start_time)
        mm, ss = divmod(elapsed, 60)
        elapsed_str = f"{mm:02d}:{ss:02d}"

        if not is_valid:
            os.remove(COOKIES_FILE_PATH)
            result = await status_msg.edit_text(
                f"**❌ Cookies Expired / Invalid 🚫**\n\n"
                f"**⚠️ Old cookies file has been deleted.**\n"
                f"**🕒 Checked in {elapsed_str}**"
            )
        else:
            result = await status_msg.edit_text(
                f"**✅ Cookies Updated & Valid 🎉**\n"
                f"**📂 Saved in {COOKIES_FILE_PATH}**\n"
                f"**🕒 Checked in {elapsed_str}**"
            )

        # 🔥 Auto delete final message after 20 sec
        await asyncio.sleep(20)
        try: await result.delete()
        except: pass

    except Exception as e:
        await m.reply_text(f"**⚠️ Error while updating cookies: {str(e)}**")
                

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'


# Edit txt file
@bot.on_message(filters.command('e2t'))
async def edit_txt(client, message: Message):
    

    # Prompt the user to upload the .txt file
    await message.reply_text(
        "🎉 **Welcome to the .txt File Editor**\n\n"
        "**Please send your `.txt` file containing subjects, links, and topics.**"
    )

    # Wait for the user to upload the file
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.document:
        await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
        return

    # Get the file name
    file_name = input_message.document.file_name.lower()

    # Define the path where the file will be saved
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Download the file
    uploaded_file = await input_message.download(uploaded_file_path)

    # After uploading the file, prompt the user for the file name or 'd' for default
    await message.reply_text(
        "🔄 **Send your .txt file name, or type 'd' for the default file name.**"
    )

    # Wait for the user's response
    user_response: Message = await bot.listen(message.chat.id)
    if user_response.text:
        user_response_text = user_response.text.strip().lower()
        if user_response_text == 'd':
            # Handle default file name logic (e.g., use the original file name)
            final_file_name = file_name
        else:
            final_file_name = user_response_text + '.txt'
    else:
        final_file_name = file_name  # Default to the uploaded file name

    # Read and process the uploaded file
    try:
        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to read the file.\n\nDetails: {e}")
        return

    # Parse the content into subjects with links and topics
    subjects = {}
    current_subject = None
    for line in content:
        line = line.strip()
        if line and ":" in line:
            # Split the line by the first ":" to separate title and URL
            title, url = line.split(":", 1)
            title, url = title.strip(), url.strip()

            # Add the title and URL to the dictionary
            if title in subjects:
                subjects[title]["links"].append(url)
            else:
                subjects[title] = {"links": [url], "topics": []}

            # Set the current subject
            current_subject = title
        elif line.startswith("-") and current_subject:
            # Add topics under the current subject
            subjects[current_subject]["topics"].append(line.strip("- ").strip())

    # Sort the subjects alphabetically and topics within each subject
    sorted_subjects = sorted(subjects.items())
    for title, data in sorted_subjects:
        data["topics"].sort()

    # Save the edited file to the defined path with the final file name
    try:
        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                # Write title and its links
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                # Write topics under the title
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to write the edited file.\n\nDetails: {e}")
        return

    # Send the sorted and edited file back to the user
    try:
        await message.reply_document(
            document=final_file_path,
            caption="📥**𝗘𝗱𝗶𝘁𝗲𝗱 𝗕𝘆 ➤ 𝗧𝘂𝘀𝗵𝗮𝗿**"
        )
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to send the file.\n\nDetails: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

from pytube import Playlist
import youtube_dl

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Utility Functions ---

def sanitize_filename(name):
    """
    Sanitizes a string to create a valid filename.
    """
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def get_videos_with_ytdlp(url):
    """
    Retrieves video titles and URLs using `yt-dlp`.
    If a title is not available, only the URL is saved.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                title = result.get('title', 'Unknown Title')
                videos = {}
                for entry in result['entries']:
                    video_url = entry.get('url', None)
                    video_title = entry.get('title', None)
                    if video_url:
                        videos[video_title if video_title else "Unknown Title"] = video_url
                return title, videos
            return None, None
    except Exception as e:
        logging.error(f"Error retrieving videos: {e}")
        return None, None

def save_to_file(videos, name):
    """
    Saves video titles and URLs to a .txt file.
    If a title is unavailable, only the URL is saved.
    """
    filename = f"{sanitize_filename(name)}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for title, url in videos.items():
            if title == "Unknown Title":
                file.write(f"{url}\n")
            else:
                file.write(f"{title}: {url}\n")
    return filename

# --- Bot Command ---

@bot.on_message(filters.command('yt2txt'))
async def ytplaylist_to_txt(client: Client, message: Message):
    """
    Handles the extraction of YouTube playlist/channel videos and sends a .txt file.
    """
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.\n\n🫠 This Command is only for owner.**")
        return

    # Request YouTube URL
    await message.delete()
    editable = await message.reply_text("📥 **𝖯𝗅𝖾𝖺𝗌𝖾 𝖾𝗇𝗍𝖾𝗋 𝗍𝗁𝖾 𝖸𝗈𝗎𝗍𝗎𝖻𝖾 𝖯𝗅𝖺𝗒𝗅𝗂𝗌𝗍 𝖴𝗋𝗅 : **")
    input_msg = await client.listen(editable.chat.id)
    youtube_url = input_msg.text
    await input_msg.delete()
    await editable.delete()

    # Process the URL
    title, videos = get_videos_with_ytdlp(youtube_url)
    if videos:
        file_name = save_to_file(videos, title)
        await message.reply_document(
            document=file_name, 
            caption=f"`{title}`\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤ 𝗧𝘂𝘀𝗵𝗮𝗿"
        )
        os.remove(file_name)
    else:
        await message.reply_text("⚠️ **Unable to retrieve videos. Please check the URL.**")



# Filter Pdf Url From txt 
@bot.on_message(filters.command("gpd") & filters.private)
async def gpd_command(bot: Client, m: Message):
    try:
        # Delete command message instantly
        await m.delete()

        # Ask user for txt file
        prompt = await m.reply_text("**📂 Please send me a txt file.**")
                     
        # Wait for user to upload the .txt file
        file_msg = await bot.listen(m.chat.id)

        # Delete the prompt
        await prompt.delete()

        # Check file type
        if not file_msg.document or not file_msg.document.file_name.endswith(".txt"):
            await m.reply_text("❌ Invalid file. Please send a `.txt` file.")
            return

        # Download uploaded .txt
        file_path = await file_msg.download()
        original_name = os.path.splitext(file_msg.document.file_name)[0]  # remove .txt

        # Delete the user's original txt message from chat
        await file_msg.delete()

        # Read and filter only PDF links
        pdf_links = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if re.search(r"pdf", line, re.IGNORECASE):  # pick if "pdf" appears
                    pdf_links.append(line)

        # Remove the uploaded file from server
        os.remove(file_path)

        if not pdf_links:
            await m.reply_text("**⚠️ No PDF links found in the file.**")
            return

        # Save filtered links to a new .txt file
        output_file = f"{original_name}.txt"
        with open(output_file, "w", encoding="utf-8") as out:
            for link in pdf_links:
                out.write(f"{link}\n")

        # Send back the new .txt file
        await m.reply_document(output_file, caption="📑 Extracted PDF links.")

        # Cleanup final file also (so it won’t stay on server)
        os.remove(output_file)

    except Exception as e:
        await m.reply_text(f"⚠️ Error: {str(e)}")
        
# Get IDs
@bot.on_message(filters.command("id"))
async def id_command(client, message):
    # Safe delete command message
    try:
        await message.delete()
    except:
        pass

    chat_id = message.chat.id
    countdown = 17  # seconds
    flash_emojis = ["🎊","🌟","💫","🔥","🎉","🌈","💥"]

    # Initial message
    msg = await message.reply_text(f"`The ID of this chat is:`\n`{chat_id}`\n\n⏳ Auto delete in {countdown} seconds")

    # Live countdown with flashing emojis
    for i in range(countdown - 1, 0, -1):
        await asyncio.sleep(1)
        try:
            emoji = random.choice(flash_emojis)
            await msg.edit_text(f"{emoji} `The ID of this chat is:` `{chat_id}` {emoji}\n\n⏳ Auto delete in {i} seconds")
        except:
            break

    # Final delete after countdown
    try:
        await msg.delete()
    except:
        pass
        

# Set your custom auto-delete time in seconds for help text 
AUTO_DELETE_TIME = 15  # Aap isse change kar sakte ho

# Help command
@bot.on_message(filters.command("help"))
async def help_command(client: Client, msg):
    help_text = (
        "`/start` - Start the bot⚡\n\n"
        "`/upload` - Download and upload files (sudo)🎬\n\n"
        "`/restart` - Restart the bot🔮\n\n"
        "`/stop` - Stop ongoing process🛑\n\n"
        "`/id` - Get Id🆔\n\n"
        "`/t2t` - Create .txt file of any text📜\n\n"
        " `/gpd` - Filter pdf url and make txt file from txt file🗃️\n\n"
        "`/cookies` - Upload cookies file🍪\n\n"
        "`/e2t` - Edit txt file📝\n\n"
        "`/yt2txt` - Create txt of yt playlist (owner)🗃️\n\n"
        "`/sudo add` - Add user or group or channel (owner)🎊\n\n"
        "`/sudo remove` - Remove user or group or channel (owner)❌\n\n"
        "`/sudolist` - List of sudo user or group or channel📜\n\n"
    )

    # Delete user's /help command immediately
    await msg.delete()
    
    # Send help message with initial countdown
    sent_msg = await msg.reply_text(help_text + f"\n⏳ Self-destruct in {AUTO_DELETE_TIME} seconds")

    # Countdown loop with colorful emojis
    for i in range(AUTO_DELETE_TIME, 0, -1):
        # Choose emoji based on remaining time
        if i > AUTO_DELETE_TIME * 0.6:
            countdown_emoji = "🟢"
        elif i > AUTO_DELETE_TIME * 0.3:
            countdown_emoji = "🟡"
        else:
            countdown_emoji = "🔴"
        
        await sent_msg.edit_text(help_text + f"\n{countdown_emoji} Self-destruct in {i} seconds ⏳")
        await asyncio.sleep(1)

    # Delete the help message
    await sent_msg.delete()
    

# Create.txt file of any text
@bot.on_message(filters.command("t2t") & filters.private)
async def t2t_command(_, message: Message):
    await message.reply(
        "✏️ 𝖲𝖾𝗇𝖽 𝗍𝗁𝖾 𝗍𝖾𝗑𝗍 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗌𝖺𝗏𝖾 𝖺𝗌 𝖺 `.txt` 𝖿𝗂𝗅𝖾.\n",
        quote=True
    )

    # Listen for next message (multi-line support)
    text_msg: Message = await bot.listen(message.chat.id)
    content = text_msg.text

    await text_msg.reply(
        "𝖲𝖾𝗇𝖽 𝖺 𝖿𝗂𝗅𝖾 𝗇𝖺𝗆𝖾.\n",
        quote=True
    )

    filename_msg: Message = await bot.listen(message.chat.id)
    filename = filename_msg.text.strip()

    if not filename:
        filename = "file.txt"
    if not filename.lower().endswith(".txt"):
        filename += ".txt"

    # Sanitize filename (replace invalid characters)
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Save text in current directory
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    # Send the file
    await filename_msg.reply_document(
        document=filename,
        caption=f"`{filename}`",
        quote=True
    )
    
# Upload command handler
@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    if not is_authorized(m.chat.id):
        await m.reply_text("**🚫You are not authorized to use this bot.**")
        return

    editable = await m.reply_text(f"⚡𝗦𝗘𝗡𝗗 𝗧𝗫𝗧 𝗙𝗜𝗟𝗘⚡")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    pdf_count = 0
    img_count = 0
    zip_count = 0
    video_count = 0
    
    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        
        links = []
        for i in content:
            if "://" in i:
                url = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif ".zip" in url:
                    zip_count += 1
                else:
                    video_count += 1
        os.remove(x)
    except:
        await m.reply_text("😶𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗶𝗹𝗲 𝗜𝗻𝗽𝘂𝘁😶")
        os.remove(x)
        return
   
    await editable.edit(f"`𝗧𝗼𝘁𝗮𝗹 🔗 𝗟𝗶𝗻𝗸𝘀 𝗙𝗼𝘂𝗻𝗱 𝗔𝗿𝗲 {len(links)}\n\n🔹Img : {img_count}  🔹Pdf : {pdf_count}\n🔹Zip : {zip_count}  🔹Video : {video_count}\n\n𝗦𝗲𝗻𝗱 𝗙𝗿𝗼𝗺 𝗪𝗵𝗲𝗿𝗲 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁 𝗧𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱.`")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
    await editable.edit("📚 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 📚\n\n🦠 𝗦𝗲𝗻𝗱 `1` 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗗𝗲𝗳𝗮𝘂𝗹𝘁 🦠")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == '1':
        b_name = file_name
    else:
        b_name = raw_text0
    

    await editable.edit("**📸 𝗘𝗻𝘁𝗲𝗿 𝗥𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 📸**\n➤ `144`\n➤ `240`\n➤ `360`\n➤ `480`\n➤ `720`\n➤ `1080`")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("📛 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗡𝗮𝗺𝗲 📛\n\n🐥 𝗦𝗲𝗻𝗱 `1` 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗗𝗲𝗳𝗮𝘂𝗹𝘁 🐥")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    # Default credit message with link
    credit = "️@Zindagii123 @Aim_Aiims143"
    if raw_text3 == '1':
        CR = '@Zindagii123 @Aim_Aiims143'
    elif raw_text3:
        try:
            text, link = raw_text3.split(',')
            CR = f'[{text.strip()}]({link.strip()})'
        except ValueError:
            CR = raw_text3  # In case the input is not in the expected format, use the raw text
    else:
        CR = credit
    
   
    await editable.edit("**𝗘𝗻𝘁𝗲𝗿 𝗣𝘄 𝗧𝗼𝗸𝗲𝗻 𝗙𝗼𝗿 𝗣𝘄 𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗼𝗿 𝗦𝗲𝗻𝗱 `3` 𝗙𝗼𝗿 𝗢𝘁𝗵𝗲𝗿𝘀**")
    input4: Message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text
    await input4.delete(True)
    if raw_text4 == 3:
        MR = token
    else:
        MR = raw_text4


    await editable.edit("𝗘𝗻𝘁𝗲𝗿 𝗤𝘂𝗼𝘁𝗲 𝗢𝗽𝘁𝗶𝗼𝗻 :\n\n`1` → 𝗦𝗲𝘁 𝗱𝗲𝗳𝗮𝘂𝗹𝘁 𝗾𝘂𝗼𝘁𝗲\n`0` → 𝗦𝗸𝗶𝗽 𝗾𝘂𝗼𝘁𝗲\n𝗔𝗻𝘆𝘁𝗵𝗶𝗻𝗴 → 𝗨𝘀𝗲 𝗮𝘀 𝗰𝘂𝘀𝘁𝗼𝗺 𝗾𝘂𝗼𝘁𝗲")
    input5: Message = await bot.listen(editable.chat.id)
    raw_text5 = input5.text.strip()
    await input5.delete(True)
    if raw_text5 == "1":  # Default quote
        QUOTE = f"**{DEFAULT_QUOTE}**"
    elif raw_text5 == "0":  # Skip quote
        QUOTE = None
    else:  # User provided custom quote
        QUOTE = f"**{raw_text5}**"

    
    await editable.edit("𝗡𝗼𝘄 𝗦𝗲𝗻𝗱 𝗧𝗵𝗲 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗜𝗺𝗮𝗴𝗲\n\n𝗢𝗿 𝗜𝗳 𝗗𝗼𝗻'𝘁 𝗪𝗮𝗻𝘁 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗦𝗲𝗻𝗱 = 𝗻𝗼")
    input6 = message = await bot.listen(editable.chat.id)
    #raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = None

   # Case 1: User types 'no' to skip
    if input6.text and input6.text.lower() == "no":
        thumb = "no"

  # Case 2: User sends a URL
    elif input6.text and (input6.text.startswith("http://") or input6.text.startswith("https://")):
        from subprocess import getstatusoutput
        status, output = getstatusoutput(f"wget '{input6.text}' -O 'thumb.jpg'")
        if status == 0:
            thumb = "thumb.jpg"
        else:
            thumb = "no"  # agar URL download fail ho jaye to skip

  # Case 3: User uploads an image
    elif input6.media:
        thumb_file = await bot.download_media(input6, file_name="thumb.jpg")
        thumb = thumb_file

  # Fallback: agar user kuch bhi valid nahi bheje
    else:
        thumb = "no"
    
    failed_count =0
    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                        
            elif 'media-cdn.classplusapp.com/drm/' in url:
                url = f"https://dragoapi.vercel.app/video/{url}"

            elif 'videos.classplusapp' in url:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "media-cdn.classplusapp" in url:
             headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
             params = (('url', f'{url}'),)
             response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
             url = response.json()['url']

            elif "https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/" in url:
                url = url.replace("https://appx-transcoded-videos.livelearn.in/videos/rozgar-data/", "")
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                
            elif "https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/" in url:
                url = url.replace("https://appx-transcoded-videos-mcdn.akamai.net.in/videos/bhainskipathshala-data/", "")
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "apps-s3-jw-prod.utkarshapp.com" in url:
                if 'enc_plain_mp4' in url:
                    url = url.replace(url.split("/")[-1], res+'.mp4')
                    
                elif 'Key-Pair-Id' in url:
                    url = None
                    
                elif '.m3u8' in url:
                    q = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).split("/")[0]
                    x = url.split("/")[5]
                    x = url.replace(x, "")
                    url = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).replace(q+"/", x)
            #elif '/master.mpd' in url:
             #id =  url.split("/")[-2]
             #url = f"https://player.muftukmall.site/?id={id}"
            elif "/master.mpd" in url or "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
             id =  url.split("/")[-2]
             #url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={raw_text4}"
             url = f"https://anonymouspwplayer-0e5a3f512dec.herokuapp.com/pw?url={url}&token={raw_text4}"
             #url = f"https://madxabhi-pw.onrender.com/{id}/master.m3u8?token={raw_text4}"
            #elif '/master.mpd' in url:
             #id =  url.split("/")[-2]
             #url = f"https://dl.alphacbse.site/download/{id}/master.m3u8"
            
        
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            #if 'cpvod.testbook' in url:
                #CPVOD = url.split("/")[-2]
                #url = requests.get(f'https://extractbot.onrender.com/classplus?link=https://cpvod.testbook.com/{CPVOD}/playlist.m3u8', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']
            
            #if 'cpvod.testbook' in url:
               #url = requests.get(f'https://mon-key-3612a8154345.herokuapp.com/get_keys?url=https://cpvod.testbook.com/{CPVOD}/playlist.m3u8', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'}).json()['url']
           
           
            if 'khansirvod4.pc.cdn.bitgravity.com' in url:               
               parts = url.split('/')               
               part1 = parts[1]
               part2 = parts[2]
               part3 = parts[3] 
               part4 = parts[4]
               part5 = parts[5]
               
               print(f"PART1: {part1}")
               print(f"PART2: {part2}")
               print(f"PART3: {part3}")
               print(f"PART4: {part4}")
               print(f"PART5: {part5}")
               url = f"https://kgs-v4.akamaized.net/kgs-cv/{part3}/{part4}/{part5}"
           
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
          
            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzUxMzUzNjIsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiYmt3cmVIWmxZMFUwVXpkSmJYUkxVemw2ZW5Oclp6MDkiLCJmaXJzdF9uYW1lIjoiY25GdVpVdG5kRzR4U25sWVNGTjRiVW94VFhaUVVUMDkiLCJlbWFpbCI6ImFFWllPRXhKYVc1NWQyTlFTazk0YmtWWWJISTNRM3BKZW1OUVdIWXJWWE0wWldFNVIzZFNLelE0ZHowPSIsInBob25lIjoiZFhSNlFrSm9XVlpCYkN0clRUWTFOR3REU3pKTVVUMDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJhVVZGZGpBMk9XSnhlbXRZWm14amF6TTBVazQxUVQwOSIsImRldmljZV90eXBlIjoid2ViIiwiZGV2aWNlX3ZlcnNpb24iOiJDaHJvbWUrMTE5IiwiZGV2aWNlX21vZGVsIjoiY2hyb21lIiwicmVtb3RlX2FkZHIiOiIyNDA5OjQwYzI6MjA1NTo5MGQ0OjYzYmM6YTNjOTozMzBiOmIxOTkifX0.Kifitj1wCe_ohkdclvUt7WGuVBsQFiz7eezXoF1RduDJi4X7egejZlLZ0GCZmEKBwQpMJLvrdbAFIRniZoeAxL4FZ-pqIoYhH3PgZU6gWzKz5pdOCWfifnIzT5b3rzhDuG7sstfNiuNk9f-HMBievswEIPUC_ElazXdZPPt1gQqP7TmVg2Hjj6-JBcG7YPSqa6CUoXNDHpjWxK_KREnjWLM7vQ6J3vF1b7z_S3_CFti167C6UK5qb_turLnOUQzWzcwEaPGB3WXO0DAri6651WF33vzuzeclrcaQcMjum8n7VQ0Cl3fqypjaWD30btHQsu5j8j3pySWUlbyPVDOk-g'
                url = url.split("bcov_auth")[0]+bcov
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            
            elif "webvideos.classplusapp." in url:
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
          
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'
          
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
                
                
           #Function to append quote after Extracted By
            def append_quote(template: str, quote: str):
                if quote:
                    return template + f"\n\n{quote}"
                return template
               
            try:  
                cc = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).𝔗𝔲𝔰𝔥𝔞𝔯.mkv\n\n📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                #cpw = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).𝔗𝔲𝔰𝔥𝔞𝔯.mkv\n\n\n🔗𝗩𝗶𝗱𝗲𝗼 𝗨𝗿𝗹 ➤ <a href="{url}">__Click Here to Watch Video__</a>\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                #cyt = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).𝔗𝔲𝔰𝔥𝔞𝔯.mp4\n\n\n🔗𝗩𝗶𝗱𝗲𝗼 𝗨𝗿𝗹 ➤ <a href="{url}">__Click Here to Watch Video__</a>\n\n\n<pre><code>📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}</code></pre>\n\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                cpvod = f'**[🎬] 𝗩𝗶𝗱_𝗜𝗱 : {str(count).zfill(3)}.\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.({res}).𝔗𝔲𝔰𝔥𝔞𝔯.mkv\n\n🔗𝗩𝗶𝗱𝗲𝗼 𝗨𝗿𝗹 ➤ <a href="{url}">__Click Here to Watch Video__</a>\n\n📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                cimg = f'**[📁] 𝗜𝗺𝗴_𝗜𝗱 : {str(count).zfill(3)}.\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.𝔗𝔲𝔰𝔥𝔞𝔯.jpg\n\n📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                cczip = f'**[📁] 𝗣𝗱𝗳_𝗜𝗱 : {str(count).zfill(3)}.\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.𝔗𝔲𝔰𝔥𝔞𝔯.zip\n\n📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'
                cc1 = f'**[📁] 𝗣𝗱𝗳_𝗜𝗱 : {str(count).zfill(3)}.\n\n☘️𝗧𝗶𝘁𝗹𝗲 𝗡𝗮𝗺𝗲 ➤ {name1}.𝔗𝔲𝔰𝔥𝔞𝔯.pdf\n\n📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 ➤ {b_name}\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤  {CR}**'

                cc = append_quote(cc, QUOTE)
                cpvod = append_quote(cpvod, QUOTE)
                cimg = append_quote(cimg, QUOTE)
                cczip = append_quote(cczip, QUOTE)
                cc1 = append_quote(cc1, QUOTE)
    
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                        
                #elif "muftukmall" in url:
                    #try:
                        #await bot.send_photo(chat_id=m.chat.id, photo=pwimg, caption=cpw)
                        #count +=1
                    #except Exception as e:
                        #await m.reply_text(str(e))    
                        #time.sleep(1)    
                        #continue
                
                #elif "youtu" in url:
                    #try:
                        #await bot.send_photo(chat_id=m.chat.id, photo=ytimg, caption=cyt)
                        #count +=1
                    #except Exception as e:
                        #await m.reply_text(str(e))    
                        #time.sleep(1)    
                        #continue

                elif "media-cdn.classplusapp.com/drm/" in url:
                    try:
                        await bot.send_photo(chat_id=m.chat.id, photo=cpimg, caption=cpvod)
                        count +=1
                    except Exception as e:
                        await m.reply_text(str(e))    
                        time.sleep(1)    
                        continue          
                        
                
                elif any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        await asyncio.sleep(4)  # Use asyncio.sleep for non-blocking sleep
                        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")

                        # Create a cloudscraper session for image download
                        scraper = cloudscraper.create_scraper()

                        # Send a GET request to download the image
                        response = scraper.get(url)

                        # Check if the response status is OK
                        if response.status_code == 200:
                            # Write the image content to a file
                            with open(f'{name}.jpg', 'wb') as file:  # Save as JPG (or PNG if you want)
                                file.write(response.content)

                            # Send the image document
                            await asyncio.sleep(2)  # Non-blocking sleep
                            copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.jpg', caption=cimg)
                            count += 1

                            # Remove the image file after sending
                            os.remove(f'{name}.jpg')

                        else:
                            await m.reply_text(f"Failed to download Image: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        await asyncio.sleep(2)  # Use asyncio.sleep for non-blocking sleep
                        return  # Exit the function to avoid continuation  
                    
                    except Exception as e:
                        await m.reply_text(f"An error occurred: {str(e)}")
                        await asyncio.sleep(4)  # You can replace this with more specific 
                        
                elif ".zip" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.zip" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.zip', caption=cczip)
                        count += 1
                        os.remove(f'{name}.zip')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        count += 1
                        continue
                        
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    emoji_message = await show_random_emojis(message)
                    remaining_links = len(links) - count
                    Show = f"**🍁 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗜𝗡𝗚 🍁**\n\n**📝ɴᴀᴍᴇ » ** `{name}\n\n🔗ᴛᴏᴛᴀʟ ᴜʀʟ » {len(links)}\n\n🎬ᴠɪᴅᴇᴏ » {video_count}\n\n📁ᴘᴅғ » {pdf_count}\n\n📑ɪɴᴅᴇx » {str(count)}/{len(links)}\n\n🌐ʀᴇᴍᴀɪɴɪɴɢ ᴜʀʟ » {remaining_links}\n\n❄ǫᴜᴀʟɪᴛʏ » {res}`\n\n**🔗ᴜʀʟ » ** `Not Defined`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await emoji_message.delete()
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(f'‼️𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗙𝗮𝗶𝗹𝗲𝗱‼️\n\n'
                                   f'📝𝗡𝗮𝗺𝗲 » `{name}`\n\n'
                                   f'🔗𝗨𝗿𝗹 » <a href="{url}">__**Click Here to See Link**__</a>`')
                                   
                count += 1
                failed_count += 1
                continue   
                

    except Exception as e:
        await m.reply_text(e)
    #await m.reply_text("**🥳𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗗𝗼𝗻𝗲🥳**")
    await m.reply_text(f"`✨𝗕𝗔𝗧𝗖𝗛 𝗦𝗨𝗠𝗠𝗔𝗥𝗬✨\n\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"📚𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 » {b_name}\n\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"✨𝗧𝗫𝗧 𝗦𝗨𝗠𝗠𝗔𝗥𝗬✨ : {len(links)}\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"🔹𝗩𝗶𝗱𝗲𝗼 » {video_count}\n🔹𝗣𝗱𝗳 » {pdf_count}\n🔹𝗜𝗺𝗴 » {img_count}\n🔹𝗙𝗮𝗶𝗹𝗲𝗱 𝗨𝗿𝗹 » {failed_count}\n\n"
                       f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                       f"✅𝗦𝗧𝗔𝗧𝗨𝗦 » 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗`")
    await m.reply_text(f"⚡𝗥𝗲𝗮𝗰𝘁𝗶𝗼𝗻 𝗗𝗲 𝗗𝗶𝘆𝗮 𝗞𝗮𝗿𝗼 𝗧𝗮𝗸𝗶 𝗠𝘂𝗷𝗵𝗲 𝗕𝗵𝗶 𝗟𝗲𝗰𝘁𝘂𝗿𝗲 𝗨𝗽𝗹𝗼𝗮𝗱 𝗞𝗮𝗿𝗻𝗲 𝗠𝗲 𝗠𝗮𝗷𝗮 𝗔𝘆𝗲🤩😊")                 
       


if __name__ == "__main__":
    #bot.loop.create_task(auto_cleanup_loop())  # sudox.py ka loop run karega
    bot.run()
