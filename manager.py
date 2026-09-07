import os
import sys
import time
import sqlite3
import telebot
from telebot import types
from keep_alive import keep_alive

print("--- Launching Brand New Apex Engine ---", flush=True)

# আপনার বটের টোকেন
BOT_TOKEN = "8967415594:AAHMJX7BU-EIBm3vjRfVGRepRcabjPbo_SM"
bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

ADMIN_USER_ID = 8243644026
ADMIN_USERNAME = "rafimhossen"

TARGET_CHANNEL = "@rafimhossen3"
NAGAD_NUMBER = "01726836941"

DB_FILE = "apex_database.db"

# ==================== DATABASE ====================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS apex_orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT,
        package TEXT,
        ad_text TEXT,
        photo_id TEXT,
        trx_id TEXT,
        status TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS apex_users (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

init_db()

def log_user(user_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO apex_users VALUES (?)", (user_id,))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_stats():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM apex_users")
        u_cnt = c.fetchone()[0]
        c.execute("SELECT count(*) FROM apex_orders WHERE status='POSTED'")
        a_cnt = c.fetchone()[0]
        conn.close()
        return u_cnt, a_cnt
    except Exception:
        return 0, 0

MODULE_DETAILS = {
    "admin": "🛡️ **Admin Module:** চ্যানেল ও গ্রুপ অ্যাডমিন ম্যানেজমেন্ট কনসোল।",
    "antiflood": "🌊 **Antiflood:** অবাঞ্ছিত মেসেজ ও লিঙ্ক স্প্যাম স্বয়ংক্রিয়ভাবে ব্লক।",
    "antiraid": "⚔️ **AntiRaid:** জরুরি অবস্থায় সার্বিক প্রতিরক্ষা ও অটো-লক।",
    "approval": "🤝 **Approval:** বিশ্বস্ত মেম্বারদের বিশেষ রাইটস অনুমোদন।",
    "bans": "🚫 **Bans:** ক্ষতিকর অ্যাকাউন্ট এক ক্লিকে স্থায়ীভাবে ব্যান।",
    "blocklists": "⛔ **Blocklists:** নির্দিষ্ট ক্ষতিকর শব্দ ও লিংক স্বয়ংক্রিয় ব্লকলিস্ট।",
    "captcha": "🤖 **CAPTCHA:** নতুন যুক্ত হওয়া প্রতিটি মেম্বারের স্মার্ট ভেরিফিকেশন।",
    "cleancom": "🧹 **Clean Com:** কমান্ড ও বটের মেসেজ চ্যাট থেকে অটো রিমুভ।",
    "cleanserv": "🧽 **Clean Service:** সার্ভিস নোটিফিকেশন ও বটের লগিং ক্লিন রাখা।",
    "connect": "🔗 **Connect:** দ্রুত কানেকশন ও মেম্বার হ্যান্ডলিং।",
    "disabling": "📴 **Disabling:** অপ্রয়োজনীয় ফিচার ডিজেবল রাখার সুবিধা।",
    "federation": "🌐 **Federation:** যৌথ গ্রুপ নেটওয়ার্ক ম্যানেজমেন্ট।",
    "filters": "🎯 **Filters:** কি-ওয়ার্ড অনুযায়ী ইনস্ট্যান্ট অটোমেটেড রিপ্লাই।",
    "formatting": "✍️ **Formatting:** বোল্ড, প্রিমিয়াম ফন্ট ও স্টাইলিশ টেক্সট এডিটর।",
    "greetings": "👋 **Greetings:** কাস্টম ওয়েলকাম বার্তা ও রুলস দেখানো।",
    "backup": "📦 **Backup:** ক্লাউড ডাটাবেজ ব্যাকআপ ও রিস্টোরেশন।",
    "language": "🌍 **Language:** বহুভাষিক সাপোর্ট ও বাংলা ইন্টারফেস।",
    "locks": "🔒 **Locks:** মিডিয়া, স্টিকার, অডিও ও লিংক লক রাখার সুবিধা।",
    "logs": "📝 **Logs:** চ্যানেলের প্রতিটি কাজের সার্বক্ষণিক রেকর্ড।",
    "misc": "⚙️ **Misc:** অতিরিক্ত টুলস ও কনফিগারেশন সেটিংস।",
    "notes": "📌 **Notes:** ক্লাউডে প্রয়োজনীয় নোটস ও মিডিয়া সংরক্ষণ।",
    "pin": "📍 **Pin:** গুরুত্বপূর্ণ পোস্ট এক ক্লিকে পিন করে রাখা।",
    "privacy": "🔐 **Privacy:** ব্যবহারকারীর ডেটার শতভাগ এনক্রিপশন ও গোপনীয়তা।",
    "purges": "🗑️ **Purges:** হাজার হাজার মেসেজ সেকেন্ডে ডিলিট করার ক্ষমতা।",
    "reports": "📢 **Reports:** ক্লায়েন্ট ও মেম্বারদের রিপোর্ট সরাসরি ওনারের ইনবক্সে।",
    "rules": "📜 **Rules:** সার্বিক নিয়মাবলী প্রদর্শনের মডিউল।",
    "topics": "💬 **Topics:** ক্যাটাগরি ও সাব-টপিক আলাদা করার টুল।",
    "warnings": "⚠️ **Warnings:** মেম্বারদের ওয়ার্নিং সিস্টেম ও অটো-অ্যাকশন।",
    "custom": "⭐ **Custom Instances:** সম্পূর্ণ কাস্টমাইজড প্রিমিয়াম ইঞ্জিন।"
}

AD_PACKAGES = {
    "pkg1": {"name": "⚡ ১টি ইনস্ট্যান্ট পোস্ট", "price": "৫০ টাকা"},
    "pkg2": {"name": "📌 ২৪ ঘণ্টার ভিআইপি পিন", "price": "১০০ টাকা"},
    "pkg3": {"name": "💎 ৩ দিনের মেগা ড্রাইভ", "price": "২৫০ টাকা"}
}

def get_bottom_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🚀 প্রমোশন বুক করুন"), types.KeyboardButton("💳 নগদ পেমেন্ট গেটওয়ে"))
    markup.add(types.KeyboardButton("📈 লাইভ মেট্রিক্স"), types.KeyboardButton("👑 আমার একাউন্ট"))
    markup.add(types.KeyboardButton("💬 ওনার সাপোর্ট"), types.KeyboardButton("🔄 রিফ্রেশ"))
    return markup

def get_rose_dashboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton("🛡️ Admin", callback_data="m_admin"), types.InlineKeyboardButton("🌊 Antiflood", callback_data="m_antiflood"), types.InlineKeyboardButton("⚔️ AntiRaid", callback_data="m_antiraid"))
    markup.add(types.InlineKeyboardButton("🤝 Approval", callback_data="m_approval"), types.InlineKeyboardButton("🚫 Bans", callback_data="m_bans"), types.InlineKeyboardButton("⛔ Blocklists", callback_data="m_blocklists"))
    markup.add(types.InlineKeyboardButton("🤖 CAPTCHA", callback_data="m_captcha"), types.InlineKeyboardButton("🧹 Clean Com", callback_data="m_cleancom"), types.InlineKeyboardButton("🧽 Clean Servi", callback_data="m_cleanserv"))
    markup.add(types.InlineKeyboardButton("🔗 Connect", callback_data="m_connect"), types.InlineKeyboardButton("📴 Disabling", callback_data="m_disabling"), types.InlineKeyboardButton("🌐 Federation", callback_data="m_federation"))
    markup.add(types.InlineKeyboardButton("🎯 Filters", callback_data="m_filters"), types.InlineKeyboardButton("✍️ Formatting", callback_data="m_formatting"), types.InlineKeyboardButton("👋 Greetings", callback_data="m_greetings"))
    markup.add(types.InlineKeyboardButton("📦 Backup", callback_data="m_backup"), types.InlineKeyboardButton("🌍 Language", callback_data="m_language"), types.InlineKeyboardButton("🔒 Locks", callback_data="m_locks"))
    markup.add(types.InlineKeyboardButton("📝 Logs", callback_data="m_logs"), types.InlineKeyboardButton("⚙️ Misc", callback_data="m_misc"), types.InlineKeyboardButton("📌 Notes", callback_data="m_notes"))
    markup.add(types.InlineKeyboardButton("📍 Pin", callback_data="m_pin"), types.InlineKeyboardButton("🔐 Privacy", callback_data="m_privacy"), types.InlineKeyboardButton("🗑️ Purges", callback_data="m_purges"))
    markup.add(types.InlineKeyboardButton("📢 Reports", callback_data="m_reports"), types.InlineKeyboardButton("📜 Rules", callback_data="m_rules"), types.InlineKeyboardButton("💬 Topics", callback_data="m_topics"))
    markup.row(types.InlineKeyboardButton("⚠️ Warnings", callback_data="m_warnings"), types.InlineKeyboardButton("⭐ Custom Instances", callback_data="m_custom"))
    markup.row(types.InlineKeyboardButton("👨‍💻 Developer Support (@rafimhossen) ↗", url=f"https://t.me/{ADMIN_USERNAME}"))
    return markup

