import requests
import telebot, time
from telebot import types
from telebot.types import LabeledPrice
from gatet import Tele 
import os
import json
from flask import Flask
from threading import Thread
import datetime

# ==========================================
# 1. إعدادات السيرفر
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "<b>Bot is Running... 🚀</b>"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. إعدادات البوت
# ==========================================

TOKEN = '8305232757:AAF-rxugmGHIbpIqiGlWFO27jZGY9Uh4CtA' 
ADMIN_ID = 7170023644 
REQUIRED_CHANNEL = "@dailydroppp" 
WELCOME_IMAGE_PATH = "welcome.jpg" 

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

USERS_FILE = "users_data.json"
LANG_FILE = "users_lang.json"

# ================= TEXTS / النصوص =================
TEXTS = {
    "ar": {
        "welcome": """
✨ <b>أهلاً بك {name} {vip_badge} 👋</b>

🤖 <b>بوت فحص البطاقات (VIP)</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
💎 <b>النقاط:</b> <code>{points}</code>
⏳ <b>الحالة:</b> {vip_status}

👇 <b>اختر من القائمة:</b>
""",
        # تصميم البطاقة البنكية للبروفايل
        "profile_card": """
<b>👤 ملفك الشخصي (VIP Card):</b>
<code>
╭───────────────────────╮
│  💳  MEMBER CARD      │
│                       │
│  👤 {name}
│  🆔 {id}
│  💎 Pts: {points}
│  ⏳ Exp: {vip_date}
╰───────────────────────╯
</code>
""",
        "btn_dev": "المطور 👨‍💻",
        "btn_buy": "شراء (نقاط/VIP) 💎",
        "btn_check": "رصيدي 💳",
        "btn_lang": "Language 🌐",
        "btn_cmds": "الأوامر 📜",
        "btn_back": "رجوع 🔙",
        "wait": "<b>جاري تحليل الملف... 📂</b>",
        "no_points": "⛔ <b>عذراً، رصيدك نفذ!</b>\nاشترِ نقاطاً أو اشترك في VIP.",
        "stop": "إيقاف الفحص 🛑",
        "choose_lang": "<b>Please choose language:</b>",
        "must_join_msg": f"⛔ <b>تنبيه</b>\nيجب الاشتراك في القناة أولاً: {REQUIRED_CHANNEL}",
        "btn_join_channel": "اشتراك 📢",
        "btn_verify_sub": "تحقق ✅",
        "sub_not_found": "❌ لم تشترك بعد!",
        "sub_confirmed": "✅ تم التحقق!",
        "cmds_msg": "📜 <b>الأوامر:</b> /chk, /points, /start",
        "chk_usage": "⚠️ <b>خطأ!</b> استخدم:\n<code>/chk CC|MM|YY|CVV</code>",
        "processing_one": "⚡ <b>جاري المعالجة...</b>",
        "buy_menu_title": "💎 <b>المتجر</b>",
        "btn_buy_points": "شراء نقاط 🔢",
        "btn_buy_vip": "اشتراك VIP ⏳",
        "vip_title": "👑 <b>باقات VIP</b>",
        "points_title": "🔢 <b>باقات النقاط</b>",
        "buy_success_pts": "✅ <b>تم الشراء!</b> أضيفت {amount} نقطة.",
        "buy_success_vip": "✅ <b>مبروك VIP! 👑</b>\nالمدة: {hours} ساعة.",
        "btn_contact": "الدعم الفني 👨‍💻",
        "vip_1h": "1 ساعة (100 ⭐️)",
        "vip_1d": "1 يوم (500 ⭐️) 🔥",
        "vip_1w": "1 أسبوع (2000 ⭐️)",
        "pts_100": "100 نقطة (50 ⭐️)",
        "pts_200": "200 نقطة (75 ⭐️)",
        "pts_500": "500 نقطة (150 ⭐️)"
    },
    "en": {
        "welcome": """
✨ <b>Welcome {name} {vip_badge} 👋</b>

🤖 <b>CC Checker Bot (VIP)</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
💎 <b>Points:</b> <code>{points}</code>
⏳ <b>Status:</b> {vip_status}

👇 <b>Select Option:</b>
""",
        "profile_card": """
<b>👤 Your Profile (VIP Card):</b>
<code>
╭───────────────────────╮
│  💳  MEMBER CARD      │
│                       │
│  👤 {name}
│  🆔 {id}
│  💎 Pts: {points}
│  ⏳ Exp: {vip_date}
╰───────────────────────╯
</code>
""",
        "btn_dev": "Developer 👨‍💻",
        "btn_buy": "Buy (Pts/VIP) 💎",
        "btn_check": "Balance 💳",
        "btn_lang": "اللغة 🌐",
        "btn_cmds": "Commands 📜",
        "btn_back": "Back 🔙",
        "wait": "<b>Analyzing File... 📂</b>",
        "no_points": "⛔ <b>No Balance!</b>\nBuy points or VIP.",
        "stop": "STOP 🛑",
        "choose_lang": "<b>Please choose language:</b>",
        "must_join_msg": f"⛔ <b>Alert</b>\nJoin channel first: {REQUIRED_CHANNEL}",
        "btn_join_channel": "Join 📢",
        "btn_verify_sub": "Verify ✅",
        "sub_not_found": "❌ Not subscribed!",
        "sub_confirmed": "✅ Verified!",
        "cmds_msg": "📜 <b>Cmds:</b> /chk, /points, /start",
        "chk_usage": "⚠️ <b>Error!</b> Use:\n<code>/chk CC|MM|YY|CVV</code>",
        "processing_one": "⚡ <b>Processing...</b>",
        "buy_menu_title": "💎 <b>Store</b>",
        "btn_buy_points": "Buy Points 🔢",
        "btn_buy_vip": "Buy VIP ⏳",
        "vip_title": "👑 <b>VIP Packs</b>",
        "points_title": "🔢 <b>Points Packs</b>",
        "buy_success_pts": "✅ <b>Purchased!</b> Added {amount} pts.",
        "buy_success_vip": "✅ <b>VIP Activated! 👑</b>\nTime: {hours} hours.",
        "btn_contact": "Support 👨‍💻",
        "vip_1h": "1 Hour (100 ⭐️)",
        "vip_1d": "1 Day (500 ⭐️) 🔥",
        "vip_1w": "1 Week (2000 ⭐️)",
        "pts_100": "100 Pts (50 ⭐️)",
        "pts_200": "200 Pts (75 ⭐️)",
        "pts_500": "500 Pts (150 ⭐️)"
    }
}

