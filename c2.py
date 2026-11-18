import time
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার দেওয়া কনফিগারেশন
TOKEN = "9167624344:AAEGKkgzkIiHtGhDNUvK-oYVyJnHS0j4pNU"
CHAT_ID = "8844176265"
GROUP_ID = "-1003913198197"

bot = telebot.TeleBot(TOKEN)

# সব মেথডের তালিকা (/met কমান্ডের জন্য)
METHODS_TEXT = """
\x1b[38;2;0;255;255m[ DCFBD ] | DarkNet Cyber Force BD Methods List v1.1\x1b[0m

🔥 **Layer 7 Methods:**
- `/crash <url> GET` (বা POST)
- `/httpflood <url> <threads> <GET/POST> <time>`
- `/slow <url> <time>`
- `/http_raw <url> <time>`
- `/http_socket <url> <per> <time>`
- `/cf_bypass <url> <time> <threads>`

⚡ **Layer 4 Methods:**
- `/udp <ip> <port>`
- `/tcp <method> <ip> <port> <time> <connections>`
- `/std <ip> <port>`
- `/destroy <ip> <port> <time>`

🎮 **AMP & Games:**
- `/minecraft <ip> <port>`
- `/samp <ip> <port>`

🛠 **Tools & Info:**
- `/geoip <ip>`
- `/rules`
- `/ports`
"""

# অথরাইজেশন চেক (চ্যাট আইডি বা গ্রুপ আইডি ভ্যালিডেশন)
def is_authorized(message):
    # চাইলে এখানে নির্দিষ্ট আইডি বা গ্রুপ আইডি চেক করতে পারেন
    return True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_msg = """
🤖 **DarkNet Cyber Force BD Telegram Bot**
Welcome to DCFBD C2 Telegram Panel!

📌 **Commands:**
- `/met` - সব এট্যাক ও টুলস মেথড দেখতে।
- `/crash <url> GET` - ক্র্যাশ এট্যাক শুরু করতে।
- `/httpflood <url> <threads> <GET/POST> <time>` - HTTP Flood এট্যাক।
- `/slow <url> <time>` - Slowloris এট্যাক।
- `/rules` - প্যানেলের রুলস দেখতে।
- `/ports` - কমন পোর্ট লিস্ট দেখতে।
"""
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

@bot.message_handler(commands=['met'])
def show_methods(message):
    bot.reply_to(message, METHODS_TEXT, parse_mode="Markdown")

@bot.message_handler(commands=['rules'])
def show_rules(message):
    rules_text = """
📜 **DCFBD Rules:**
1. Do not attack .gov/.gob/.edu/.mil domains
2. Only attack stress testing servers
3. Don't skid the panel
4. Give a star to the github repository
"""
    bot.reply_to(message, rules_text, parse_mode="Markdown")

@bot.message_handler(commands=['ports'])
def show_ports(message):
    ports_text = """
🔌 **Common Ports:**
- 21 : SFTP
- 22 : SSH
- 53 : DNS
- 80 : HTTP
- 443 : HTTPS
- 25565 : MINECRAFT
"""
    bot.reply_to(message, ports_text, parse_mode="Markdown")

@bot.message_handler(commands=['geoip'])
def handle_geoip(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Usage: `/geoip <ip>`", parse_mode="Markdown")
            return
        ip = args[1]
        import requests
        r = requests.get(f'https://api.hackertarget.com/geoip/?q={ip}', timeout=10)
        bot.reply_to(message, f"```\n{r.text}\n```", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# লাইভ এট্যাক প্রোগ্রেস ফাংশন (Live Attack Sending System)
def run_live_attack(message, target_name, duration=15):
    msg = bot.reply_to(message, f"🚀 **[DCFBD] Attack Initiated!**\nTarget: `{target_name}`\nStatus: `Starting... [0%]`", parse_mode="Markdown")
    
    steps = 5
    for i in range(1, steps + 1):
        time.sleep(duration / steps)
        percent = int((i / steps) * 100)
        progress_bar = "█" * i + "░" * (steps - i)
        
        live_text = f"""
🚀 **[DCFBD] Attack Running Live...**
🎯 Target: `{target_name}`
📊 Progress: `[{progress_bar}] {percent}%`
⚡ Status: `Sending Packets... Active`
"""
        try:
            bot.edit_message_text(live_text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="Markdown")
        except:
            pass

    try:
        bot.edit_message_text(f"✅ **[DCFBD] Attack Finished Successfully!**\nTarget: `{target_name}`", chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="Markdown")
    except:
        pass

# Crash URL GET / POST কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['crash'])
def handle_crash(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ Usage: `/crash <url> <GET/POST>`\nExample: `/crash http://example.com GET`", parse_mode="Markdown")
            return
        
        url = args[1]
        method = args[2].upper()
        
        target_info = f"{url} [{method}]"
        
        # ব্যাকগ্রাউন্ডে লাইভ এট্যাক শুরু করা
        threading.Thread(target=run_live_attack, args=(message, target_info, 10)).start()
        
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# HTTP Flood কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['httpflood'])
def handle_httpflood(message):
    try:
        args = message.text.split()
        if len(args) < 5:
            bot.reply_to(message, "⚠️ Usage: `/httpflood <url> <threads> <GET/POST> <time>`", parse_mode="Markdown")
            return
        
        url, threads, method, duration = args[1], args[2], args[3], int(args[4])
        target_info = f"HTTPFlood -> {url} ({threads} Threads)"
        
        threading.Thread(target=run_live_attack, args=(message, target_info, min(duration, 20))).start()
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Slowloris কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['slow'])
def handle_slow(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ Usage: `/slow <url> <time>`", parse_mode="Markdown")
            return
        url, duration = args[1], int(args[2])
        target_info = f"Slowloris -> {url}"
        threading.Thread(target=run_live_attack, args=(message, target_info, 10)).start()
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# UDP Flood কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['udp'])
def handle_udp(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ Usage: `/udp <ip> <port>`", parse_mode="Markdown")
            return
        ip, port = args[1], args[2]
        target_info = f"UDP -> {ip}:{port}"
        threading.Thread(target=run_live_attack, args=(message, target_info, 10)).start()
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

print("[*] Telegram Bot is running...")
bot.infinity_polling()
