import requests
import telebot, time
from telebot import types
from telebot.types import LabeledPrice
from gatet import Tele  # تأكد أن ملف gatet.py مرفوع بجانب هذا الملف
import os
import json
from flask import Flask
from threading import Thread

# ==========================================
# 1. كود السيرفر الوهمي (Render Fix)
# هذا الجزء هو المسؤول عن إبقاء البوت يعمل على Render
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "<b>Telegram Bot is Running... 🚀</b>"

def run():
    # Render يعين منفذ (Port) تلقائياً، هذا الكود يستقبله
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. إعدادات البوت والملفات
# ==========================================

TOKEN = '8305232757:AAF-rxugmGHIbpIqiGlWFO27jZGY9Uh4CtA' 
ADMIN_ID = 7170023644 
REQUIRED_CHANNEL = "@freecrunchyrollaccountt" 
WELCOME_IMAGE_PATH = "welcome.jpg" # يجب رفع الصورة بهذا الاسم بجانب الملف

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

USERS_FILE = "users_data.json"
LANG_FILE = "users_lang.json"

# ================= TEXTS / النصوص =================
TEXTS = {
    "ar": {
        "welcome": """
✨ <b>أهلاً بك عزيزي {name} {username} 👋</b>

🤖 <b>Credit Card Checker</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
✅ <b>البوت الأفضل لفحص الكومبو واستخراج البطاقات الصالحة.</b>

💎 <b>رصيدك الحالي:</b> <code>{points}</code> نقطة

👇 <b>اختر من القائمة الرئيسية:</b>
""",
        "btn_dev": "المطور 👨‍💻",
        "btn_buy": "شراء نقاط 💎",
        "btn_check": "رصيدي 💰",
        "btn_lang": "Language 🌐",
        "btn_cmds": "الأوامر 📜",
        "btn_back": "رجوع 🔙",
        "points_msg": "💰 <b>رصيدك الحالي هو:</b> <code>{pts}</code> نقطة.",
        "wait": "<b>جاري البدء... يرجى الانتظار ⌛</b>",
        "no_points": "⛔ <b>عذراً، رصيدك غير كافٍ!</b>\nتحتاج إلى <code>{total}</code> نقطة.",
        "stop": "إيقاف الفحص 🛑",
        "choose_lang": "<b>Please choose your language:\nالرجاء اختيار لغتك لبدء الاستخدام:</b>",
        "must_join_msg": f"⛔ <b>عذراً عزيزي</b>\n\nيجب عليك الاشتراك في قناة المطور أولاً لاستخدام البوت.\n\nاشترك ثم اضغط على زر <b>'تحقق من الاشتراك'</b>.",
        "btn_join_channel": "اشتراك في القناة 📢",
        "btn_verify_sub": "✅ تحقق من الاشتراك",
        "sub_not_found": "❌ لم تقم بالاشتراك في القناة بعد. حاول مجدداً.",
        "sub_confirmed": "✅ تم التحقق من اشتراكك. أهلاً بك!",
        "cmds_msg": """
📜 <b>قائمة الأوامر المتاحة:</b>

1️⃣ <b>/start</b>
➜ لبدء البوت وعرض القائمة الرئيسية.

2️⃣ <b>/points</b>
➜ لعرض عدد نقاطك الحالية.

3️⃣ <b>/chk cc|mm|yy|cvv</b>
➜ لفحص بطاقة واحدة بسرعة (تكلفة 1 نقطة).
مثال: <code>/chk 444444444444|01|26|123</code>

4️⃣ <b>إرسال ملف</b>
➜ أرسل ملف كومبو (txt) لفحصه بالكامل.
""",
        "chk_usage": "⚠️ <b>طريقة الاستخدام خطأ!</b>\nأرسل الأمر مع البطاقة هكذا:\n<code>/chk XXXXXXXXXXXXXXXX|MM|YY|CVV</code>",
        "processing_one": "⚡ <b>جاري فحص البطاقة...</b>\n<code>{cc}</code>",
        
        "buy_title": "💎 <b>قائمة شراء النقاط</b>\nاختر العرض المناسب لك، يمكنك الدفع مباشرة عبر نجوم تليجرام (Stars) أو التواصل مع المطور.",
        "btn_contact": "تواصل مع المطور 👨‍💻",
        "buy_success": "✅ <b>تم الدفع بنجاح!</b>\nتمت إضافة <code>{amount}</code> نقطة إلى رصيدك.\nرصيدك الحالي: {balance}",
        "buy_desc_100": "شراء 100 نقطة فحص",
        "buy_desc_200": "شراء 200 نقطة (تخفيض 25%)",
        "buy_desc_500": "شراء 500 نقطة (تخفيض VIP)"
    },
    "en": {
        "welcome": """
✨ <b>Welcome Dear {name} {username} 👋</b>

🤖 <b>Credit Card Checker</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
✅ <b>The best bot for checking combos and filtering valid cards.</b>

💎 <b>Your Balance:</b> <code>{points}</code> Points

👇 <b>Select from the main menu:</b>
""",
        "btn_dev": "Developer 👨‍💻",
        "btn_buy": "Buy Points 💎",
        "btn_check": "Balance 💰",
        "btn_lang": "اللغة 🌐",
        "btn_cmds": "Commands 📜",
        "btn_back": "Back 🔙",
        "points_msg": "💰 <b>Your current balance:</b> <code>{pts}</code> points.",
        "wait": "<b>Starting... Please wait ⌛</b>",
        "no_points": "⛔ <b>Sorry, Insufficient points!</b>\nYou need <code>{total}</code> points.",
        "stop": "STOP CHECK 🛑",
        "choose_lang": "<b>Please choose your language:\nالرجاء اختيار لغتك لبدء الاستخدام:</b>",
        "must_join_msg": f"⛔ <b>Sorry Dear</b>\n\nYou must subscribe to the developer's channel first to use the bot.\n\nSubscribe and then press <b>'Verify Subscription'</b>.",
        "btn_join_channel": "Join Channel 📢",
        "btn_verify_sub": "✅ Verify Subscription",
        "sub_not_found": "❌ You haven't subscribed yet. Please try again.",
        "sub_confirmed": "✅ Subscription verified. Welcome!",
        "cmds_msg": """
📜 <b>Available Commands:</b>

1️⃣ <b>/start</b>
➜ To start the bot and show the menu.

2️⃣ <b>/points</b>
➜ To check your current balance.

3️⃣ <b>/chk cc|mm|yy|cvv</b>
➜ To check a single card (Costs 1 Point).
Ex: <code>/chk 444444444444|01|26|123</code>

4️⃣ <b>Send File</b>
➜ Send a combo file (txt) to check bulk.
""",
        "chk_usage": "⚠️ <b>Wrong Usage!</b>\nUse command like this:\n<code>/chk XXXXXXXXXXXXXXXX|MM|YY|CVV</code>",
        "processing_one": "⚡ <b>Checking card...</b>\n<code>{cc}</code>",

        "buy_title": "💎 <b>Buy Points Menu</b>\nChoose a package below. Pay instantly via Telegram Stars or contact the developer.",
        "btn_contact": "Contact Developer 👨‍💻",
        "buy_success": "✅ <b>Payment Successful!</b>\nAdded <code>{amount}</code> points to your account.\nCurrent Balance: {balance}",
        "buy_desc_100": "Buy 100 Check Points",
        "buy_desc_200": "Buy 200 Points (25% OFF)",
        "buy_desc_500": "Buy 500 Points (VIP Deal)"
    }
}