# ================= DATA & HELPER FUNCTIONS =================
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def get_user_data(user_id):
    data = load_json(USERS_FILE)
    uid = str(user_id)
    if uid not in data: return {"points": 0, "vip_expire": 0}
    if isinstance(data[uid], int): # Fix old data
        new_data = {"points": data[uid], "vip_expire": 0}
        data[uid] = new_data
        save_json(USERS_FILE, data)
        return new_data
    return data.get(uid, {"points": 0, "vip_expire": 0})

def update_user_data(user_id, points=0, vip_hours=0):
    data = load_json(USERS_FILE)
    uid = str(user_id)
    if uid not in data or isinstance(data[uid], int):
        current_pts = data.get(uid, 0) if isinstance(data.get(uid), int) else 0
        current_vip = 0
    else:
        current_pts = data[uid].get("points", 0)
        current_vip = data[uid].get("vip_expire", 0)
    
    new_points = current_pts + points
    if new_points < 0: new_points = 0
    
    new_vip = current_vip
    if vip_hours > 0:
        now = time.time()
        if current_vip > now: new_vip = current_vip + (vip_hours * 3600)
        else: new_vip = now + (vip_hours * 3600)
            
    data[uid] = {"points": new_points, "vip_expire": new_vip}
    save_json(USERS_FILE, data)
    return data[uid]

def is_vip(user_id):
    data = get_user_data(user_id)
    return data["vip_expire"] > time.time()

def get_lang(user_id):
    return load_json(LANG_FILE).get(str(user_id), "en") 

