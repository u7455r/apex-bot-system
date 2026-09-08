import os
import sys
import time
import sqlite3
import telebot
from telebot import types
from keep_alive import keep_alive

print("--- Launching Fully Working Ads Engine ---", flush=True)

BOT_TOKEN = "8967415594:AAHVZWYsgz6oXBUdSkdjdrjTOTuHucif6mc"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# আপনার সঠিক টেলিগ্রাম আইডি
ADMIN_USER_ID = 8243644026
ADMIN_USERNAME = "rafimhossen"

TARGET_CHANNEL = "@rafimhossen3"
REQ_CHANNEL_LINK = "https://t.me/rafimhossen3"
NAGAD_NUMBER = "01726836941"

DB_FILE = "pure_ads.db"

# ==================== DATABASE ====================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT,
        package TEXT,
        ad_text TEXT,
        photo_id TEXT,
        trx_id TEXT,
        status TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

init_db()

def log_user(user):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users VALUES (?)", (user.id,))
        conn.commit()
        conn.close()
    except Exception:
        pass

AD_PACKAGES = {
    "pkg1": {"name": "⚡ ১টি ইনস্ট্যান্ট চ্যানেল পোস্ট", "price": "৫০ ৳"},
    "pkg2": {"name": "📌 ২৪ ঘণ্টা ভিআইপি পিন পোস্ট", "price": "১০০ ৳"},
    "pkg3": {"name": "🔥 ৩ দিনের মেগা পাওয়ার বুস্ট", "price": "২৫০ ৳"}
}

# ==================== কীবোর্ড লেআউট ====================
def get_bottom_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🚀 বিজ্ঞাপন বুক করুন 📢"), types.KeyboardButton("💳 নগদ পেমেন্ট তথ্য ⚡"))
    markup.add(types.KeyboardButton("📜 প্রিমিয়াম নীতিমালা 🛡️"), types.KeyboardButton("💬 ওনার ডিরেক্ট সাপোর্ট ↗"))
    
    # শুধু ওনারের ফোনে এই স্পেশাল বাটনটি আসবে
    if user_id == ADMIN_USER_ID:
        markup.add(types.KeyboardButton("👑 পেন্ডিং অর্ডার দেখুন (Admin)"))
    return markup

def get_clean_dashboard():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("🔥 সেরা বিজ্ঞাপন প্যাকেজ ও রেট দেখুন 📊", callback_data="view_packages"))
    m.add(types.InlineKeyboardButton("💳 ইনস্ট্যান্ট নগদ পেমেন্ট গেটওয়ে ⚡", callback_data="view_payment"))
    m.add(types.InlineKeyboardButton("📢 আমাদের মূল চ্যানেল ভিজিট করুন ↗", url=REQ_CHANNEL_LINK))
    m.add(types.InlineKeyboardButton("👑 ওনার ইনবক্স (@rafimhossen) 💬", url=f"https://t.me/{ADMIN_USERNAME}"))
    return m

def get_back_button():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("⬅️ প্রধান মেনুতে ফিরে যান (Home)", callback_data="go_home"))
    return m

# ==================== মূল হ্যান্ডলার ====================
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    log_user(message.from_user)
    u_id = message.from_user.id
    u_name = message.from_user.first_name

    welcome_text = (
        f"👑 **স্বাগতম, {u_name}!** ✨\n\n"
        f"📢 আমাদের হাই-অ্যাক্টিভ চ্যানেল **{TARGET_CHANNEL}**-এ বিজ্ঞাপন বুক করতে নিচের অপশন ব্যবহার করুন:"
    )
    bot.send_message(message.chat.id, "🔘 মেনু প্যানেল সক্রিয় হয়েছে ⚡", reply_markup=get_bottom_keyboard(u_id))
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_clean_dashboard(), parse_mode='Markdown')