# ================= DATA FUNCTIONS =================
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def get_points(user_id):
    data = load_json(USERS_FILE)
    return data.get(str(user_id), 0)

def add_points(user_id, pts):
    data = load_json(USERS_FILE)
    uid = str(user_id)
    data[uid] = data.get(uid, 0) + pts
    if data[uid] < 0: data[uid] = 0
    save_json(USERS_FILE, data)

def get_lang(user_id):
    data = load_json(LANG_FILE)
    return data.get(str(user_id), "en") 

def set_lang(user_id, lang_code):
    data = load_json(LANG_FILE)
    data[str(user_id)] = lang_code
    save_json(LANG_FILE, data)

def check_subscription(user_id):
    try:
        status = bot.get_chat_member(REQUIRED_CHANNEL, user_id).status
        if status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        return False

# ================= HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        show_force_sub_message(message.chat.id, user_id)
        return 
    pts_data = load_json(USERS_FILE)
    if str(user_id) not in pts_data:
        add_points(user_id, 0)
    lang_data = load_json(LANG_FILE)
    if str(user_id) in lang_data:
        show_main_menu(message.chat.id, user_id, message.from_user.first_name, message.from_user.username)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_ar = types.InlineKeyboardButton("العربية 🇩🇿", callback_data="set_lang_ar")
        btn_en = types.InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en")
        markup.add(btn_ar, btn_en)
        bot.send_message(message.chat.id, TEXTS["en"]["choose_lang"], reply_markup=markup)