def set_lang(user_id, lang_code):
    data = load_json(LANG_FILE)
    data[str(user_id)] = lang_code
    save_json(LANG_FILE, data)

def check_subscription(user_id):
    try:
        return bot.get_chat_member(REQUIRED_CHANNEL, user_id).status in ['creator', 'administrator', 'member']
    except: return False

def get_progress_bar(current, total, length=10):
    percent = (current / total) 
    filled_length = int(length * percent)
    bar = '█' * filled_length + '░' * (length - filled_length)
    return f"[{bar}] {int(percent * 100)}%"

# ================= MENU HANDLERS =================
def show_main_menu(chat_id, user_id, message_id=None):
    lang = get_lang(user_id)
    t = TEXTS[lang]
    user_data = get_user_data(user_id)
    points = user_data["points"]
    is_vip_bool = is_vip(user_id)
    
    vip_badge = "👑" if is_vip_bool else ""
    vip_status = "ACTIVE ✅" if is_vip_bool else "FREE ❌"

    try:
        user = bot.get_chat_member(chat_id, user_id).user
        first_name = user.first_name
        username_raw = user.username
    except: first_name = "User"; username_raw = ""
    user_tag = f"(@{username_raw})" if username_raw else ""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t["btn_dev"], url="https://t.me/aymen_1144"),
        types.InlineKeyboardButton(t["btn_buy"], callback_data="buy_main_menu"),
        types.InlineKeyboardButton(t["btn_check"], callback_data="check_profile"),
        types.InlineKeyboardButton(t["btn_lang"], callback_data="change_lang"),
        types.InlineKeyboardButton(t["btn_cmds"], callback_data="show_cmds")
    )
    
    caption = t["welcome"].format(name=first_name, username=user_tag, points=points, vip_badge=vip_badge, vip_status=vip_status)
    
    if message_id:
        try: bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption, reply_markup=markup)
        except: pass
    else:
        try:
            with open(WELCOME_IMAGE_PATH, 'rb') as photo_file:
                 bot.send_photo(chat_id, photo_file, caption=caption, reply_markup=markup)
        except: bot.send_message(chat_id, caption, reply_markup=markup)

def show_force_sub_message(chat_id, user_id):
    lang = get_lang(user_id)
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(t["btn_join_channel"], url=f"https://t.me/{REQUIRED_CHANNEL.replace('@','')}"),
        types.InlineKeyboardButton(t["btn_verify_sub"], callback_data="verify_sub")
    )
    bot.send_message(chat_id, t["must_join_msg"], reply_markup=markup)

# ================= CORE HANDLERS =================
@bot.message_handler(commands=["start"])
def start(message):
    if not check_subscription(message.from_user.id):
        show_force_sub_message(message.chat.id, message.from_user.id)
        return
    get_user_data(message.from_user.id) # Init data
    show_main_menu(message.chat.id, message.from_user.id)

@bot.callback_query_handler(func=lambda call: call.data == 'verify_sub')
def verify_sub_callback(call):
    lang = get_lang(call.from_user.id)
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, TEXTS[lang]["sub_confirmed"], show_alert=False)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id, call.from_user.id)
    else:
        bot.answer_callback_query(call.id, TEXTS[lang]["sub_not_found"], show_alert=True)

# --- 1. PROFILE CARD (Credit Card Style) ---
@bot.callback_query_handler(func=lambda call: call.data == 'check_profile')
def check_profile_btn(call):
    user_id = call.from_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    user_data = get_user_data(user_id)
    
    # Format Expiry Date
    if user_data["vip_expire"] > time.time():
        vip_date = datetime.datetime.fromtimestamp(user_data["vip_expire"]).strftime('%d/%m/%y')
    else:
        vip_date = "N/A"
    
    # Clean Name for Card
    name = call.from_user.first_name[:15] # Limit name length for card
    
    msg = t["profile_card"].format(name=name, id=user_id, points=user_data["points"], vip_date=vip_date)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main"))
    
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=msg, reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == 'change_lang')
def change_lang_btn(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("العربية 🇩🇿", callback_data="set_lang_ar"),
        types.InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en"),
        types.InlineKeyboardButton(TEXTS[get_lang(call.from_user.id)]["btn_back"], callback_data="back_to_main")
    )
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=TEXTS["en"]["choose_lang"], reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def language_selection(call):
    set_lang(call.from_user.id, call.data.split("_")[2])
    show_main_menu(call.message.chat.id, call.from_user.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'show_cmds')
