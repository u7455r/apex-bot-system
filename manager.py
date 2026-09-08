import os
import sys
import time
import sqlite3
import telebot
from telebot import types
from keep_alive import keep_alive

print("--- Launching High-Converting Premium Ads Engine ---", flush=True)

BOT_TOKEN = "8967415594:AAG6uceO3FPSPKkbPm8X6xFjA_NHA9UHoIU"
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

# আকর্ষণীয় অফার প্যাকেজ তালিকা
AD_PACKAGES = {
    "pkg1": {"name": "⚡ ১টি ইনস্ট্যান্ট চ্যানেল পোস্ট", "price": "৫০ ৳", "desc": "দ্রুত চ্যানেল গ্রোথের জন্য সেরা"},
    "pkg2": {"name": "📌 ২৪ ঘণ্টা ভিআইপি পিন পোস্ট", "price": "১০০ ৳", "desc": "টপ ভিউ ও সর্বোচ্চ মেম্বার নিশ্চিত"},
    "pkg3": {"name": "🔥 ৩ দিনের মেগা পাওয়ার বুস্ট", "price": "২৫০ ৳", "desc": "সবচেয়ে জনপ্রিয় & সর্বাধিক ট্রাফিক"}
}

# ==================== কীবোর্ড ডিজাইন ====================

# নিচের চারকোনা পার্মানেন্ট মেনু
def get_bottom_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🚀 বিজ্ঞাপন বুক করুন"),
        types.KeyboardButton("💳 নগদ পেমেন্ট তথ্য")
    )
    markup.add(
        types.KeyboardButton("📜 প্রিমিয়াম নীতিমালা"),
        types.KeyboardButton("👑 ওনার ডিরেক্ট সাপোর্ট")
    )
    return markup

# ইনলাইন ড্যাশবোর্ড
def get_clean_dashboard():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("🔥 সেরা বিজ্ঞাপন প্যাকেজ ও রেট দেখুন 📊", callback_data="view_packages"))
    m.add(types.InlineKeyboardButton("💳 ইনস্ট্যান্ট নগদ পেমেন্ট গেটওয়ে ⚡", callback_data="view_payment"))
    m.add(types.InlineKeyboardButton("📢 আমাদের মূল চ্যানেল ভিজিট করুন ↗", url=REQ_CHANNEL_LINK))
    m.add(types.InlineKeyboardButton("👑 ওনার ইনবক্স (@rafimhossen) 💬", url=f"https://t.me/{ADMIN_USERNAME}"))
    return m

# ব্যাক বাটন
def get_back_button():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("⬅️ প্রধান মেনুতে ফিরে যান (Home)", callback_data="go_home"))
    return m

# ==================== মূল হ্যান্ডলার ====================
@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    u_name = message.from_user.first_name
    welcome_text = (
        f"👑 **স্বাগতম, {u_name}!** ✨\n\n"
        f"🎯 আপনার টেলিগ্রাম চ্যানেল, গ্রুপ কিংবা অনলাইন বিজনেসকে নিমেষেই বড় করতে চান?\n"
        f"📢 আমাদের হাই-অ্যাক্টিভ চ্যানেল **{TARGET_CHANNEL}**-এ প্রতিদিন হাজার হাজার মানুষের কাছে বিজ্ঞাপন পৌঁছানোর এটাই সেরা সুযোগ! 🚀\n\n"
        "👇 **নিজের সুবিধাজনক অপশনটি বেছে নিতে নিচের বাটনে চাপ দিন:**"
    )
    bot.send_message(message.chat.id, "🔘 মেনু প্যানেল লোড হয়েছে", reply_markup=get_bottom_keyboard())
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_clean_dashboard(), parse_mode='Markdown')

# পার্মানেন্ট কীবোর্ড রেসপন্স
@bot.message_handler(func=lambda msg: msg.text in [
    "🚀 বিজ্ঞাপন বুক করুন", "💳 নগদ পেমেন্ট তথ্য", "📜 প্রিমিয়াম নীতিমালা", "👑 ওনার ডিরেক্ট সাপোর্ট"
])
def handle_menu_options(message):
    txt = message.text

    if txt == "🚀 বিজ্ঞাপন বুক করুন":
        show_packages(message.chat.id)
    elif txt == "💳 নগদ পেমেন্ট তথ্য":
        show_payment_info(message.chat.id)
    elif txt == "📜 প্রিমিয়াম নীতিমালা":
        show_rules_info(message.chat.id)
    elif txt == "👑 ওনার ডিরেক্ট সাপোর্ট":
        m = types.InlineKeyboardMarkup()
        m.add(types.InlineKeyboardButton("💬 ওনারের ইনবক্সে মেসেজ দিন ↗", url=f"https://t.me/{ADMIN_USERNAME}"))
        bot.send_message(
            message.chat.id,
            f"👑 **ডিরেক্ট ভিআইপি সাপোর্ট:**\n\nযেকোনো জরুরি জিজ্ঞাসা, কাস্টম ডিল বা সহায়তার জন্য সরাসরি ওনারকে ইনবক্স করুন:\n👉 @{ADMIN_USERNAME}",
            reply_markup=m,
            parse_mode='Markdown'
        )