def show_main_menu(chat_id, user_id, first_name, username_raw):
    lang = get_lang(user_id)
    t = TEXTS[lang]
    points = get_points(user_id)
    user_tag = f"(@{username_raw})" if username_raw else ""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(t["btn_dev"], url="https://t.me/aymen_1144")
    btn2 = types.InlineKeyboardButton(t["btn_buy"], callback_data="buy_menu") 
    btn3 = types.InlineKeyboardButton(t["btn_check"], callback_data="check_pts")
    btn4 = types.InlineKeyboardButton(t["btn_lang"], callback_data="change_lang")
    btn5 = types.InlineKeyboardButton(t["btn_cmds"], callback_data="show_cmds") 
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    caption = t["welcome"].format(name=first_name, username=user_tag, points=points)
    try:
        with open(WELCOME_IMAGE_PATH, 'rb') as photo_file:
             bot.send_photo(chat_id, photo_file, caption=caption, reply_markup=markup)
    except:
        bot.send_message(chat_id, caption, reply_markup=markup)

def show_force_sub_message(chat_id, user_id):
    lang = get_lang(user_id)
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup()
    channel_url = f"https://t.me/{REQUIRED_CHANNEL.replace('@','')}"
    btn_join = types.InlineKeyboardButton(t["btn_join_channel"], url=channel_url)
    btn_verify = types.InlineKeyboardButton(t["btn_verify_sub"], callback_data="verify_sub")
    markup.add(btn_join)
    markup.add(btn_verify)
    bot.send_message(chat_id, t["must_join_msg"], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'verify_sub')
def verify_sub_callback(call):
    user_id = call.from_user.id
    lang = get_lang(user_id)
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, TEXTS[lang]["sub_confirmed"], show_alert=False)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)
    else:
        bot.answer_callback_query(call.id, TEXTS[lang]["sub_not_found"], show_alert=True)