# পেন্ডিং অর্ডার দেখার ফাংশন
def display_pending_orders(chat_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT order_id, user_name, package, ad_text, photo_id, trx_id FROM orders WHERE status='PENDING'")
    rows = c.fetchall()
    conn.close()

    if not rows:
        bot.send_message(chat_id, "📭 বর্তমানে কোনো পেন্ডিং অর্ডার নেই!")
        return

    bot.send_message(chat_id, f"📋 **মোট {len(rows)} টি পেন্ডিং বিজ্ঞাপন রয়েছে:**")
    for r in rows:
        order_id, user_name, package, ad_text, photo_id, trx_id = r
        m = types.InlineKeyboardMarkup(row_width=2)
        m.add(
            types.InlineKeyboardButton("✅ এক ক্লিকে অনুমোদন ও পোস্ট", callback_data=f"post_ok_{order_id}"),
            types.InlineKeyboardButton("❌ বাতিল", callback_data=f"post_no_{order_id}")
        )
        caption = (
            f"🆔 অর্ডার নম্বর: `#{order_id}`\n"
            f"👤 ক্লায়েন্ট: {user_name}\n"
            f"📦 প্যাকেজ: **{package}**\n"
            f"🧾 নগদ TrxID: `{trx_id}`\n\n"
            f"📄 বিজ্ঞাপনের কনটেন্ট:\n{ad_text}"
        )
        if photo_id:
            bot.send_photo(chat_id, photo_id, caption=caption, reply_markup=m, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, caption, reply_markup=m, parse_mode='Markdown')

@bot.message_handler(commands=['orders', 'myid'])
def handle_special_commands(message):
    if message.text == '/myid':
        bot.reply_to(message, f"🆔 আপনার আইডি: `{message.from_user.id}`", parse_mode='Markdown')
        return
    if message.text == '/orders':
        display_pending_orders(message.chat.id)

@bot.message_handler(func=lambda msg: msg.text in [
    "🚀 বিজ্ঞাপন বুক করুন 📢", "💳 নগদ পেমেন্ট তথ্য ⚡", "📜 প্রিমিয়াম নীতিমালা 🛡️",
    "💬 ওনার ডিরেক্ট সাপোর্ট ↗", "👑 পেন্ডিং অর্ডার দেখুন (Admin)"
])
def handle_menu_options(message):
    txt = message.text
    if txt == "🚀 বিজ্ঞাপন বুক করুন 📢":
        show_packages(message.chat.id)
    elif txt == "💳 নগদ পেমেন্ট তথ্য ⚡":
        show_payment_info(message.chat.id)
    elif txt == "📜 প্রিমিয়াম নীতিমালা 🛡️":
        bot.send_message(message.chat.id, "📜 সঠিক TrxID দিয়ে পেমেন্ট করুন। ওনার যাচাই করে চ্যানেলে পোস্ট করে দেবেন।", reply_markup=get_back_button())
    elif txt == "💬 ওনার ডিরেক্ট সাপোর্ট ↗":
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton("💬 সরাসরি ইনবক্সে মেসেজ দিন ↗", url=f"https://t.me/{ADMIN_USERNAME}"))
        bot.send_message(message.chat.id, f"👑 ওনার যোগাযোগ:\n👉 @{ADMIN_USERNAME}", reply_markup=m)
    elif txt == "👑 পেন্ডিং অর্ডার দেখুন (Admin)":
        display_pending_orders(message.chat.id)

def show_packages(chat_id, message_id=None):
    m = types.InlineKeyboardMarkup(row_width=1)
    for k, v in AD_PACKAGES.items():
        m.add(types.InlineKeyboardButton(f"{v['name']} ➔ {v['price']}", callback_data=f"buy_{k}"))
    m.add(types.InlineKeyboardButton("⬅️ প্রধান মেনুতে ফিরে যান (Home)", callback_data="go_home"))
    text = f"💎 **{TARGET_CHANNEL} অফিশিয়াল প্রমোশন ডিলস**\n\n👇 প্যাকেজ বেছে নিন:"
    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=m, parse_mode='Markdown')
        except Exception:
            bot.send_message(chat_id, text, reply_markup=m, parse_mode='Markdown')
    else:
        bot.send_message(chat_id, text, reply_markup=m, parse_mode='Markdown')

