import os
import subprocess
from datetime import datetime
from pytz import timezone
from pyrogram import Client, filters
from pyrogram.types import Message

def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if ":" in line:
            name, url = line.split(":", 1)
            data.append((name.strip(), url.strip()))
    return data

def categorize_urls(urls, your_working_token="YOUR_TOKEN_HERE"):
    videos, pdfs, others = [], [], []
    for name, url in urls:
        new_url = url
        if "akamaized.net/" in url or "1942403233.rsc.cdn77.org/" in url:
            new_url = f"https://www.khanglobalstudies.com/player?src={url}"
            videos.append((name, new_url))
        elif "d1d34p8vz63oiq.cloudfront.net/" in url:
            new_url = f"https://anonymouspwplayer-0e5a3f512dec.herokuapp.com/pw?url={url}&token={your_working_token}"
            videos.append((name, new_url))
        elif "youtube.com/embed" in url:
            yt_id = url.split("/")[-1]
            new_url = f"https://www.youtube.com/watch?v={yt_id}"
            videos.append((name, new_url))
        elif ".m3u8" in url or ".mp4" in url:
            videos.append((name, url))
        elif "pdf" in url.lower():
            pdfs.append((name, url))
        else:
            others.append((name, url))
    return videos, pdfs, others

def generate_html(file_name, videos, pdfs, others):
    file_name_no_ext = os.path.splitext(file_name)[0]
    ist = timezone('Asia/Kolkata')
    creation_date = datetime.now(ist).strftime("%d %b %Y, %I:%M %p")

    video_links = "".join(f'<div class="card"><a href="#" onclick="playVideo(\'{url}\')">{name}</a></div>' for name, url in videos)
    pdf_links = "".join(f'<div class="card"><a href="{url}" target="_blank">{name}</a></div>' for name, url in pdfs)
    other_links = "".join(f'<div class="card"><a href="{url}" target="_blank">{name}</a></div>' for name, url in others)

    html_template = fr"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{file_name_no_ext}</title>