# ---------------- COMMANDS & PAYMENTS ----------------
@bot.callback_query_handler(func=lambda call: call.data == 'buy_menu')
def show_buy_menu(call):
    lang = get_lang(call.from_user.id)
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_100 = types.InlineKeyboardButton(f"100 Points (50 ⭐️)", callback_data="pay_50")
    btn_200 = types.InlineKeyboardButton(f"200 Points (75 ⭐️) 🏷", callback_data="pay_75")
    btn_500 = types.InlineKeyboardButton(f"500 Points (150 ⭐️) 🔥", callback_data="pay_150")
    btn_contact = types.InlineKeyboardButton(t["btn_contact"], url="https://t.me/aymen_1144")
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main")
    markup.add(btn_100, btn_200, btn_500, btn_contact, btn_back)
    try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["buy_title"], reply_markup=markup)
    except:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=t["buy_title"], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def send_invoice_handler(call):
    amount_stars = int(call.data.split('_')[1])
    lang = get_lang(call.from_user.id)
    t = TEXTS[lang]
    if amount_stars == 50: points = 100; description = t["buy_desc_100"]
    elif amount_stars == 75: points = 200; description = t["buy_desc_200"]
    elif amount_stars == 150: points = 500; description = t["buy_desc_500"]
    else: return
    bot.send_invoice(
        chat_id=call.message.chat.id,
        title=f"{points} Points",
        description=description,
        invoice_payload=f"points_{points}_{call.from_user.id}",
        provider_token="", currency="XTR",
        prices=[LabeledPrice(label=f"{points} Points", amount=amount_stars)],
        start_parameter="buy_points"
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    lang = get_lang(message.from_user.id)
    t = TEXTS[lang]
    payment_info = message.successful_payment
    amount_paid = payment_info.total_amount
    payload = payment_info.invoice_payload
    try: points_to_add = int(payload.split('_')[1])
    except:
        if amount_paid == 50: points_to_add = 100
        elif amount_paid == 75: points_to_add = 200
        elif amount_paid == 150: points_to_add = 500
        else: points_to_add = 0
    if points_to_add > 0:
        add_points(message.from_user.id, points_to_add)
        new_balance = get_points(message.from_user.id)
        bot.reply_to(message, t["buy_success"].format(amount=points_to_add, balance=new_balance))
        try:
            user_tag = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
            bot.send_message(ADMIN_ID, f"💰 <b>عملية شراء!</b>\n👤 {user_tag}\n⭐️ {amount_paid} Stars\n💎 {points_to_add} Pts")
        except: pass

@bot.message_handler(commands=["cmds", "help"])
def commands_handler(message):
    if not check_subscription(message.from_user.id):
        show_force_sub_message(message.chat.id, message.from_user.id)
        return
    lang = get_lang(message.from_user.id)
    bot.reply_to(message, TEXTS[lang]["cmds_msg"])

@bot.callback_query_handler(func=lambda call: call.data == 'show_cmds')
def show_cmds_callback(call):
    lang = get_lang(call.from_user.id)
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main")
    markup.add(btn_back)
    try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["cmds_msg"], reply_markup=markup)
    except:
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=t["cmds_msg"], reply_markup=markup)
        except: pass

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def back_to_main_callback(call):
    user_id = call.from_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    points = get_points(user_id)
    username_raw = call.from_user.username
    user_tag = f"(@{username_raw})" if username_raw else ""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(t["btn_dev"], url="https://t.me/aymen_1144")
    btn2 = types.InlineKeyboardButton(t["btn_buy"], callback_data="buy_menu") 
    btn3 = types.InlineKeyboardButton(t["btn_check"], callback_data="check_pts")
    btn4 = types.InlineKeyboardButton(t["btn_lang"], callback_data="change_lang")
    btn5 = types.InlineKeyboardButton(t["btn_cmds"], callback_data="show_cmds") 
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    caption = t["welcome"].format(name=call.from_user.first_name, username=user_tag, points=points)
    try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption, reply_markup=markup)
    except:
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=caption, reply_markup=markup)
        except:
            show_main_menu(call.message.chat.id, user_id, call.from_user.first_name, username_raw)