# ==================== তথ্যবহুল পেজসমূহ ====================
def show_packages(chat_id, message_id=None):
    m = types.InlineKeyboardMarkup(row_width=1)
    for k, v in AD_PACKAGES.items():
        m.add(types.InlineKeyboardButton(f"{v['name']} ➔ {v['price']}", callback_data=f"buy_{k}"))
    m.add(types.InlineKeyboardButton("⬅️ প্রধান মেনুতে ফিরে যান (Home)", callback_data="go_home"))

    text = (
        f"💎 **{TARGET_CHANNEL} অফিশিয়াল প্রমোশন ডিলস** 💎\n\n"
        "⚡ **প্যাকেজ তালিকা ও স্পেশাল অফার:**\n\n"
        "১️⃣ **১টি সাধারণ পোস্ট:** মাত্র ৫০ ৳\n"
        "└ 🎯 *স্ট্যান্ডার্ড রিচ ও দ্রুত সাবস্ক্রাইবার বৃদ্ধির জন্য।*\n\n"
        "২️⃣ **২৪ ঘণ্টা ভিআইপি পিন পোস্ট:** মাত্র ১০০ ৳\n"
        "└ 📌 *পোস্ট সবার উপরে পিন থাকবে, যাতে কেউ মিস না করে! (বেস্ট চয়েস)*\n\n"
        "৩️⃣ **৩ দিনের মেগা পাওয়ার বুস্ট:** মাত্র ২৫০ ৳\n"
        "└ 🔥 *একটানা ৩ দিন সর্বোচ্চ মেম্বার ও সেলস ড্রাইভ করার সেরা সুযোগ!*\n\n"
        "👇 **যে প্যাকেজটি বুক করতে চান, নিচের বাটনে আলতো চাপ দিন:**"
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
        "💳 **অফিশিয়াল নগদ পার্সোনাল গেটওয়ে** ⚡\n\n"
        f"📱 **নগদ নম্বর (Personal):**\n"
        f"👉 `{NAGAD_NUMBER}` 👈 *(কপি করতে নম্বরে ট্যাপ করুন)*\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "✨ **পেমেন্ট করার সহজ ধাপসমূহ:**\n"
        "১. নগদ অ্যাপ বা ডায়াল কোড থেকে উপরের নম্বরে **Send Money** করুন।\n"
        "২. টাকা সফলভাবে যাওয়ার পর এসএমএস থেকে প্রাপ্ত **TrxID** টি কপি করে রাখুন।\n"
        "৩. বিজ্ঞাপন বুকিংয়ের সময় TrxID টি বটে সেন্ড করে দিলেই ওনার দ্রুত অ্যাপ্রুভ করে দেবেন।\n"
        "━━━━━━━━━━━━━━━━━━━"
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
        "📜 **বিজ্ঞাপনের গুরুত্বপূর্ণ নীতিমালা** 🛡️\n\n"
        "🔹 **১.** কোনো প্রকার বেআইনি, ১৮+ বা বিভ্রান্তিকর স্ক্যাম পোস্ট অনুমোদিত নয়।\n"
        "🔹 **২.** টাকা পাঠানোর পর সঠিক TrxID সাবমিট করতে হবে, ভুল তথ্যে অর্ডার বাতিল হবে।\n"
        "🔹 **৩.** ওনার নগদ যাচাই করার পর বিজ্ঞাপনটি স্বয়ংক্রিয়ভাবে চ্যানেলে পোস্ট করে পিন করে দেবেন।\n\n"
        "🤝 সততা ও বিশ্বস্ততার সাথে এগিয়ে চলাই আমাদের লক্ষ্য!"
    )
    bot.send_message(chat_id, text, reply_markup=get_back_button(), parse_mode='Markdown')