def show_cmds_callback(call):
    user_id = call.from_user.id; lang = get_lang(user_id); t = TEXTS[lang]
    msg = t["cmds_msg"]
    if user_id == ADMIN_ID: msg += "\n\n👮‍♂️ <b>Dev:</b>\n⚡ /give ID PTS\n⚡ /vip ID HOURS"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main"))
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=msg, reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def back_to_main_callback(call):
    show_main_menu(call.message.chat.id, call.from_user.id, message_id=call.message.message_id)

# ================= PURCHASE SYSTEM =================
@bot.callback_query_handler(func=lambda call: call.data == 'buy_main_menu')
def buy_main(call):
    lang = get_lang(call.from_user.id); t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(t["btn_buy_vip"], callback_data="buy_vip_list"),
        types.InlineKeyboardButton(t["btn_buy_points"], callback_data="buy_points_list"),
        types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main")
    )
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["buy_menu_title"], reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == 'buy_vip_list')
def buy_vip(call):
    lang = get_lang(call.from_user.id); t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(t["vip_1h"], callback_data="pay_vip_100_1"),
        types.InlineKeyboardButton(t["vip_1d"], callback_data="pay_vip_500_24"),
        types.InlineKeyboardButton(t["vip_1w"], callback_data="pay_vip_2000_168"),
        types.InlineKeyboardButton(t["btn_back"], callback_data="buy_main_menu")
    )
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["vip_title"], reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == 'buy_points_list')
def buy_pts(call):
    lang = get_lang(call.from_user.id); t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(t["pts_100"], callback_data="pay_pts_50_100"),
        types.InlineKeyboardButton(t["pts_200"], callback_data="pay_pts_75_200"),
        types.InlineKeyboardButton(t["pts_500"], callback_data="pay_pts_150_500"),
        types.InlineKeyboardButton(t["btn_back"], callback_data="buy_main_menu")
    )
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["points_title"], reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def invoice(call):
    parts = call.data.split('_'); type_ = parts[1]; stars = int(parts[2]); val = int(parts[3])
    lang = get_lang(call.from_user.id); t = TEXTS[lang]
    
    if type_ == 'pts':
        title = f"{val} Points"; desc = f"Add {val} points"; payload = f"pts_{val}_{call.from_user.id}"
    else:
        title = f"VIP {val}h"; desc = f"VIP for {val} hours"; payload = f"vip_{val}_{call.from_user.id}"
        
    bot.send_invoice(call.message.chat.id, title=title, description=desc, invoice_payload=payload,
                     provider_token="", currency="XTR", prices=[LabeledPrice(label=title, amount=stars)],
                     start_parameter="buy")

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(q): bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_pay(message):
    lang = get_lang(message.from_user.id); t = TEXTS[lang]
    parts = message.successful_payment.invoice_payload.split('_')
    
    if parts[0] == 'pts':
        update_user_data(message.from_user.id, points=int(parts[1]))
        bot.reply_to(message, t["buy_success_pts"].format(amount=parts[1]))
    else:
        update_user_data(message.from_user.id, vip_hours=int(parts[1]))
        bot.reply_to(message, t["buy_success_vip"].format(hours=parts[1]))
        
    try: bot.send_message(ADMIN_ID, f"💰 <b>Paid:</b> {message.from_user.first_name} | {parts[1]} {parts[0]}")
    except: pass

