import requests
import telebot, time
from telebot import types
from gatet import Tele  # تأكد أن ملف gatet.py موجود في نفس المجلد
import os
import json

# ================= SETTINGS / الإعدادات =================

TOKEN = '8305232757:AAF-rxugmGHIbpIqiGlWFO27jZGY9Uh4CtA' 
ADMIN_ID = 7170023644 

# 1. إعداد قناة الاشتراك الإجباري
REQUIRED_CHANNEL = "@dailydroppp" 

# 2. إعداد مسار الصورة (تم استخدام r قبل المسار لتجنب أخطاء ويندوز)
WELCOME_IMAGE_PATH = "welcome.jpg"

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
        "processing_one": "⚡ <b>جاري فحص البطاقة...</b>\n<code>{cc}</code>"
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
        "processing_one": "⚡ <b>Checking card...</b>\n<code>{cc}</code>"
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

# ================= MAIN MENU & UI =================
def show_main_menu(chat_id, user_id, first_name, username_raw):
    lang = get_lang(user_id)
    t = TEXTS[lang]
    points = get_points(user_id)
    user_tag = f"(@{username_raw})" if username_raw else ""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(t["btn_dev"], url="https://t.me/aymen_1144")
    btn2 = types.InlineKeyboardButton(t["btn_buy"], url="https://t.me/aymen_1144")
    btn3 = types.InlineKeyboardButton(t["btn_check"], callback_data="check_pts")
    btn4 = types.InlineKeyboardButton(t["btn_lang"], callback_data="change_lang")
    btn5 = types.InlineKeyboardButton(t["btn_cmds"], callback_data="show_cmds") 
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    caption = t["welcome"].format(name=first_name, username=user_tag, points=points)
    
    try:
        # قراءة الملف من المسار المحدد
        with open(WELCOME_IMAGE_PATH, 'rb') as photo_file:
             bot.send_photo(chat_id, photo_file, caption=caption, reply_markup=markup)
    except FileNotFoundError:
        # إذا لم يجد الصورة، يرسل رسالة نصية فقط مع طباعة تنبيه في الكونسول
        print(f"Warning: Image not found at {WELCOME_IMAGE_PATH}")
        bot.send_message(chat_id, caption, reply_markup=markup)
    except Exception as e:
        print(f"Error sending photo: {e}")
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

# ---------------- COMMANDS LIBRARY ----------------
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
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                 caption=t["cmds_msg"], reply_markup=markup)
    except:
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=t["cmds_msg"], reply_markup=markup)
        except:
            pass

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
    btn2 = types.InlineKeyboardButton(t["btn_buy"], url="https://t.me/aymen_1144")
    btn3 = types.InlineKeyboardButton(t["btn_check"], callback_data="check_pts")
    btn4 = types.InlineKeyboardButton(t["btn_lang"], callback_data="change_lang")
    btn5 = types.InlineKeyboardButton(t["btn_cmds"], callback_data="show_cmds") 
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    caption = t["welcome"].format(name=call.from_user.first_name, username=user_tag, points=points)
    
    try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                 caption=caption, reply_markup=markup)
    except:
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=caption, reply_markup=markup)
        except:
            show_main_menu(call.message.chat.id, user_id, call.from_user.first_name, username_raw)

# ---------------- SINGLE CHECKER (/chk) ----------------
@bot.message_handler(commands=["chk"])
def single_check_handler(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        show_force_sub_message(message.chat.id, user_id)
        return
    
    lang = get_lang(user_id)
    t = TEXTS[lang]
    
    try:
        cc_data = message.text.split(" ", 1)[1]
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
        elif 'insufficient funds' in last:
            res_msg = msg_template.format(cc=cc_data, response="📉 Low Funds", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
        elif 'security code is incorrect' in last:
            res_msg = msg_template.format(cc=cc_data, response="⚠️ CCN Match", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
        elif 'Your card does not support' in last:
            res_msg = msg_template.format(cc=cc_data, response="⚠️ CVV Error", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)
        else:
            res_msg = msg_template.format(cc=cc_data, response="❌ Declined", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag)

        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=res_msg)

    except Exception as e:
        print(f"Error in single check: {e}")
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="❌ Error checking card.")

# ---------------- OTHER HANDLERS ----------------
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

# ================= FILE CHECKER LOGIC =================
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
    print("🤖 Credit Card Checker is running...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)