# ==================== ইনলাইন কলব্যাক হ্যান্ডলার ====================
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
            f"👑 **স্বাগতম, {call.from_user.first_name}!** ✨\n\n"
            f"🎯 আপনার টেলিগ্রাম চ্যানেল বা প্রজেক্ট প্রমোশন করতে নিচের যেকোনো অপশন ব্যবহার করুন:\n"
            f"📢 অফিসিয়াল চ্যানেল: **{TARGET_CHANNEL}**"
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
            f"🎯 আপনি বেছে নিয়েছেন: **{pkg['name']}**\n\n"
            "✍️ **বিজ্ঞাপনের কনটেন্ট পাঠান:**\n"
            "আপনার বিজ্ঞাপনের পুরো লেখা ও লিংক (অথবা ছবি সহ ক্যাপশন) লিখে এই ইনবক্সে সেন্ড করুন:",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, step_receive_ad_content, pkg_key)
    elif data.startswith(("post_ok_", "post_no_")):
        handle_owner_decision(call)

# ==================== কনটেন্ট ও TrxID গ্রহণ ====================
def step_receive_ad_content(message, pkg_key):
    ad_text = message.text or message.caption or ""
    photo_id = message.photo[-1].file_id if message.photo else None

    if not ad_text and not photo_id:
        bot.reply_to(message, "⚠️ বিজ্ঞাপনের কোনো কনটেন্ট পাওয়া যায়নি! অনুগ্রহ করে পুনরায় /start দিন।")
        return

    pkg = AD_PACKAGES[pkg_key]
    pay_prompt = (
        "🎉 **বিজ্ঞাপন সাবমিট সফল হয়েছে!**\n\n"
        f"📦 প্যাকেজ: **{pkg['name']}**\n"
        f"💵 ফি: **{pkg['price']}**\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"📱 নগদ পার্সোনাল নম্বর: `{NAGAD_NUMBER}` *(ট্যাপ করলেই কপি)*\n"
        f"💸 সেন্ড মানি করুন: **{pkg['price']}**\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "টাকা পাঠানো শেষ হলে নগদ থেকে আসা **TrxID (Transaction ID)** টি নিচে মেসেজ করুন:"
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

    bot.reply_to(message, "✅ **আপনার পেমেন্ট রিকোয়েস্ট জমা হয়েছে!**\n\nঅ্যাডমিন নগদ যাচাই করার সাথে সাথেই পোস্ট স্বয়ংক্রিয়ভাবে চ্যানেলে লাইভ হয়ে যাবে। ধন্যবাদ! 💖")

    # ওনারের ইনবক্সে প্রিভিউ ও অনুমোদন বাটন
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("✅ এক ক্লিকে অনুমোদন ও পোস্ট", callback_data=f"post_ok_{order_id}"),
        types.InlineKeyboardButton("❌ বাতিল", callback_data=f"post_no_{order_id}")
    )

    alert = (
        "🚨 **নতুন প্রিমিয়াম বিজ্ঞাপন বুকিং এসেছে!**\n\n"
        f"🆔 অর্ডার নম্বর: `#{order_id}`\n"
        f"👤 ক্লায়েন্ট: {u_name}\n"
        f"📦 প্যাকেজ: **{pkg_name}**\n"
        f"🧾 নগদ TrxID: `{trx_id}`\n\n"
        "👇 **পোস্ট প্রিভিউ নিচে দেখুন:**"
    )
    bot.send_message(ADMIN_USER_ID, alert, parse_mode='Markdown')

    if photo_id:
        bot.send_photo(ADMIN_USER_ID, photo_id, caption=ad_text, reply_markup=m)
    else:
        bot.send_message(ADMIN_USER_ID, f"📄 **ক্যাপশন:**\n{ad_text}", reply_markup=m)

# ==================== ওনার অনুমোদন হ্যান্ডলিং ====================
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
        bot.answer_callback_query(call.id, "এই অর্ডারটি ইতিমধ্যে সম্পন্ন বা বাতিল হয়েছে!")
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
            bot.send_message(ADMIN_USER_ID, f"⚠️ চ্যানেলে পোস্ট করতে ত্রুটি: {e}")

        bot.send_message(client_id, f"🎉 **অভিনন্দন! আপনার বিজ্ঞাপনটি সফলভাবে {TARGET_CHANNEL} চ্যানেলে পোস্ট করা হয়েছে!** 🚀")
        bot.edit_message_text(f"✅ অর্ডার `#{order_id}` অনুমোদিত এবং চ্যানেলে পোস্ট সম্পন্ন!", call.message.chat.id, call.message.message_id)

    elif action == "no":
        c.execute("UPDATE orders SET status='REJECTED' WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

        bot.send_message(client_id, "❌ আপনার পেমেন্ট তথ্যে অসঙ্গতি থাকায় বিজ্ঞাপনটি বাতিল করা হয়েছে। প্রয়োজনে যোগাযোগ করুন: @" + ADMIN_USERNAME)
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
    print(f"Premium High-Converting Engine Live: @{bot_info.username}", flush=True)

    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=10, long_polling_timeout=10)
        except Exception as e:
            time.sleep(3)