def get_back_button():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.row(
        types.InlineKeyboardButton("⬅️ ব্যাক মেনু", callback_data="nav_home"),
        types.InlineKeyboardButton("📢 বিজ্ঞাপন প্যাকেজ ↗", callback_data="nav_packages")
    )
    return m

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    log_user(message.from_user.id)
    u = message.from_user

    welcome_text = (
        f"🌟 **স্বাগতম, {u.first_name}!**\n\n"
        "এটি **Rafim Apex Ads & Manager** — চ্যানেলে প্রমোশন ও স্বয়ংক্রিয় ব্যবস্থাপনার আল্টিমেট প্ল্যাটফর্ম।\n\n"
        "নিচে মডিউল ড্যাশবোর্ডে ক্লিক করে বিস্তারিত দেখুন অথবা নিচের চারকোনা মেনু বাটন ব্যবহার করুন:"
    )
    bot.send_message(message.chat.id, "কন্ট্রোল মেনু সক্রিয় করা হয়েছে 🔘", reply_markup=get_bottom_keyboard())
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_rose_dashboard(), parse_mode='Markdown')

@bot.message_handler(func=lambda msg: msg.text in [
    "🚀 প্রমোশন বুক করুন", "💳 নগদ পেমেন্ট গেটওয়ে", "📈 লাইভ মেট্রিক্স", "👑 আমার একাউন্ট", "💬 ওনার সাপোর্ট", "🔄 রিফ্রেশ"
])
def handle_menu_options(message):
    log_user(message.from_user.id)
    u = message.from_user

    if message.text == "🔄 রিফ্রেশ":
        handle_start(message)
    elif message.text == "💳 নগদ পেমেন্ট গেটওয়ে":
        text = (
            "💳 **অফিশিয়াল নগদ পার্সোনাল নম্বর:**\n\n"
            f"📱 নগদ নম্বর: `{NAGAD_NUMBER}`\n\n"
            "টাকা পাঠাতে নগদ অ্যাপ থেকে 'Send Money' করুন।"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    elif message.text == "📈 লাইভ মেট্রিক্স":
        u_cnt, a_cnt = get_stats()
        text = (
            "📊 **সার্ভার মেট্রিক্স ও স্ট্যাটাস:**\n\n"
            "🟢 সার্ভার অবস্থা: Online 24/7\n"
            f"👥 মোট অ্যাক্টিভ ইউজার: {u_cnt} জন\n"
            f"📢 প্রকাশিত প্রোমো: {a_cnt} টি"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    elif message.text == "👑 আমার একাউন্ট":
        text = (
            f"👤 **ইউজার প্রোফাইল:**\n\n"
            f"• নাম: {u.first_name}\n"
            f"• ইউজারনেম: @{u.username or 'নেই'}\n"
            f"• আইডি: `{u.id}`"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    elif message.text == "💬 ওনার সাপোর্ট":
        bot.send_message(message.chat.id, f"👨‍💻 ওনারের সাথে যোগাযোগ: @{ADMIN_USERNAME}")
    elif message.text == "🚀 প্রমোশন বুক করুন":
        display_ad_packages(message.chat.id)

def display_ad_packages(chat_id):
    m = types.InlineKeyboardMarkup(row_width=1)
    for k, v in AD_PACKAGES.items():
        m.add(types.InlineKeyboardButton(f"{v['name']} — {v['price']}", callback_data=f"buy_{k}"))
    m.add(types.InlineKeyboardButton("⬅️ ড্যাশবোর্ডে ফিরুন", callback_data="nav_home"))

    text = (
        f"📢 **{TARGET_CHANNEL} চ্যানেলে প্রচার করার প্যাকেজসমূহ:**\n\n"
        "পছন্দের প্যাকেজটি নির্বাচন করুন:"
    )
    bot.send_message(chat_id, text, reply_markup=m, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: True)
def process_callbacks(call):
    data = call.data
    log_user(call.from_user.id)

    if data == "nav_home":
        bot.edit_message_text(
            "⚡ **মডিউল ড্যাশবোর্ড:**\nনিচের যেকোনো মডিউলে ক্লিক করে বিস্তারিত দেখে নিন:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_rose_dashboard(),
            parse_mode='Markdown'
        )
    elif data == "nav_packages":
        display_ad_packages(call.message.chat.id)
    elif data.startswith("m_"):
        key = data.replace("m_", "")
        desc = MODULE_DETAILS.get(key, "📌 মডিউলটি সক্রিয় রয়েছে।")
        bot.edit_message_text(
            desc,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_back_button(),
            parse_mode='Markdown'
        )
    elif data.startswith("buy_"):
        pkg_key = data.replace("buy_", "")
        pkg = AD_PACKAGES[pkg_key]

        msg = bot.send_message(
            call.message.chat.id,
            f"📝 আপনি নির্বাচন করেছেন: **{pkg['name']}**\n\n"
            "আপনার বিজ্ঞাপনের সম্পূর্ণ লেখা (ক্যাপশন ও লিংক) অথবা ছবি সহ লিখে পাঠান:",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, step_get_content, pkg_key)
    elif data.startswith(("post_ok_", "post_no_")):
        handle_owner_decision(call)

def step_get_content(message, pkg_key):
    ad_text = message.text or message.caption or ""
    photo_id = message.photo[-1].file_id if message.photo else None

    if not ad_text and not photo_id:
        bot.reply_to(message, "⚠️ কোনো টেক্সট বা ছবি পাওয়া যায়নি। অনুগ্রহ করে /start দিন।")
        return

    pkg = AD_PACKAGES[pkg_key]
    pay_prompt = (
        "💳 **বিজ্ঞাপন সাবমিট সফল হয়েছে!**\n\n"
        f"📦 প্যাকেজ: **{pkg['name']}**\n"
        f"💵 ফি: **{pkg['price']}**\n\n"
        f"১. নগদ (Personal): `{NAGAD_NUMBER}`\n"
        f"২. সেন্ড মানি করুন: **{pkg['price']}**\n\n"
        "টাকা পাঠানোর পর নগদ থেকে প্রাপ্ত **TrxID** নিচে মেসেজ আকারে পাঠান:"
    )
    msg = bot.send_message(message.chat.id, pay_prompt, parse_mode='Markdown')
    bot.register_next_step_handler(msg, step_save_trx, pkg['name'], ad_text, photo_id)

def step_save_trx(message, pkg_name, ad_text, photo_id):
    trx_id = message.text.strip()
    u = message.from_user
    u_name = f"{u.first_name} (@{u.username or 'নেই'})"

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO apex_orders (user_id, user_name, package, ad_text, photo_id, trx_id, status) VALUES (?, ?, ?, ?, ?, ?, 'PENDING')",
              (u.id, u_name, pkg_name, ad_text, photo_id, trx_id))
    order_id = c.lastrowid
    conn.commit()
    conn.close()

    bot.reply_to(message, "✅ পেমেন্ট ডাটা সংরক্ষিত হয়েছে! ওনার ভেরিফাই করলেই চ্যানেলে সরাসরি পোস্ট হয়ে যাবে।")

    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("✅ Approve & Post", callback_data=f"post_ok_{order_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"post_no_{order_id}")
    )

    alert = (
        "🚨 **নতুন বিজ্ঞাপন বুকিং রিকোয়েস্ট!**\n\n"
        f"🆔 অর্ডার নম্বর: `#{order_id}`\n"
        f"👤 ক্লায়েন্ট: {u_name}\n"
        f"📦 প্যাকেজ: **{pkg_name}**\n"
        f"🧾 নগদ TrxID: `{trx_id}`\n\n"
        "👇 **বিজ্ঞাপনের প্রিভিউ:**"
    )
    bot.send_message(ADMIN_USER_ID, alert, parse_mode='Markdown')

    if photo_id:
        bot.send_photo(ADMIN_USER_ID, photo_id, caption=ad_text, reply_markup=m)
    else:
        bot.send_message(ADMIN_USER_ID, f"📄 **ক্যাপশন:**\n{ad_text}", reply_markup=m)

def handle_owner_decision(call):
    if call.from_user.id != ADMIN_USER_ID:
        return

    action, order_id = call.data.split("_")[1], call.data.split("_")[2]

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, package, ad_text, photo_id FROM apex_orders WHERE order_id=? AND status='PENDING'", (order_id,))
    row = c.fetchone()

    if not row:
        bot.answer_callback_query(call.id, "অর্ডারটি ইতিমধ্যে সম্পন্ন বা বাতিল হয়েছে!")
        conn.close()
        return

    client_id, pkg_name, ad_text, photo_id = row

    if action == "ok":
        c.execute("UPDATE apex_orders SET status='POSTED' WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

        try:
            if photo_id:
                p_msg = bot.send_photo(TARGET_CHANNEL, photo_id, caption=ad_text)
            else:
                p_msg = bot.send_message(TARGET_CHANNEL, ad_text)

            if "পিন" in pkg_name:
                bot.pin_chat_message(TARGET_CHANNEL, p_msg.message_id)
        except Exception as e:
            bot.send_message(ADMIN_USER_ID, f"⚠️ চ্যানেলে পোস্ট করতে ত্রুটি: {e}")

        bot.send_message(client_id, f"🎉 **আপনার বিজ্ঞাপনটি সফলভাবে {TARGET_CHANNEL} চ্যানেলে পোস্ট করা হয়েছে!**")
        bot.edit_message_text(f"✅ অর্ডার `#{order_id}` Approved এবং সরাসরি চ্যানেলে পোস্ট সম্পন্ন!", call.message.chat.id, call.message.message_id)

    elif action == "no":
        c.execute("UPDATE apex_orders SET status='REJECTED' WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

        bot.send_message(client_id, "❌ আপনার পেমেন্ট তথ্য মেলেনি। প্রয়োজনে ওনারের সাথে যোগাযোগ করুন: @" + ADMIN_USERNAME)
        bot.edit_message_text(f"❌ অর্ডার `#{order_id}` বাতিল করা হয়েছে!", call.message.chat.id, call.message.message_id)

if __name__ == '__main__':
    keep_alive()
    try:
        bot.remove_webhook()
        time.sleep(1)
    except Exception:
        pass

    bot_info = bot.get_me()
    print(f"Apex System Online: @{bot_info.username}", flush=True)

    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Loop Alert: {e}", flush=True)
            time.sleep(3)
