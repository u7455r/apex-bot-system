import os
import sys
import time
import sqlite3
import telebot
from telebot import types
from keep_alive import keep_alive

print("--- Starting Zero-Module Pure Ads Engine ---", flush=True)

BOT_TOKEN = "8967415594:AAEA95JmGE_IRSZH_qDlLqjUQ6Pa6siwc_I"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

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
    conn.commit()
    conn.close()

init_db()

# প্যাকেজ তালিকা
AD_PACKAGES = {
    "pkg1": {"name": "📢 ১টি সাধারণ চ্যানেল পোস্ট", "price": "৫০ টাকা"},
    "pkg2": {"name": "📌 ২৪ ঘণ্টার পিন পোস্ট", "price": "১০০ টাকা"},
    "pkg3": {"name": "🔥 ৩ দিনের মেগা প্রমোশন", "price": "২৫০ টাকা"}
}

# ==================== কীবোর্ড ডিজাইন ====================
def get_bottom_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("📢 বিজ্ঞাপন দিন"), types.KeyboardButton("💳 নগদ পেমেন্ট তথ্য"))
    markup.add(types.KeyboardButton("📜 নীতিমালা"), types.KeyboardButton("👨‍💻 ওনার সাপোর্ট (@rafimhossen)"))
    return markup

def get_clean_dashboard():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("📢 বিজ্ঞাপন প্যাকেজ দেখুন", callback_data="view_packages"))
    m.add(types.InlineKeyboardButton("💳 নগদ পেমেন্ট তথ্য", callback_data="view_payment"))
    m.add(types.InlineKeyboardButton("📢 অফিসিয়াল চ্যানেল ↗", url=REQ_CHANNEL_LINK))
    m.add(types.InlineKeyboardButton("👨‍💻 ওনার সাপোর্ট (@rafimhossen) ↗", url=f"https://t.me/{ADMIN_USERNAME}"))
    return m

def get_back_button():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("⬅️ ব্যাক মেনু (Back)", callback_data="go_home"))
    return m

# ==================== মূল হ্যান্ডলার ====================
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    welcome_text = (
        f"👋 **স্বাগতম, {message.from_user.first_name}!**\n\n"
        f"📢 আমাদের অফিসিয়াল চ্যানেল **{TARGET_CHANNEL}**-এ বিজ্ঞাপন বুক করতে নিচের অপশন ব্যবহার করুন:"
    )
    bot.send_message(message.chat.id, "কন্ট্রোল মেনু চালু করা হয়েছে 🔘", reply_markup=get_bottom_keyboard())
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_clean_dashboard(), parse_mode='Markdown')

@bot.message_handler(func=lambda msg: msg.text in [
    "📢 বিজ্ঞাপন দিন", "💳 নগদ পেমেন্ট তথ্য", "📜 নীতিমালা", "👨‍💻 ওনার সাপোর্ট (@rafimhossen)"
])
def handle_menu_options(message):
    txt = message.text

    if txt == "📢 বিজ্ঞাপন দিন":
        show_packages(message.chat.id)
    elif txt == "💳 নগদ পেমেন্ট তথ্য":
        show_payment_info(message.chat.id)
    elif txt == "📜 নীতিমালা":
        show_rules_info(message.chat.id)
    elif txt == "👨‍💻 ওনার সাপোর্ট (@rafimhossen)":
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton("💬 সরাসরি চ্যাট করুন ↗", url=f"https://t.me/{ADMIN_USERNAME}"))
        bot.send_message(
            message.chat.id,
            f"👨‍💻 **অফিশিয়াল সাপোর্ট:**\nযোগাযোগ করতে নিচের লিংকে চাপ দিন:\n👉 @{ADMIN_USERNAME}",
            reply_markup=m,
            parse_mode='Markdown'
        )

def show_packages(chat_id, message_id=None):
    m = types.InlineKeyboardMarkup(row_width=1)
    for k, v in AD_PACKAGES.items():
        m.add(types.InlineKeyboardButton(f"{v['name']} — {v['price']}", callback_data=f"buy_{k}"))
    m.add(types.InlineKeyboardButton("⬅️ ব্যাক মেনু (Back)", callback_data="go_home"))

    text = (
        f"📢 **{TARGET_CHANNEL} চ্যানেলের বিজ্ঞাপন প্যাকেজ:**\n\n"
        "যে প্যাকেজে পোস্ট করতে চান সেটি সিলেক্ট করুন:"
    )
    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=m, parse_mode='Markdown')
        except Exception:
            bot.send_message(chat_id, text, reply_markup=m, parse_mode='Markdown')
    else:
        bot.send_message(chat_id, text, reply_markup=m, parse_mode='Markdown')

def show_payment_info(chat_id, message_id=None):
    text = (
        "💳 **অফিশিয়াল নগদ পেমেন্ট তথ্য:**\n\n"
        f"📱 নগদ নম্বর (Personal): `{NAGAD_NUMBER}`\n\n"
        "💡 **নিয়মাবলী:**\n"
        "১. আপনার নগদ অ্যাকাউন্ট থেকে اوپرের নম্বরে 'Send Money' করুন।\n"
        "২. টাকা পাঠানোর পর পাওয়া TrxID বটের কাছে সাবমিট করুন।"
    )
    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=get_back_button(), parse_mode='Markdown')
        except Exception:
            bot.send_message(chat_id, text, reply_markup=get_back_button(), parse_mode='Markdown')
    else:
        bot.send_message(chat_id, text, reply_markup=get_back_button(), parse_mode='Markdown')

