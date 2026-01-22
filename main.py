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
✨ <b>أهلاً بك عزيزي {name} {username} {vip_badge} 👋</b>

🤖 <b>Credit Card Checker</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
✅ <b>البوت الأفضل لفحص الكومبو واستخراج البطاقات الصالحة.</b>

💎 <b>رصيدك:</b> <code>{points}</code> نقطة
⏳ <b>حالة الاشتراك:</b> {vip_status}

👇 <b>اختر من القائمة الرئيسية:</b>
""",
        "profile_msg": """
👤 <b>ملفك الشخصي:</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
🆔 <b>الآيدي:</b> <code>{id}</code>
👤 <b>الاسم:</b> {name} {vip_badge}
💎 <b>النقاط:</b> <code>{points}</code>

🌟 <b>حالة الـ VIP:</b>
{vip_status_full}
""",
        "btn_dev": "المطور 👨‍💻",
        "btn_buy": "شراء (نقاط/VIP) 💎",
        "btn_check": "رصيدي 💰",
        "btn_lang": "Language 🌐",
        "btn_cmds": "الأوامر 📜",
        "btn_back": "رجوع 🔙",
        "wait": "<b>جاري البدء... يرجى الانتظار ⌛</b>",
        "no_points": "⛔ <b>عذراً، رصيدك غير كافٍ وليس لديك اشتراك VIP!</b>\nاشترِ نقاطاً أو اشترك في VIP.",
        "stop": "إيقاف الفحص 🛑",
        "choose_lang": "<b>Please choose your language:\nالرجاء اختيار لغتك لبدء الاستخدام:</b>",
        "must_join_msg": f"⛔ <b>عذراً عزيزي</b>\n\nيجب عليك الاشتراك في قناة المطور أولاً لاستخدام البوت.\n\nاشترك ثم اضغط على زر <b>'تحقق من الاشتراك'</b>.",
        "btn_join_channel": "اشتراك في القناة 📢",
        "btn_verify_sub": "✅ تحقق من الاشتراك",
        "sub_not_found": "❌ لم تقم بالاشتراك في القناة بعد. حاول مجدداً.",
        "sub_confirmed": "✅ تم التحقق من اشتراكك. أهلاً بك!",
        "cmds_msg": "📜 <b>الأوامر المتاحة:</b>\n/start, /points, /chk ...",
        "chk_usage": "⚠️ <b>طريقة الاستخدام خطأ!</b>\nأرسل الأمر مع البطاقة هكذا:\n<code>/chk XXXXXXXXXXXXXXXX|MM|YY|CVV</code>",
        "processing_one": "⚡ <b>جاري فحص البطاقة...</b>\n<code>{cc}</code>",
        "buy_menu_title": "💎 <b>قائمة الشراء</b>\nاختر نوع الشراء المناسب لك:",
        "btn_buy_points": "شراء نقاط (بالعدد) 🔢",
        "btn_buy_vip": "اشتراك VIP (بالوقت) ⏳",
        "vip_title": "👑 <b>اشتراكات VIP</b>\nافحص بدون خصم نقاط طوال مدة الاشتراك!",
        "points_title": "🔢 <b>باقات النقاط</b>\nتدفع مرة واحدة وتبقى النقاط معك للأبد.",
        "buy_success_pts": "✅ <b>تم الدفع بنجاح!</b>\nتمت إضافة <code>{amount}</code> نقطة.",
        "buy_success_vip": "✅ <b>تم تفعيل VIP بنجاح! 👑</b>\nمدتة: {hours} ساعة.\nينتهي في: {date}",
        "btn_contact": "تواصل مع المطور 👨‍💻",
        # VIP Packages
        "vip_1h": "1 ساعة (100 ⭐️)",
        "vip_1d": "1 يوم (500 ⭐️) 🔥",
        "vip_1w": "1 أسبوع (2000 ⭐️) 🏷",
        # Points Packages
        "pts_100": "100 نقطة (50 ⭐️)",
        "pts_200": "200 نقطة (75 ⭐️)",
        "pts_500": "500 نقطة (150 ⭐️)"
    },
    "en": {
        "welcome": """
✨ <b>Welcome Dear {name} {username} {vip_badge} 👋</b>

🤖 <b>Credit Card Checker</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
✅ <b>Best bot for checking combos.</b>

💎 <b>Balance:</b> <code>{points}</code> Points
⏳ <b>Status:</b> {vip_status}

👇 <b>Select from menu:</b>
""",
        "profile_msg": """