@bot.message_handler(commands=["chk"])
def single_check_handler(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        show_force_sub_message(message.chat.id, user_id)
        return
    lang = get_lang(user_id)
    t = TEXTS[lang]
    try: cc_data = message.text.split(" ", 1)[1]
    except IndexError:
        bot.reply_to(message, t["chk_usage"])
        return
    if get_points(user_id) < 1:
        bot.reply_to(message, t["no_points"].format(total=1))
        return
    ko = bot.reply_to(message, t["processing_one"].format(cc=cc_data)).message_id
    add_points(user_id, -1)
    try:
        try: req = requests.get('https://bins.antipublic.cc/bins/'+cc_data[:6]).json()
        except: req = {}
        brand = req.get('brand', 'Unknown'); card_type = req.get('type', 'Unknown')
        country = req.get('country_name', 'Unknown'); country_flag = req.get('country_flag', '')
        bank = req.get('bank', 'Unknown')
        start_time = time.time()
        try: last = str(Tele(cc_data))
        except Exception as e: print(e); last = 'Error'
        execution_time = time.time() - start_time
        username_raw = message.from_user.username
        user_tag = f"@{username_raw}" if username_raw else message.from_user.first_name
        msg_template = """
✨✨ 𝐂𝐀𝐑𝐃 𝐂𝐇𝐄𝐂𝐊 𝐑𝐄𝐒𝐔𝐋𝐓 ✨✨
━━━━━━━━━━━━━━━━━━
💳 <b>𝐂𝐀𝐑𝐃</b>: <code>{cc}</code>
[ϟ] <b>𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄</b>: <code>{response}</code>
━━━━━━━━━━━━━━━━━━
🏦 <b>𝐁𝐈𝐍</b>: <code>{cc[:6]} - {card_type} - {brand}</code>
🏛 <b>𝐁𝐀𝐍𝐊</b>: <code>{bank}</code>
🌍 <b>𝐂𝐎𝐔𝐍𝐓𝐑𝐘</b>: <code>{country} {country_flag}</code>
⏱ <b>𝐓𝐈𝐌𝐄</b>: <code>{time:.1f} sec</code>
━━━━━━━━━━━━━━━━━━
👤 <b>Checked By:</b> {user_tag}
🤖 <b>Bot By:</b> @aymen_1144
"""
        if 'Donation Successful!' in last or 'Approved' in last:
            res_msg = msg_template.format(cc=cc_data, response="✅ Charged $1 🔥", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
            bot.reply_to(message, res_msg)
        elif 'insufficient funds' in last:
            res_msg = msg_template.format(cc=cc_data, response="📉 Low Funds", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
            bot.reply_to(message, res_msg)
        elif 'security code is incorrect' in last:
            res_msg = msg_template.format(cc=cc_data, response="⚠️ CCN Match", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
            bot.reply_to(message, res_msg)
        elif 'Your card does not support' in last:
            res_msg = msg_template.format(cc=cc_data, response="⚠️ CVV Error", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
            bot.reply_to(message, res_msg)
        else:
            res_msg = msg_template.format(cc=cc_data, response="❌ Declined", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=res_msg)
    except Exception as e:
        print(f"Error in single check: {e}")
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="❌ Error checking card.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def language_selection(call):
    if not check_subscription(call.from_user.id):
         bot.delete_message(call.message.chat.id, call.message.message_id)
         show_force_sub_message(call.message.chat.id, call.from_user.id)
         return
    lang_code = call.data.split("_")[2]
    set_lang(call.from_user.id, lang_code)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_main_menu(call.message.chat.id, call.from_user.id, call.from_user.first_name, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data == 'change_lang')
def change_lang_btn(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_ar = types.InlineKeyboardButton("العربية 🇩🇿", callback_data="set_lang_ar")
    btn_en = types.InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en")
    markup.add(btn_ar, btn_en)
    bot.send_message(call.message.chat.id, TEXTS["en"]["choose_lang"], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'check_pts')
def check_points_btn(call):
    lang = get_lang(call.from_user.id)
    pts = get_points(call.from_user.id)
    bot.answer_callback_query(call.id, show_alert=True, text=TEXTS[lang]["points_msg"].format(pts=pts))

@bot.message_handler(commands=["points"])
def points_cmd(message):
    if not check_subscription(message.from_user.id):
        show_force_sub_message(message.chat.id, message.from_user.id)
        return
    lang = get_lang(message.from_user.id)
    pts = get_points(message.from_user.id)
    bot.reply_to(message, TEXTS[lang]["points_msg"].format(pts=pts))

@bot.message_handler(commands=["give"])
def give_cmd(message):
    if message.from_user.id != ADMIN_ID: return
    parts = message.text.split()
    if len(parts) != 3:
        bot.reply_to(message, "Usage: /give user_id points")
        return
    try:
        uid = int(parts[1]); pts = int(parts[2])
        add_points(uid, pts)
        bot.reply_to(message, f"✅ Done. Added {pts} points to {uid}")
    except: bot.reply_to(message, "Error in format.")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    with open("stop.stop", "w") as file: pass

@bot.message_handler(content_types=["document"])
def main(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        show_force_sub_message(message.chat.id, user_id)
        return
    lang = get_lang(user_id)
    t = TEXTS[lang]
    username_raw = message.from_user.username
    user_tag = f"@{username_raw}" if username_raw else message.from_user.first_name
    ko = bot.reply_to(message, t["wait"]).message_id
    try:
        ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
        with open("combo.txt", "wb") as w: w.write(ee)
    except:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="❌ Error downloading file.")
        return
    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            if get_points(user_id) < total:
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=t["no_points"].format(total=total))
                return
            add_points(user_id, -total)
            ch = 0; ccn = 0; cvv = 0; lowfund = 0; dd = 0
            mes = types.InlineKeyboardMarkup(row_width=1)
            status_btn = types.InlineKeyboardButton(f"• Waiting... •", callback_data='x')
            cm3 = types.InlineKeyboardButton(f"✅ LIVE : [ {ch} ]", callback_data='x')
            cm4 = types.InlineKeyboardButton(f"⚠️ CCN : [ {ccn} ]", callback_data='x')
            cm5 = types.InlineKeyboardButton(f"⚠️ CVV : [ {cvv} ]", callback_data='x')
            cm6 = types.InlineKeyboardButton(f"📉 LOW : [ {lowfund} ]", callback_data='x')
            cm7 = types.InlineKeyboardButton(f"❌ DEAD : [ {dd} ]", callback_data='x')
            cm8 = types.InlineKeyboardButton(f"📊 TOTAL : [ {total} ]", callback_data='x')
            stop_btn = types.InlineKeyboardButton(t["stop"], callback_data='stop')
            mes.add(status_btn, cm3, cm4, cm5, cm6, cm7, cm8, stop_btn)
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="⚡ Processing...", reply_markup=mes)
            for cc in lino:
                if os.path.exists('stop.stop'):
                    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='🛑 STOPPED BY USER')
                    os.remove('stop.stop')
                    return
                try: data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
                except: data = {}
                brand = data.get('brand', 'Unknown'); card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown'); country_flag = data.get('country_flag', '')
                bank = data.get('bank', 'Unknown')
                start_time = time.time()
                try: last = str(Tele(cc))
                except Exception as e: print(e); last = 'Error'
                execution_time = time.time() - start_time
                mes = types.InlineKeyboardMarkup(row_width=1)
                status_btn = types.InlineKeyboardButton(f"• {cc[:6]}****** ➜ {last} •", callback_data='x')
                cm3 = types.InlineKeyboardButton(f"✅ LIVE : [ {ch} ]", callback_data='x')
                cm4 = types.InlineKeyboardButton(f"⚠️ CCN : [ {ccn} ]", callback_data='x')
                cm5 = types.InlineKeyboardButton(f"⚠️ CVV : [ {cvv} ]", callback_data='x')
                cm6 = types.InlineKeyboardButton(f"📉 LOW : [ {lowfund} ]", callback_data='x')
                cm7 = types.InlineKeyboardButton(f"❌ DEAD : [ {dd} ]", callback_data='x')
                cm8 = types.InlineKeyboardButton(f"📊 TOTAL : [ {total} ]", callback_data='x')
                stop_btn = types.InlineKeyboardButton(t["stop"], callback_data='stop')
                mes.add(status_btn, cm3, cm4, cm5, cm6, cm7, cm8, stop_btn)
                try:
                    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=ko, reply_markup=mes)
                except: pass
                msg_template = """
✨✨ 𝐂𝐀𝐑𝐃 𝐂𝐇𝐄𝐂𝐊 𝐑𝐄𝐒𝐔𝐋𝐓 ✨✨
━━━━━━━━━━━━━━━━━━
💳 <b>𝐂𝐀𝐑𝐃</b>: <code>{cc}</code>
[ϟ] <b>𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄</b>: <code>{response}</code>
━━━━━━━━━━━━━━━━━━
🏦 <b>𝐁𝐈𝐍</b>: <code>{cc[:6]} - {card_type} - {brand}</code>
🏛 <b>𝐁𝐀𝐍𝐊</b>: <code>{bank}</code>
🌍 <b>𝐂𝐎𝐔𝐍𝐓𝐑𝐘</b>: <code>{country} {country_flag}</code>
⏱ <b>𝐓𝐈𝐌𝐄</b>: <code>{time:.1f} sec</code>
━━━━━━━━━━━━━━━━━━
👤 <b>Checked By:</b> {user_tag}
🤖 <b>Bot By:</b> @aymen_1144
"""
                if 'Donation Successful!' in last or 'Approved' in last:
                    ch += 1
                    res_msg = msg_template.format(cc=cc, response="✅ Charged $1 🔥", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
                    bot.reply_to(message, res_msg)
                elif 'insufficient funds' in last:
                    lowfund += 1
                    res_msg = msg_template.format(cc=cc, response="📉 Low Funds", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
                    bot.reply_to(message, res_msg)
                elif 'security code is incorrect' in last: ccn += 1
                elif 'Your card does not support' in last: cvv += 1
                else: dd += 1
                time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "❌ حدث خطأ أثناء قراءة الملف.")
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='✅ CHECK COMPLETED | انتهى الفحص\n🤖 DEV: @aymen_1144')

if __name__ == "__main__":
    print("🤖 Bot started...")
    keep_alive() # تشغيل السيرفر الوهمي هنا لكي لا يتوقف البوت
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