# ================= ADMIN & CHECKING =================
@bot.message_handler(commands=["give", "vip"])
def admin_cmds(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        cmd, uid, val = message.text.split()
        if cmd == "/give":
            update_user_data(int(uid), points=int(val))
            bot.reply_to(message, f"✅ Given {val} pts to {uid}")
        elif cmd == "/vip":
            update_user_data(int(uid), vip_hours=int(val))
            bot.reply_to(message, f"✅ Given {val}h VIP to {uid}")
    except: bot.reply_to(message, "Error. Usage: /give ID PTS or /vip ID HOURS")

# --- 2. RECEIPT STYLE (Single Check) ---
@bot.message_handler(commands=["chk"])
def chk_single(message):
    uid = message.from_user.id
    if not check_subscription(uid):
        show_force_sub_message(message.chat.id, uid)
        return
    
    lang = get_lang(uid); t = TEXTS[lang]
    user_data = get_user_data(uid)
    is_vip_bool = user_data["vip_expire"] > time.time()
    
    if not is_vip_bool and user_data["points"] < 1:
        bot.reply_to(message, t["no_points"])
        return

    try: cc = message.text.split(" ", 1)[1]
    except: 
        bot.reply_to(message, t["chk_usage"])
        return
        
    ko = bot.reply_to(message, t["processing_one"]).message_id
    if not is_vip_bool: update_user_data(uid, points=-1)
    
    try:
        try: req = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
        except: req = {}
        bank = req.get('bank', 'N/A')
        
        # Tele check
        res = str(Tele(cc))
        
        status = "DECLINED ❌"
        if 'Approved' in res or 'Succeeded' in res: status = "APPROVED ✅"
        elif 'Insufficient' in res: status = "LOW FUNDS ⚠️"
        
        vip_tag = "👑 VIP" if is_vip_bool else "Free"

        # Receipt Template
        msg = f"""
<b>🧾 TRANSACTION RECEIPT</b>
<code>
───────────────
💳 Card: {cc}
🏦 Bank: {bank}
💰 Amt:  $1.00
✅ Sts:  {status}
───────────────
</code>
<b>👑 Member: {vip_tag}</b>
<b>🤖 Dev: @aymen_1144</b>
"""
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="❌ Error")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_call(call):
    with open("stop.stop", "w") as f: pass

# --- 3. PROGRESS BAR (File Check) ---
@bot.message_handler(content_types=["document"])
def chk_file(message):
    uid = message.from_user.id
    if not check_subscription(uid): return
    
    lang = get_lang(uid); t = TEXTS[lang]
    user_data = get_user_data(uid)
    is_vip_bool = user_data["vip_expire"] > time.time()
    
    ko = bot.reply_to(message, t["wait"]).message_id
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open("combo.txt", "wb") as f: f.write(downloaded)
    except: return

    with open("combo.txt", "r") as f: lines = f.readlines()
    total = len(lines)
    
    if not is_vip_bool and user_data["points"] < total:
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=t["no_points"])
        return
        
    if not is_vip_bool: update_user_data(uid, points=-total)
    
    # Init Stats
    live = 0; die = 0; checked = 0
    stop_markup = types.InlineKeyboardMarkup()
    stop_markup.add(types.InlineKeyboardButton(t["stop"], callback_data="stop"))
    
    for i, cc in enumerate(lines):
        if os.path.exists("stop.stop"):
            os.remove("stop.stop")
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="🛑 STOPPED")
            return
            
        cc = cc.strip()
        if not cc: continue
        
        # Check Card logic here (Simplified for loop)
        try: res = str(Tele(cc))
        except: res = "Error"
        
        if 'Approved' in res: live += 1
        else: die += 1
        checked += 1
        
        # --- UPDATE PROGRESS BAR (Every 5 cards) ---
        if i % 5 == 0 or i == total - 1:
            bar = get_progress_bar(checked, total)
            msg = f"""
<b>📂 FILE CHECKING...</b>
{bar}
━━━━━━━━━━━━━━
<b>✅ Live:</b> {live}
<b>❌ Die:</b>  {die}
<b>📉 Total:</b> {total}
━━━━━━━━━━━━━━
<b>🚀 Processing:</b> <code>{cc[:10]}...</code>
"""
            try: bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg, reply_markup=stop_markup)
            except: pass

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"✅ <b>DONE!</b>\nLive: {live} | Die: {die}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