def show_rules_info(chat_id):
    text = (
        "📜 **বিজ্ঞাপন নীতিমালা:**\n\n"
        "১. কোনো ক্ষতিকর বা ভুয়া কনটেন্ট গ্রহণযোগ্য নয়।\n"
        "২. টাকা পাঠানোর পর সঠিক TrxID পাঠাতে হবে।\n"
        "৩. ওনার নগদ চেক করে বিজ্ঞাপনটি চ্যানেলে অনুমোদন করবেন।"
    )
    bot.send_message(chat_id, text, reply_markup=get_back_button(), parse_mode='Markdown')

# ==================== কলব্যাক হ্যান্ডলার ====================
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
        welcome_text = (
            f"👋 **স্বাগতম, {call.from_user.first_name}!**\n\n"
            f"📢 আমাদের অফিসিয়াল চ্যানেল **{TARGET_CHANNEL}**-এ বিজ্ঞাপন বুক করতে নিচের অপশন ব্যবহার করুন:"
        )
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

        msg = bot.send_message(
            chat_id,
            f"📝 আপনি সিলেক্ট করেছেন: **{pkg['name']}**\n\n"
            "এখন আপনার বিজ্ঞাপনের লেখা (ক্যাপশন ও লিংক) অথবা ছবি সহ ক্যাপশন লিখে পাঠান:",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, step_receive_ad_content, pkg_key)
    elif data.startswith(("post_ok_", "post_no_")):
        handle_owner_decision(call)

# ==================== বিজ্ঞাপন রিসিভ ও সাবমিট ====================
def step_receive_ad_content(message, pkg_key):
    ad_text = message.text or message.caption or ""
    photo_id = message.photo[-1].file_id if message.photo else None

    if not ad_text and not photo_id:
        bot.reply_to(message, "⚠️ কোনো লেখা বা ছবি পাওয়া যায়নি। অনুগ্রহ করে /start দিন।")
        return

    pkg = AD_PACKAGES[pkg_key]
    pay_prompt = (
        "💳 **বিজ্ঞাপন গ্রহণ করা হয়েছে!**\n\n"
        f"📦 প্যাকেজ: **{pkg['name']}**\n"
        f"💵 ফি: **{pkg['price']}**\n\n"
        f"১. নগদ (Personal): `{NAGAD_NUMBER}`\n"
        f"২. সেন্ড মানি করুন: **{pkg['price']}**\n\n"
        "টাকা পাঠানোর পর নগদ থেকে পাওয়া **TrxID** নিচে লিখে পাঠান:"
    )
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

    bot.reply_to(message, "✅ আপনার পেমেন্ট তথ্য জমা হয়েছে!\nওনার যাচাই করে অনুমোদন দিলেই চ্যানেলে পোস্ট হয়ে যাবে।")

    # ওনারের ইনবক্সে নোটিফিকেশন
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("✅ Approve & Post", callback_data=f"post_ok_{order_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"post_no_{order_id}")
    )

    alert = (
        "🚨 **নতুন বিজ্ঞাপন বুকিং রিকোয়েস্ট!**\n\n"
        f"🆔 অর্ডার: `#{order_id}`\n"
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

# ==================== ওনার ১-ক্লিক অনুমোদন ====================
def handle_owner_decision(call):
    if call.from_user.id != ADMIN_USER_ID:
        return

    action, order_id = call.data.split("_")[1], call.data.split("_")[2]

    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, package, ad_text, photo_id FROM orders WHERE order_id=? AND status='PENDING'", (order_id,))
    row = c.fetchone()

    if not row:
        bot.answer_callback_query(call.id, "অর্ডারটি ইতিমধ্যে সম্পন্ন বা বাতিল হয়েছে!")
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

            if "পিন" in pkg_name:
                bot.pin_chat_message(TARGET_CHANNEL, p_msg.message_id)
        except Exception as e:
            bot.send_message(ADMIN_USER_ID, f"⚠️ চ্যানেলে পোস্ট হতে সমস্যা: {e}")

        bot.send_message(client_id, f"🎉 **আপনার বিজ্ঞাপনটি সফলভাবে {TARGET_CHANNEL} চ্যানেলে পোস্ট করা হয়েছে!**")
        bot.edit_message_text(f"✅ অর্ডার `#{order_id}` Approved এবং চ্যানেলে পোস্ট সম্পন্ন!", call.message.chat.id, call.message.message_id)

    elif action == "no":
        c.execute("UPDATE orders SET status='REJECTED' WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

        bot.send_message(client_id, "❌ আপনার পেমেন্ট মেলেনি বা অর্ডার বাতিল হয়েছে। যোগাযোগ: @" + ADMIN_USERNAME)
        bot.edit_message_text(f"❌ অর্ডার `#{order_id}` বাতিল করা হয়েছে!", call.message.chat.id, call.message.message_id)

# ==================== RUNNER ====================
if __name__ == '__main__':
    keep_alive()
    try:
        bot.remove_webhook()
        time.sleep(1)
    except Exception:
        pass

    bot_info = bot.get_me()
    print(f"Zero-Module Bot Live: @{bot_info.username}", flush=True)

    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=10, long_polling_timeout=10)
        except Exception as e:
            time.sleep(3)