👤 <b>Your Profile:</b>
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
🆔 <b>ID:</b> <code>{id}</code>
👤 <b>Name:</b> {name} {vip_badge}
💎 <b>Points:</b> <code>{points}</code>

🌟 <b>VIP Status:</b>
{vip_status_full}
""",
        "btn_dev": "Developer 👨‍💻",
        "btn_buy": "Buy (Points/VIP) 💎",
        "btn_check": "Profile 💰",
        "btn_lang": "اللغة 🌐",
        "btn_cmds": "Commands 📜",
        "btn_back": "Back 🔙",
        "wait": "<b>Starting... Please wait ⌛</b>",
        "no_points": "⛔ <b>Insufficient points & No VIP!</b>\nBuy points or subscribe to VIP.",
        "stop": "STOP CHECK 🛑",
        "choose_lang": "<b>Please choose your language:\nالرجاء اختيار لغتك لبدء الاستخدام:</b>",
        "must_join_msg": f"⛔ <b>Sorry Dear</b>\n\nYou must subscribe to the developer's channel first to use the bot.\n\nSubscribe and then press <b>'Verify Subscription'</b>.",
        "btn_join_channel": "Join Channel 📢",
        "btn_verify_sub": "✅ Verify Subscription",
        "sub_not_found": "❌ You haven't subscribed yet. Please try again.",
        "sub_confirmed": "✅ Subscription verified. Welcome!",
        "cmds_msg": "📜 <b>Commands:</b>\n/start, /points, /chk ...",
        "chk_usage": "⚠️ <b>Wrong Usage!</b>\nUse command like this:\n<code>/chk XXXXXXXXXXXXXXXX|MM|YY|CVV</code>",
        "processing_one": "⚡ <b>Checking card...</b>\n<code>{cc}</code>",
        "buy_menu_title": "💎 <b>Purchase Menu</b>\nChoose check type:",
        "btn_buy_points": "Buy Points (Count) 🔢",
        "btn_buy_vip": "Subscribe VIP (Time) ⏳",
        "vip_title": "👑 <b>VIP Subscriptions</b>\nCheck unlimited without points!",
        "points_title": "🔢 <b>Points Packages</b>\nPay once, keep points forever.",
        "buy_success_pts": "✅ <b>Payment Successful!</b>\nAdded <code>{amount}</code> points.",
        "buy_success_vip": "✅ <b>VIP Activated! 👑</b>\nDuration: {hours} Hours.\nExpires: {date}",
        "btn_contact": "Contact Developer 👨‍💻",
        "vip_1h": "1 Hour (100 ⭐️)",
        "vip_1d": "1 Day (500 ⭐️) 🔥",
        "vip_1w": "1 Week (2000 ⭐️) 🏷",
        "pts_100": "100 Points (50 ⭐️)",
        "pts_200": "200 Points (75 ⭐️)",
        "pts_500": "500 Points (150 ⭐️)"
    }
}

# ================= DATA FUNCTIONS (SMART) =================
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# دالة ذكية تجلب البيانات وتحول المستخدمين القدامى للنظام الجديد
def get_user_data(user_id):
    data = load_json(USERS_FILE)
    uid = str(user_id)
    if uid not in data:
        return {"points": 0, "vip_expire": 0}
    
    # تحويل البيانات القديمة (int) إلى النظام الجديد (dict)
    if isinstance(data[uid], int):
        new_data = {"points": data[uid], "vip_expire": 0}
        data[uid] = new_data
        save_json(USERS_FILE, data)
        return new_data
        
    return data.get(uid, {"points": 0, "vip_expire": 0})

def update_user_data(user_id, points=0, vip_hours=0):
    data = load_json(USERS_FILE)
    uid = str(user_id)
    
    # التأكد من التنسيق
    if uid not in data or isinstance(data[uid], int):
        current_pts = data.get(uid, 0) if isinstance(data.get(uid), int) else 0
        current_vip = 0
    else:
        current_pts = data[uid].get("points", 0)
        current_vip = data[uid].get("vip_expire", 0)
    
    # تحديث النقاط
    new_points = current_pts + points
    if new_points < 0: new_points = 0
    
    # تحديث الـ VIP
    new_vip = current_vip
    if vip_hours > 0:
        now = time.time()
        # إذا كان مشتركاً بالفعل، نضيف الوقت على وقته الحالي
        if current_vip > now:
            new_vip = current_vip + (vip_hours * 3600)
        else:
            new_vip = now + (vip_hours * 3600)
            
    data[uid] = {"points": new_points, "vip_expire": new_vip}
    save_json(USERS_FILE, data)
    return data[uid]

def is_vip(user_id):
    data = get_user_data(user_id)
    return data["vip_expire"] > time.time()

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

# ================= MENU FUNCTIONS =================
def show_main_menu(chat_id, user_id, message_id=None):
    lang = get_lang(user_id)
    t = TEXTS[lang]
    user_data = get_user_data(user_id)
    points = user_data["points"]
    is_vip_bool = is_vip(user_id)
    
    vip_badge = "👑 VIP" if is_vip_bool else ""
    vip_status = "Active ✅" if is_vip_bool else "Free ❌"
    if lang == "ar":
        vip_status = "نشط ✅" if is_vip_bool else "مجاني ❌"

    try:
        user = bot.get_chat_member(chat_id, user_id).user
        first_name = user.first_name
        username_raw = user.username
    except:
        first_name = "User"
        username_raw = ""
    user_tag = f"(@{username_raw})" if username_raw else ""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(t["btn_dev"], url="https://t.me/aymen_1144")
    btn2 = types.InlineKeyboardButton(t["btn_buy"], callback_data="buy_main_menu") 
    btn3 = types.InlineKeyboardButton(t["btn_check"], callback_data="check_profile") 
    btn4 = types.InlineKeyboardButton(t["btn_lang"], callback_data="change_lang") 
    btn5 = types.InlineKeyboardButton(t["btn_cmds"], callback_data="show_cmds") 
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    caption = t["welcome"].format(name=first_name, username=user_tag, points=points, vip_badge=vip_badge, vip_status=vip_status)
    
    if message_id:
        try: bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption, reply_markup=markup)
        except: pass # Ignore if same content
    else:
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

# ================= HANDLERS =================

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        show_force_sub_message(message.chat.id, user_id)
        return 
    # التأكد من وجود البيانات
    get_user_data(user_id)
    show_main_menu(message.chat.id, user_id)

@bot.callback_query_handler(func=lambda call: call.data == 'verify_sub')
def verify_sub_callback(call):
    user_id = call.from_user.id
    lang = get_lang(user_id)
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, TEXTS[lang]["sub_confirmed"], show_alert=False)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id, user_id)
    else:
        bot.answer_callback_query(call.id, TEXTS[lang]["sub_not_found"], show_alert=True)

# 1. البروفايل (Profile)
@bot.callback_query_handler(func=lambda call: call.data == 'check_profile')
def check_profile_btn(call):
    user_id = call.from_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    
    user_data = get_user_data(user_id)
    points = user_data["points"]
    vip_expire = user_data["vip_expire"]
    
    is_vip_bool = vip_expire > time.time()
    vip_badge = "👑 VIP" if is_vip_bool else ""
    
    if is_vip_bool:
        exp_date = datetime.datetime.fromtimestamp(vip_expire).strftime('%Y-%m-%d %H:%M')
        vip_status_full = f"✅ Active until: {exp_date}"
        if lang == "ar": vip_status_full = f"✅ نشط حتى: {exp_date}"
    else:
        vip_status_full = "❌ Not Active (Free)"
        if lang == "ar": vip_status_full = "❌ غير نشط (مجاني)"

    try:
        user = bot.get_chat_member(call.message.chat.id, user_id).user
        first_name = user.first_name
        username = f"@{user.username}" if user.username else "None"
    except:
        first_name = "User"; username = "None"
    
    msg = t["profile_msg"].format(name=first_name, username=username, id=user_id, points=points, vip_badge=vip_badge, vip_status_full=vip_status_full)
    
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main")
    markup.add(btn_back)

    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=msg, reply_markup=markup)
    except: pass

# 2. تغيير اللغة
@bot.callback_query_handler(func=lambda call: call.data == 'change_lang')
def change_lang_btn(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_ar = types.InlineKeyboardButton("العربية 🇩🇿", callback_data="set_lang_ar")
    btn_en = types.InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en")
    btn_back = types.InlineKeyboardButton(TEXTS[get_lang(call.from_user.id)]["btn_back"], callback_data="back_to_main")
    markup.add(btn_ar, btn_en)
    markup.add(btn_back)
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=TEXTS["en"]["choose_lang"], reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('set_lang_'))
def language_selection(call):
    lang_code = call.data.split("_")[2]
    set_lang(call.from_user.id, lang_code)
    show_main_menu(call.message.chat.id, call.from_user.id, message_id=call.message.message_id)

# 3. الأوامر
@bot.callback_query_handler(func=lambda call: call.data == 'show_cmds')
def show_cmds_callback(call):
    user_id = call.from_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    msg_text = t["cmds_msg"]
    if user_id == ADMIN_ID:
        admin_txt = "\n\n👮‍♂️ <b>Dev:</b>\n⚡ <b>/give ID PTS</b>\n⚡ <b>/vip ID HOURS</b>"
        msg_text += admin_txt
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main")
    markup.add(btn_back)
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=msg_text, reply_markup=markup)
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def back_to_main_callback(call):
    show_main_menu(call.message.chat.id, call.from_user.id, message_id=call.message.message_id)

# ================= PURCHASE SYSTEM (POINTS + VIP) =================

# القائمة الرئيسية للشراء (اختيار بين نقاط او VIP)
@bot.callback_query_handler(func=lambda call: call.data == 'buy_main_menu')
def buy_main_menu_func(call):
    lang = get_lang(call.from_user.id)
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_vip = types.InlineKeyboardButton(t["btn_buy_vip"], callback_data="buy_vip_list")
    btn_pts = types.InlineKeyboardButton(t["btn_buy_points"], callback_data="buy_points_list")
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="back_to_main")
    markup.add(btn_vip, btn_pts, btn_back)
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["buy_menu_title"], reply_markup=markup)
    except: pass

# قائمة اشتراكات VIP
@bot.callback_query_handler(func=lambda call: call.data == 'buy_vip_list')
def buy_vip_list_func(call):
    lang = get_lang(call.from_user.id)
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    # الاسعار: 1 ساعة=100، 1 يوم=500، 1 اسبوع=2000
    btn_1h = types.InlineKeyboardButton(t["vip_1h"], callback_data="pay_vip_100_1") # 100 stars, 1 hour
    btn_1d = types.InlineKeyboardButton(t["vip_1d"], callback_data="pay_vip_500_24") # 500 stars, 24 hours
    btn_1w = types.InlineKeyboardButton(t["vip_1w"], callback_data="pay_vip_2000_168") # 2000 stars, 168 hours
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="buy_main_menu")
    markup.add(btn_1h, btn_1d, btn_1w, btn_back)
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["vip_title"], reply_markup=markup)
    except: pass

# قائمة شراء النقاط
@bot.callback_query_handler(func=lambda call: call.data == 'buy_points_list')
def buy_points_list_func(call):
    lang = get_lang(call.from_user.id)
    t = TEXTS[lang]
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_100 = types.InlineKeyboardButton(t["pts_100"], callback_data="pay_pts_50_100")
    btn_200 = types.InlineKeyboardButton(t["pts_200"], callback_data="pay_pts_75_200")
    btn_500 = types.InlineKeyboardButton(t["pts_500"], callback_data="pay_pts_150_500")
    btn_back = types.InlineKeyboardButton(t["btn_back"], callback_data="buy_main_menu")
    markup.add(btn_100, btn_200, btn_500, btn_back)
    try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=t["points_title"], reply_markup=markup)
    except: pass

# معالج إرسال الفاتورة (للاثنين)
@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def send_invoice_handler(call):
    # Data formats: 
    # pay_pts_STARS_POINTS (e.g., pay_pts_50_100)
    # pay_vip_STARS_HOURS  (e.g., pay_vip_100_1)
    
    data_parts = call.data.split('_')
    buy_type = data_parts[1] # 'pts' or 'vip'
    stars_amount = int(data_parts[2])
    value_amount = int(data_parts[3]) # Points amount OR Hours count
    
    lang = get_lang(call.from_user.id)
    t = TEXTS[lang]
    
    if buy_type == 'pts':
        title = f"{value_amount} Points"
        description = f"Buy {value_amount} Check Points"
        payload = f"pts_{value_amount}_{call.from_user.id}"
    else:
        title = f"VIP {value_amount} Hours"
        description = f"VIP Subscription for {value_amount} Hours"
        payload = f"vip_{value_amount}_{call.from_user.id}"

    bot.send_invoice(
        chat_id=call.message.chat.id,
        title=title,
        description=description,
        invoice_payload=payload,
        provider_token="", currency="XTR",
        prices=[LabeledPrice(label=title, amount=stars_amount)],
        start_parameter="buy"
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
    
    parts = payload.split('_')
    p_type = parts[0]
    p_amount = int(parts[1])
    
    if p_type == 'pts':
        # إضافة نقاط
        update_user_data(message.from_user.id, points=p_amount)
        bot.reply_to(message, t["buy_success_pts"].format(amount=p_amount))
        admin_note = f"💎 {p_amount} Pts"
    else:
        # تفعيل VIP
        update_user_data(message.from_user.id, vip_hours=p_amount)
        # حساب تاريخ الانتهاء للعرض
        user_data = get_user_data(message.from_user.id)
        exp_date = datetime.datetime.fromtimestamp(user_data["vip_expire"]).strftime('%Y-%m-%d %H:%M')
        bot.reply_to(message, t["buy_success_vip"].format(hours=p_amount, date=exp_date))
        admin_note = f"👑 VIP {p_amount} Hours"

    try:
        user_tag = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        bot.send_message(ADMIN_ID, f"💰 <b>شراء جديد!</b>\n👤 {user_tag}\n⭐️ {amount_paid} Stars\n📦 {admin_note}")
    except: pass

# 5. أوامر المطور (نقاط + VIP)
@bot.message_handler(commands=["give"])
def give_pts_cmd(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        # /give ID POINTS
        parts = message.text.split()
        uid = int(parts[1]); pts = int(parts[2])
        update_user_data(uid, points=pts)
        bot.reply_to(message, f"✅ Done. Added {pts} points to {uid}")
    except: bot.reply_to(message, "Usage: /give ID POINTS")

@bot.message_handler(commands=["vip"])
def give_vip_cmd(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        # /vip ID HOURS
        parts = message.text.split()
        uid = int(parts[1]); hours = int(parts[2])
        update_user_data(uid, vip_hours=hours)
        bot.reply_to(message, f"✅ Done. Added {hours} VIP hours to {uid}")
    except: bot.reply_to(message, "Usage: /vip ID HOURS")

# 6. الفحص (Check Logic Updated)
@bot.message_handler(commands=["chk"])
def single_check_handler(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        show_force_sub_message(message.chat.id, user_id)
        return
    
    lang = get_lang(user_id)
    t = TEXTS[lang]
    
    # التحقق من الرصيد والاشتراك
    user_data = get_user_data(user_id)
    is_vip_bool = user_data["vip_expire"] > time.time()
    points = user_data["points"]
    
    # الشرط: يجب أن يكون VIP أو لديه نقاط > 0
    if not is_vip_bool and points < 1:
        bot.reply_to(message, t["no_points"])
        return

    try: cc_data = message.text.split(" ", 1)[1]
    except IndexError:
        bot.reply_to(message, t["chk_usage"])
        return

    ko = bot.reply_to(message, t["processing_one"].format(cc=cc_data)).message_id
    
    # خصم نقطة فقط إذا لم يكن VIP
    if not is_vip_bool:
        update_user_data(user_id, points=-1)
        
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
        
        # Badge in result
        user_tag = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        vip_tag = "👑" if is_vip_bool else ""
        
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
👤 <b>By:</b> {user_tag} {vip_tag}
🤖 <b>Bot By:</b> @aymen_1144
"""
        if 'Donation Successful!' in last or 'Approved' in last:
            res_msg = msg_template.format(cc=cc_data, response="✅ Charged $1 🔥", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag, vip_tag=vip_tag)
            bot.reply_to(message, res_msg)
        elif 'insufficient funds' in last:
            res_msg = msg_template.format(cc=cc_data, response="📉 Low Funds", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag, vip_tag=vip_tag)
            bot.reply_to(message, res_msg)
        elif 'security code is incorrect' in last:
            res_msg = msg_template.format(cc=cc_data, response="⚠️ CCN Match", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag, vip_tag=vip_tag)
            bot.reply_to(message, res_msg)
        else:
            res_msg = msg_template.format(cc=cc_data, response="❌ Declined", card_type=card_type, brand=brand, bank=bank, country=country, country_flag=country_flag, time=execution_time, user_tag=user_tag, vip_tag=vip_tag)
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=res_msg)
    except Exception as e:
        print(f"Error in single check: {e}")
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="❌ Error checking card.")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    with open("stop.stop", "w") as file: pass

@bot.message_handler(commands=["points"])
def points_cmd(message):
    show_main_menu(message.chat.id, message.from_user.id) # Just show menu

@bot.message_handler(commands=["cmds", "help"])
def commands_handler(message):
    user_id = message.from_user.id
    lang = get_lang(user_id)
    t = TEXTS[lang]
    msg_text = t["cmds_msg"]
    if user_id == ADMIN_ID:
        admin_txt = "\n\n👮‍♂️ <b>Dev:</b>\n⚡ <b>/give ID PTS</b>\n⚡ <b>/vip ID HOURS</b>"
        msg_text += admin_txt
    bot.reply_to(message, msg_text)

if __name__ == "__main__":
    print("🤖 Bot started...")
    keep_alive() 
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