def show_payment_info(chat_id, message_id=None):
    text = f"💳 **নগদ পার্সোনাল গেটওয়ে:**\n📱 নম্বর: `{NAGAD_NUMBER}` *(ট্যাপ করলেই কপি)*\n\nটাকা পাঠানোর পর নগদ থেকে প্রাপ্ত TrxID বটের কাছে লিখে পাঠান।"
    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=get_back_button(), parse_mode='Markdown')
        except Exception:
            bot.send_message(chat_id, text, reply_markup=get_back_button(), parse_mode='Markdown')
    else:
        bot.send_message(chat_id, text, reply_markup=get_back_button(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: True)
def handle_callbacks(call):
    data = call.data
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    if data == "go_home":
        welcome_text = f"👑 **স্বাগতম, {call.from_user.first_name}!**"
        try:
            bot.edit_message_text(welcome_text, chat_id, msg_id, reply_markup=get_clean_dashboard(), parse_mode='Markdown')
        except Exception:
            bot.send_message(chat_id, welcome_text, reply_markup=get_clean_dashboard(), parse_mode='Markdown')
    elif data == "view_packages":
        show_packages(chat_id, msg_id)
    elif data == "view_payment":
        show_payment_info(chat_id, msg_id)
    elif data.startswith("buy_"):
        pkg_key = data.replace("buy_", "")
        pkg = AD_PACKAGES[pkg_key]
        msg = bot.send_message(chat_id, f"📝 আপনি বেছে নিয়েছেন: **{pkg['name']}**\n\nবিজ্ঞাপনের ক্যাপশন ও লিংক (অথবা ছবি সহ ক্যাপশন) পাঠান:")
        bot.register_next_step_handler(msg, step_receive_ad_content, pkg_key)
    elif data.startswith(("post_ok_", "post_no_")):
        handle_owner_decision(call)

def step_receive_ad_content(message, pkg_key):
    ad_text = message.text or message.caption or ""
    photo_id = message.photo[-1].file_id if message.photo else None
    if not ad_text and not photo_id:
        bot.reply_to(message, "⚠️ কোনো তথ্য পাওয়া যায়নি! পুনরায় /start দিন।")
        return
    pkg = AD_PACKAGES[pkg_key]
    pay_prompt = f"💳 **নগদ নম্বর:** `{NAGAD_NUMBER}`\n💸 সেন্ড মানি ফি: **{pkg['price']}**\n\nটাকা পাঠানোর পর প্রাপ্ত **TrxID** টি নিচে লিখুন:"
    msg = bot.send_message(message.chat.id, pay_prompt, parse_mode='Markdown')
    bot.register_next_step_handler(msg, step_receive_trx, pkg['name'], ad_text, photo_id)

def step_receive_trx(message, pkg_name, ad_text, photo_id):
    trx_id = message.text.strip()
    u = message.from_user
    u_name = f"{u.first_name} (@{u.username or 'নেই'})"

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, user_name, package, ad_text, photo_id, trx_id, status) VALUES (?, ?, ?, ?, ?, ?, 'PENDING')",
              (u.id, u_name, pkg_name, ad_text, photo_id, trx_id))
    order_id = c.lastrowid
    conn.commit()
    conn.close()

    bot.reply_to(message, "✅ **আপনার পেমেন্ট রিকোয়েস্ট জমা হয়েছে!**\nঅ্যাডমিন নগদ যাচাই করার পর চ্যানেলে পোস্ট করে দেবেন।")

    # ওনারকে অ্যালার্ট পাঠানো
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("✅ এক ক্লিকে অনুমোদন ও পোস্ট", callback_data=f"post_ok_{order_id}"),
        types.InlineKeyboardButton("❌ বাতিল", callback_data=f"post_no_{order_id}")
    )
    alert = (
        "🚨 **নতুন বিজ্ঞাপন বুকিং এসেছে!**\n\n"
        f"🆔 অর্ডার নম্বর: `#{order_id}`\n"
        f"👤 ক্লায়েন্ট: {u_name}\n"
        f"📦 প্যাকেজ: **{pkg_name}**\n"
        f"🧾 নগদ TrxID: `{trx_id}`\n\n"
        "👇 **বিজ্ঞাপনের প্রিভিউ:**"
    )
    try:
        bot.send_message(ADMIN_USER_ID, alert, parse_mode='Markdown')
        if photo_id:
            bot.send_photo(ADMIN_USER_ID, photo_id, caption=ad_text, reply_markup=m)
        else:
            bot.send_message(ADMIN_USER_ID, f"📄 **ক্যাপশন:**\n{ad_text}", reply_markup=m)
    except Exception as e:
        print(f"Alert error: {e}")

def handle_owner_decision(call):
    action, order_id = call.data.split("_")[1], call.data.split("_")[2]
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, package, ad_text, photo_id FROM orders WHERE order_id=? AND status='PENDING'", (order_id,))
    row = c.fetchone()

    if not row:
        bot.answer_callback_query(call.id, "অর্ডারটি ইতিমধ্যে সম্পন্ন হয়েছে!")
        conn.close()
        return

    client_id, pkg_name, ad_text, photo_id = row

    if action == "ok":
        c.execute("UPDATE orders SET status='POSTED' WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

        try:
            if photo_id:
                p_msg = bot.send_photo(TARGET_CHANNEL, photo_id, caption=ad_text)
            else:
                p_msg = bot.send_message(TARGET_CHANNEL, ad_text)

            if "পিন" in pkg_name or "বুস্ট" in pkg_name:
                bot.pin_chat_message(TARGET_CHANNEL, p_msg.message_id)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"⚠️ চ্যানেলে পোস্ট করতে সমস্যা: {e}")

        bot.send_message(client_id, f"🎉 **আপনার বিজ্ঞাপনটি সফলভাবে {TARGET_CHANNEL} চ্যানেলে পোস্ট করা হয়েছে!** 🚀")
        bot.edit_message_text(f"✅ অর্ডার `#{order_id}` অনুমোদিত এবং চ্যানেলে পোস্ট সম্পন্ন!", call.message.chat.id, call.message.message_id)

    elif action == "no":
        c.execute("UPDATE orders SET status='REJECTED' WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()
        bot.send_message(client_id, "❌ আপনার পেমেন্ট মেলেনি। যোগাযোগ: @" + ADMIN_USERNAME)
        bot.edit_message_text(f"❌ অর্ডার `#{order_id}` বাতিল করা হয়েছে!", call.message.chat.id, call.message.message_id)

if __name__ == '__main__':
    keep_alive()
    try:
        bot.remove_webhook()
        time.sleep(1)
    except Exception:
        pass
    print("Bot Active", flush=True)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=10, long_polling_timeout=10)
        except Exception:
            time.sleep(3)