<link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
<style>
:root {{--blue:#007bff;--gray:#d3d3d3;--dark-bg:#121212;--dark-text:#eee;--yellow:#ffeb3b;}}
body.light {{background:#f5f7fa;color:#333;}}
body.dark {{background:#121212;color:#eee;}}
body {{margin:0;font-family:'Poppins',sans-serif;transition:0.3s;}}
.welcome-container {{display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;text-align:center;}}
.welcome-box {{background:#000;color:white;padding:25px;border-radius:12px;box-shadow:0 4px 8px rgba(0,0,0,0.3);margin-bottom:20px;}}
.welcome-box p {{color:yellow;font-weight:bold;margin:5px 0;}}
.enter-btn {{background:red;color:white;padding:12px 25px;border:none;border-radius:10px;font-weight:bold;cursor:pointer;font-size:16px;transition:0.3s;}}
.enter-btn:hover {{background:darkred;}}
#themeToggle {{cursor:pointer;margin:10px auto;display:block;padding:8px 15px;background:var(--blue);color:white;border:none;border-radius:10px;font-weight:bold;}}
#themeToggle:hover {{background:#0056b3;}}
#video-section {{display:none;}}
.video-header {{text-align:center;padding:20px;background:#1c1c1c;color:white;border-radius:12px;margin-bottom:15px;}}
.video-header p {{color:var(--yellow);font-weight:bold;}}
.counts {{text-align:center;font-weight:bold;color:#007bff;margin-bottom:20px;}}
#video-player {{margin:0 auto;max-width:850px;border-radius:12px;overflow:hidden;transition:0.3s;}}
#open-youtube-btn {{display:none;margin:10px auto;text-align:center;color:#ff0000;font-weight:bold;text-decoration:none;transition:0.3s;}}
#open-youtube-btn:hover {{color:#ff6b6b;}}
.search-bar {{text-align:center;margin:20px auto;}}
.search-bar input {{width:90%;max-width:650px;padding:12px 20px;border-radius:25px;border:2px solid var(--blue);font-size:16px;outline:none;}}
.search-bar input:focus {{border-color:#0056b3;box-shadow:0 0 8px rgba(0,123,255,0.3);}}
.tabs {{display:flex;justify-content:center;margin:25px 0;gap:15px;flex-wrap:wrap;}}
.tab {{padding:12px 30px;background:linear-gradient(135deg,#00b4db,#0083b0);color:white;border-radius:15px;cursor:pointer;font-weight:bold;box-shadow:0 4px 8px rgba(0,0,0,0.15);}}
.tab.active {{transform:scale(1.05);box-shadow:0 6px 12px rgba(0,0,0,0.25);}}
.content {{display:none;width:90%;max-width:850px;margin:0 auto;}}
.card {{margin:10px 0;padding:15px 18px;border-radius:10px;box-shadow:0 3px 6px rgba(0,0,0,0.1);}}
.card a {{text-decoration:none;font-weight:bold;}}
.footer {{text-align:center;padding:18px;background:#1c1c1c;color:yellow;font-weight:bold;margin-top:30px;border-radius:12px;}}
.back-btn, .settings-btn {{display:none;margin:10px auto;padding:8px 15px;background:#ff5722;color:white;border:none;border-radius:10px;font-weight:bold;cursor:pointer;}}
.back-btn:hover, .settings-btn:hover {{background:#e64a19;}}
.settings-panel {{display:none;text-align:center;margin:15px;}}
.settings-panel button {{margin:5px;padding:8px 15px;border:none;border-radius:8px;background:#007bff;color:white;font-weight:bold;cursor:pointer;}}
.settings-panel button:hover {{background:#0056b3;}}
</style>
</head>
<body class="light">

<div class="welcome-container" id="welcome-page">
    <div class="welcome-box">
        <h2>{file_name_no_ext}</h2>
        <p><b>📥 Created By : Tushar</b></p>
        <p>📅 <b>Created On : {creation_date}</b></p>
    </div>
    <button class="enter-btn" onclick="enterBatch()">Open Your Batch</button>
    <button id="themeToggle" onclick="toggleTheme()">Switch to Dark</button>
</div>

<div id="video-section">
    <div class="video-header">
        <h2>{file_name_no_ext}</h2>
        <p><b>📥 Created By : Tushar</b></p>
        <p>📅 Created On : {creation_date}</p>
    </div>
    <button id="themeToggle" onclick="toggleTheme()">Switch to Dark</button>

    <div class="counts">Videos : {len(videos)} | PDFs : {len(pdfs)} | Others : {len(others)}</div>

    <div id="video-player">
        <video id="tushar-player" class="video-js vjs-default-skin" controls preload="auto" width="640" height="360"></video>
        <a id="open-youtube-btn" href="#" target="_blank">Open in YouTube</a>
    </div>

    <button class="back-btn" id="backBtn" onclick="backToMenu()">🏠 Back to Home 🏠</button>
    <button class="settings-btn" id="settingsBtn" onclick="openSettings()">⚙ Settings ⚙</button>

    <div class="settings-panel" id="settingsPanel">
        <h3>Playback Speed</h3>
        <button onclick="setSpeed(1)">1x</button>
        <button onclick="setSpeed(1.25)">1.25x</button>
        <button onclick="setSpeed(1.5)">1.5x</button>
        <button onclick="setSpeed(2)">2x</button>
        <button onclick="setSpeed(2.25)">2.25x</button>
        <button onclick="setSpeed(2.5)">2.5x</button>
        <button onclick="setSpeed(3)">3x</button>
        <br>
        <button onclick="closeSettings()">⬅ Back</button>
    </div>

    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="Search for videos, PDFs, or others..." oninput="filterContent()">
    </div>

    <div class="tabs">
        <div class="tab active" onclick="showContent('videos', this)">Videos</div>
        <div class="tab" onclick="showContent('pdfs', this)">PDFs</div>
        <div class="tab" onclick="showContent('others', this)">Others</div>
    </div>

    <div id="videos" class="content">{video_links}</div>
    <div id="pdfs" class="content">{pdf_links}</div>
    <div id="others" class="content">{other_links}</div>

    <div class="footer">🎊 Created By : Tushar 🎊</div>
</div>

<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
<script>
const player = videojs('tushar-player', {{controls:true, fluid:true}});

function toggleTheme(){{
    if(document.body.classList.contains('light')){{
        document.body.classList.remove('light');
        document.body.classList.add('dark');
        document.querySelectorAll('#themeToggle').forEach(btn => btn.innerText='Switch to Light');
        localStorage.setItem('theme','dark');
    }} else {{
        document.body.classList.remove('dark');
        document.body.classList.add('light');
        document.querySelectorAll('#themeToggle').forEach(btn => btn.innerText='Switch to Dark');
        localStorage.setItem('theme','light');
    }}
}}

function enterBatch(){{
    document.getElementById('welcome-page').style.display='none';
    document.getElementById('video-section').style.display='block';
    sessionStorage.setItem("enteredBatch","true");
    showContent('videos', document.querySelector('.tab.active'));
}}

function playVideo(url){{
    document.getElementById('backBtn').style.display='block';
    document.getElementById('settingsBtn').style.display='block';
    const playerContainer=document.getElementById('video-player');
    const openYTBtn=document.getElementById('open-youtube-btn');
    const iframe=document.getElementById('youtube-iframe');
    if(iframe) iframe.remove();
    if(url.includes("youtube.com/watch")){{
        const yt_id=new URL(url).searchParams.get("v");
        const ytIframe=document.createElement("iframe");
        ytIframe.id="youtube-iframe";
        ytIframe.width="100%";
        ytIframe.height="360";
        ytIframe.src="https://www.youtube.com/embed/"+yt_id+"?autoplay=1";
        ytIframe.frameBorder="0";
        ytIframe.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        ytIframe.allowFullscreen=true;
        playerContainer.appendChild(ytIframe);
        openYTBtn.style.display="block";
        openYTBtn.href=url;
        player.pause();
    }} else if(url.includes('.m3u8') || url.includes('.mp4')){{
        playerContainer.style.display="block";
        player.src({{src:url,type:url.includes('.m3u8')?'application/x-mpegURL':'video/mp4'}});
        player.play().catch(()=>{{window.open(url,'_blank');}});
        openYTBtn.style.display="none";
    }} else {{
        window.open(url,'_blank');
        openYTBtn.style.display="none";
    }}
}}

function backToMenu(){{
    const iframe=document.getElementById('youtube-iframe');
    if(iframe) iframe.remove();
    player.pause();
    document.getElementById('backBtn').style.display='none';
    document.getElementById('settingsBtn').style.display='none';
}}

function openSettings(){{
    document.getElementById('settingsPanel').style.display='block';
    document.getElementById('settingsBtn').style.display='none';
}}

function closeSettings(){{
    document.getElementById('settingsPanel').style.display='none';
    document.getElementById('settingsBtn').style.display='block';
}}

function setSpeed(speed){{
    player.playbackRate(speed);
    alert("Playback Speed set to "+speed+"x");
}}

function showContent(tabId, elem){{
    document.querySelectorAll('.content').forEach(c=>c.style.display='none');
    document.getElementById(tabId).style.display='block';
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    elem.classList.add('active');
    filterContent();
}}

function filterContent(){{
    const term=document.getElementById('searchInput').value.toLowerCase();
    ['videos','pdfs','others'].forEach(cat=>{{
        document.querySelectorAll('#'+cat+' .card').forEach(i=>{{i.style.display=i.textContent.toLowerCase().includes(term)?'block':'none';}});
    }});
}}

document.addEventListener('DOMContentLoaded',()=>{{
    // Apply persisted theme
    const savedTheme = localStorage.getItem('theme');
    if(savedTheme){{
        document.body.className = savedTheme;
        document.querySelectorAll('#themeToggle').forEach(btn => {{
            btn.innerText = savedTheme==='dark' ? 'Switch to Light' : 'Switch to Dark';
        }});
    }}

    // Show video-section if user clicked "Open Your Batch" in this tab
    if(sessionStorage.getItem("enteredBatch")==="true"){{
        document.getElementById('welcome-page').style.display='none';
        document.getElementById('video-section').style.display='block';
    }}

    showContent('videos', document.querySelector('.tab.active'));
}});
</script>
</body>
</html>
"""
    return html_template

def download_video(url, output_path):
    command = f"ffmpeg -i {url} -c copy {output_path}"
    subprocess.run(command, shell=True, check=True)
    
