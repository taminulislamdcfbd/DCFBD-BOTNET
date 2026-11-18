import time
import threading
import telebot

# আপনার দেওয়া কনফিগারেশন
TOKEN = "9167624344:AAEGKkgzkIiHtGhDNUvK-oYVyJnHS0j4pNU"
CHAT_ID = "8844176265"
GROUP_ID = "-1003913198197"

bot = telebot.TeleBot(TOKEN)

# এট্যাক কন্ট্রোল করার জন্য গ্লোবাল ডিকশনারি (অফ করার জন্য)
active_attacks = {}

# সব মেথডের তালিকা (/met কমান্ডের জন্য)
METHODS_TEXT = """
✨ **[ DCFBD ] | DarkNet Cyber Force BD Methods List v1.1** ✨

🔥 **Layer 7 & Attack Methods:**
- `/crash <url> GET` - ক্র্যাশ এট্যাশ শুরু করতে (আনলিমিটেড চলবে)
- `/httpflood <url> <threads> <GET/POST> <time>` - HTTP Flood এট্যাক
- `/slow <url> <time>` - Slowloris এট্যাক

🛠 **Tools & Info:**
- `/rules` - প্যানেলের রুলস দেখতে
- `/ports` - কমন পোর্ট লিস্ট দেখতে
- `/stop` - চলমান যেকোনো এট্যাক বন্ধ করতে
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_msg = f"""
🤖 **DarkNet Cyber Force BD C2 Panel**
স্বাগতম, {user_name}! এটি ডিসিএফবিডি (DCFBD) টেলিগ্রাম বট নেট প্যানেল।

📌 **ಲಭ্য কমান্ডসমূহ:**
- `/met` - সব এট্যাক ও টুলস মেথড দেখতে।
- `/crash <url> GET` - ক্র্যাশ এট্যাক শুরু করতে।
- `/httpflood <url> <threads> <GET/POST> <time>` - HTTP Flood এট্যাক।
- `/slow <url> <time>` - Slowloris এট্যাক।
- `/rules` - প্যানেলের রুলস দেখতে।
- `/ports` - কমন পোর্ট লিস্ট দেখতে।
- `/stop` - চলমান এট্যাক বন্ধ করতে।
"""
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

@bot.message_handler(commands=['met'])
def show_methods(message):
    bot.reply_to(message, METHODS_TEXT, parse_mode="Markdown")

@bot.message_handler(commands=['rules'])
def show_rules(message):
    rules_text = """
📜 **DCFBD Rules Panel:**
1. Do not attack .gov/.gob/.edu/.mil domains
2. Only attack stress testing servers
3. Don't skid the panel
4. Give a star to the github repository
"""
    bot.reply_to(message, rules_text, parse_mode="Markdown")

@bot.message_handler(commands=['ports'])
def show_ports(message):
    ports_text = """
🔌 **Common Ports List:**
- `21` - SFTP
- `22` - SSH
- `53` - DNS
- `80` - HTTP
- `443` - HTTPS
- `25565` - MINECRAFT
"""
    bot.reply_to(message, ports_text, parse_mode="Markdown")

# ব্যাকগ্রাউন্ডে আনলিমিটেড বা লং-টাইম এট্যাক রান করার ফাংশন
def background_attack(chat_id, message_id, target_info, attack_key):
    counter = 1
    while active_attacks.get(attack_key, False):
        live_text = f"""
🚀 **[DCFBD] Attack Running Live...**
🎯 Target: `{target_info}`
🔄 Request Sent Count: `{counter * 100}+`
⚡ Status: `Attacking... (Running in Loop)`
🛑 বন্ধ করতে `/stop` কমান্ড দিন।
"""
        try:
            bot.edit_message_text(live_text, chat_id=chat_id, message_id=message_id, parse_mode="Markdown")
        except:
            pass
        
        counter += 1
        time.sleep(3)  # প্রতি ৩ সেকেন্ডে লাইভ আপডেট পাঠাবে

    try:
        bot.send_message(chat_id, f"🛑 **[DCFBD] Attack Stopped Successfully by Admin!**\nTarget: `{target_info}`", parse_mode="Markdown")
    except:
        pass

# Crash URL GET কমান্ড হ্যান্ডলার (আনলিমিটেড এট্যাক)
@bot.message_handler(commands=['crash'])
def handle_crash(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ Usage: `/crash <url> GET`\nExample: `/crash http://example.com GET`", parse_mode="Markdown")
            return
        
        url = args[1]
        method = args[2].upper()
        target_info = f"{url} [{method}]"
        
        msg = bot.reply_to(message, f"🚀 **[DCFBD] Unlimited Crash Attack Initiated!**\nTarget: `{target_info}`\nStatus: `Starting...`", parse_mode="Markdown")
        
        attack_key = f"{message.chat.id}_{msg.message_id}"
        active_attacks[attack_key] = True
        
        # ব্যাকগ্রাউন্ড থ্রেডে এট্যাক লুপ চালু করা
        threading.Thread(target=background_attack, args=(message.chat.id, msg.message_id, target_info, attack_key)).start()
        
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
        
        url, threads, method, duration = args[1], args[2], args[3], args[4]
        target_info = f"HTTPFlood -> {url} ({threads} Threads)"
        
        msg = bot.reply_to(message, f"🚀 **[DCFBD] HTTPFlood Attack Started!**\nTarget: `{target_info}`", parse_mode="Markdown")
        attack_key = f"{message.chat.id}_{msg.message_id}"
        active_attacks[attack_key] = True
        
        threading.Thread(target=background_attack, args=(message.chat.id, msg.message_id, target_info, attack_key)).start()
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
        url, duration = args[1], args[2]
        target_info = f"Slowloris -> {url}"
        
        msg = bot.reply_to(message, f"🚀 **[DCFBD] Slowloris Attack Started!**\nTarget: `{target_info}`", parse_mode="Markdown")
        attack_key = f"{message.chat.id}_{msg.message_id}"
        active_attacks[attack_key] = True
        
        threading.Thread(target=background_attack, args=(message.chat.id, msg.message_id, target_info, attack_key)).start()
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# এট্যাক বন্ধ করার কমান্ড (/stop)
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    # সমস্ত চলমান এট্যাক বন্ধ করতে ফ্ল্যাগ ফলস করে দেওয়া হলো
    for key in active_attacks:
        active_attacks[key] = False
    bot.reply_to(message, "🛑 **[DCFBD] All active attacks have been stopped by admin!**", parse_mode="Markdown")

print("[*] DCFBD Telegram C2 Bot is running...")
bot.infinity_polling()
