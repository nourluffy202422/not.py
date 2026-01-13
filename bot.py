import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot.apihelper
import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

ADMIN_ID = 8062504379
BOT_TOKEN = "8490801013:AAGshZn_N0ZY1K-Ocd7CIgza2alUeYBUxd4"
bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = "data-users.json"
CHANNELS_FILE = "channels.json"

user_states = {}
broadcast_message = {}

SURAS = {
    "1. الفاتحة": "https://t.me/quran_chunnle/5",
    "2. البقرة": "https://t.me/quran_chunnle/7",
    "3. آل عمران": "https://t.me/quran_chunnle/38",
    "4. النساء": "https://t.me/quran_chunnle/39",
    "5. المائدة": "https://t.me/quran_chunnle/40",
    "6. الأنعام": "https://t.me/quran_chunnle/41",
    "7. الأعراف": "https://t.me/quran_chunnle/42",
    "8. الأنفال": "https://t.me/quran_chunnle/43",
    "9. التوبة": "https://t.me/quran_chunnle/44",
    "10. يونس": "https://t.me/quran_chunnle/45",
    "11. هود": "https://t.me/quran_chunnle/46",
    "12. يوسف": "https://t.me/quran_chunnle/47",
    "13. الرعد": "https://t.me/quran_chunnle/48",
    "14. إبراهيم": "https://t.me/quran_chunnle/49",
    "15. الحجر": "https://t.me/quran_chunnle/50",
    "16. النحل": "https://t.me/quran_chunnle/51",
    "17. الإسراء": "https://t.me/quran_chunnle/52",
    "18. الكهف": "https://t.me/quran_chunnle/53",
    "19. مريم": "https://t.me/quran_chunnle/54",
    "20. طه": "https://t.me/quran_chunnle/55",
    "21. الأنبياء": "https://t.me/quran_chunnle/56",
    "22. الحج": "https://t.me/quran_chunnle/57",
    "23. المؤمنون": "https://t.me/quran_chunnle/58",
    "24. النور": "https://t.me/quran_chunnle/59",
    "25. الفرقان": "https://t.me/quran_chunnle/60",
    "26. الشعراء": "https://t.me/quran_chunnle/61",
    "27. النمل": "https://t.me/quran_chunnle/62",
    "28. القصص": "https://t.me/quran_chunnle/63",
    "29. العنكبوت": "https://t.me/quran_chunnle/64",
    "30. الروم": "https://t.me/quran_chunnle/65",
    "31. لقمان": "https://t.me/quran_chunnle/66",
    "32. السجدة": "https://t.me/quran_chunnle/67",
    "33. الأحزاب": "https://t.me/quran_chunnle/68",
    "34. سبأ": "https://t.me/quran_chunnle/69",
    "35. فاطر": "https://t.me/quran_chunnle/70",
    "36. يس": "https://t.me/quran_chunnle/71",
    "37. الصافات": "https://t.me/quran_chunnle/72",
    "38. ص": "https://t.me/quran_chunnle/73",
    "39. الزمر": "https://t.me/quran_chunnle/74",
    "40. غافر": "https://t.me/quran_chunnle/75",
    "41. فصلت": "https://t.me/quran_chunnle/76",
    "42. الشورى": "https://t.me/quran_chunnle/77",
    "43. الزخرف": "https://t.me/quran_chunnle/78",
    "44. الدخان": "https://t.me/quran_chunnle/79",
    "45. الجاثية": "https://t.me/quran_chunnle/80",
    "46. الأحقاف": "https://t.me/quran_chunnle/81",
    "47. محمد": "https://t.me/quran_chunnle/82",
    "48. الفتح": "https://t.me/quran_chunnle/83",
    "49. الحجرات": "https://t.me/quran_chunnle/84",
    "50. ق": "https://t.me/quran_chunnle/85",
    "51. الذاريات": "https://t.me/quran_chunnle/86",
    "52. الطور": "https://t.me/quran_chunnle/87",
    "53. النجم": "https://t.me/quran_chunnle/88",
    "54. القمر": "https://t.me/quran_chunnle/89",
    "55. الرحمن": "https://t.me/quran_chunnle/90",
    "56. الواقعة": "https://t.me/quran_chunnle/91",
    "57. الحديد": "https://t.me/quran_chunnle/92",
    "58. المجادلة": "https://t.me/quran_chunnle/93",
    "59. الحشر": "https://t.me/quran_chunnle/94",
    "60. الممتحنة": "https://t.me/quran_chunnle/95",
    "61. الصف": "https://t.me/quran_chunnle/96",
    "62. الجمعة": "https://t.me/quran_chunnle/97",
    "63. المنافقون": "https://t.me/quran_chunnle/98",
    "64. التغابن": "https://t.me/quran_chunnle/99",
    "65. الطلاق": "https://t.me/quran_chunnle/100",
    "66. التحريم": "https://t.me/quran_chunnle/101",
    "67. الملك": "https://t.me/quran_chunnle/102",
    "68. القلم": "https://t.me/quran_chunnle/103",
    "69. الحاقة": "https://t.me/quran_chunnle/104",
    "70. المعارج": "https://t.me/quran_chunnle/105",
    "71. نوح": "https://t.me/quran_chunnle/106",
    "72. الجن": "https://t.me/quran_chunnle/107",
    "73. المزمل": "https://t.me/quran_chunnle/108",
    "74. المدثر": "https://t.me/quran_chunnle/109",
    "75. القيامة": "https://t.me/quran_chunnle/110",
    "76. الإنسان": "https://t.me/quran_chunnle/111",
    "77. المرسلات": "https://t.me/quran_chunnle/112",
    "78. النبأ": "https://t.me/quran_chunnle/113",
    "79. النازعات": "https://t.me/quran_chunnle/114",
    "80. عبس": "https://t.me/quran_chunnle/115",
    "81. التكوير": "https://t.me/quran_chunnle/116",
    "82. الإنفطار": "https://t.me/quran_chunnle/117",
    "83. المطففين": "https://t.me/quran_chunnle/118",
    "84. الإنشقاق": "https://t.me/quran_chunnle/119",
    "85. البروج": "https://t.me/quran_chunnle/120",
    "86. الطارق": "https://t.me/quran_chunnle/121",
    "87. الأعلى": "https://t.me/quran_chunnle/122",
    "88. الغاشية": "https://t.me/quran_chunnle/123",
    "89. الفجر": "https://t.me/quran_chunnle/124",
    "90. البلد": "https://t.me/quran_chunnle/125",
    "91. الشمس": "https://t.me/quran_chunnle/126",
    "92. الليل": "https://t.me/quran_chunnle/127",
    "93. الضحى": "https://t.me/quran_chunnle/128",
    "94. الشرح": "https://t.me/quran_chunnle/129",
    "95. التين": "https://t.me/quran_chunnle/130",
    "96. العلق": "https://t.me/quran_chunnle/131",
    "97. القدر": "https://t.me/quran_chunnle/132",
    "98. البينة": "https://t.me/quran_chunnle/133",
    "99. الزلزلة": "https://t.me/quran_chunnle/134",
    "100. العاديات": "https://t.me/quran_chunnle/135",
    "101. القارعة": "https://t.me/quran_chunnle/136",
    "102. التكاثر": "https://t.me/quran_chunnle/137",
    "103. العصر": "https://t.me/quran_chunnle/138",
    "104. الهمزة": "https://t.me/quran_chunnle/139",
    "105. الفيل": "https://t.me/quran_chunnle/140",
    "106. قريش": "https://t.me/quran_chunnle/141",
    "107. الماعون": "https://t.me/quran_chunnle/142",
    "108. الكوثر": "https://t.me/quran_chunnle/143",
    "109. الكافرون": "https://t.me/quran_chunnle/144",
    "110. النصر": "https://t.me/quran_chunnle/145",
    "111. المسد": "https://t.me/quran_chunnle/146",
    "112. الإخلاص": "https://t.me/quran_chunnle/147",
    "113. الفلق": "https://t.me/quran_chunnle/148",
    "114. الناس": "https://t.me/quran_chunnle/149"
}
user_page = {}
tasbih_count = {}

def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
                logger.info(f"تم تحميل {len(users)} مستخدم من الملف")
                return users
        else:
            logger.info("ملف المستخدمين غير موجود، سيتم إنشاؤه")
            return []
    except Exception as e:
        logger.error(f"خطأ في تحميل ملف المستخدمين: {e}")
        return []

def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        logger.info(f"تم حفظ {len(users)} مستخدم في الملف")
    except Exception as e:
        logger.error(f"خطأ في حفظ ملف المستخدمين: {e}")

def add_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)
        logger.info(f"تم إضافة مستخدم جديد: {user_id}")
    return users

def load_channels():
    try:
        if os.path.exists(CHANNELS_FILE):
            with open(CHANNELS_FILE, 'r', encoding='utf-8') as f:
                channels = json.load(f)
                logger.info(f"تم تحميل {len(channels)} قناة من الملف")
                return channels
        else:
            logger.info("ملف القنوات غير موجود، سيتم إنشاؤه")
            return []
    except Exception as e:
        logger.error(f"خطأ في تحميل ملف القنوات: {e}")
        return []

def save_channels(channels):
    try:
        with open(CHANNELS_FILE, 'w', encoding='utf-8') as f:
            json.dump(channels, f, ensure_ascii=False, indent=2)
        logger.info(f"تم حفظ {len(channels)} قناة في الملف")
    except Exception as e:
        logger.error(f"خطأ في حفظ ملف القنوات: {e}")

def check_user_subscription(user_id):
    channels = load_channels()
    if not channels:
        return True, []

    unsubscribed_channels = []
    for channel in channels:
        try:
            member = bot.get_chat_member(channel['id'], user_id)
            if member.status in ['left', 'kicked']:
                unsubscribed_channels.append(channel)
        except Exception as e:
            logger.error(f"خطأ في فحص الاشتراك في القناة {channel['id']}: {e}")
            unsubscribed_channels.append(channel)

    return len(unsubscribed_channels) == 0, unsubscribed_channels

def main_menu(chat_id, msg_id=None):
    key = InlineKeyboardMarkup(row_width=2)
    key.add(InlineKeyboardButton("🕋 القرآن الكريم", callback_data="quran_menu"),
            InlineKeyboardButton("📿 تسبيح", callback_data="sbh"))
    key.add(InlineKeyboardButton("©️ حقوق البوت", callback_data="bot_rights"))


    if chat_id == ADMIN_ID:
        key.add(InlineKeyboardButton("⚙️ لوحة الأدمن", callback_data="admin_panel"))

    text = "اهلا بك في افضل بوت قرءان كريم ممكن ان تراه نتمني لك تجربة سعيده ..♥"
    if msg_id:
        try:
            bot.edit_message_text("اهلا بك في افضل بوت قرءان كريم ممكن ان تراه نتمني لك تجربة سعيده..♥", chat_id, msg_id, reply_markup=key)
        except telebot.apihelper.ApiTelegramException:
            bot.delete_message(chat_id, msg_id)
            bot.send_message(chat_id, text, reply_markup=key)
    else:
        bot.send_message(chat_id, text, reply_markup=key)

def quran_menu(chat_id, msg_id):
    key = InlineKeyboardMarkup(row_width=2)
    key.add(InlineKeyboardButton("📖 قراءة (صور)", callback_data="read_quran"),
            InlineKeyboardButton("🎧 استماع (صوت)", callback_data="listen_quran_0"))
    key.add(InlineKeyboardButton("🔍 بحث عن صفحة (صورة)", callback_data="search_page"))
    key.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_main"))
    text = "اختر ما تريد من القرآن الكريم:"
    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=key)
    except telebot.apihelper.ApiTelegramException as e:
        if 'message to edit not found' in e.description or "message can't be edited" in e.description:
            bot.delete_message(chat_id, msg_id)
            bot.send_message(chat_id, text, reply_markup=key)
        else:
            raise

def show_sura_list(chat_id, msg_id, page=0):
    suras_list = sorted(SURAS.keys(), key=lambda x: int(x.split('.')[0]))
    keyboard = InlineKeyboardMarkup(row_width=1)
    start_index = page * 10
    end_index = min(start_index + 10, len(suras_list))
    for i in range(start_index, end_index):
        sura_name = suras_list[i]
        keyboard.add(InlineKeyboardButton(sura_name, callback_data=f"sura_{sura_name}"))
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton("◀️ السابق", callback_data=f"listen_quran_{page-1}"))
    if end_index < len(suras_list):
        pagination_buttons.append(InlineKeyboardButton("التالي ▶️", callback_data=f"listen_quran_{page+1}"))
    if pagination_buttons:
        keyboard.row(*pagination_buttons)
    keyboard.add(InlineKeyboardButton("🔙 رجوع لقائمة القرآن", callback_data="quran_menu_delete"))
    bot.edit_message_text(
        text="اختر سورة للاستماع - تلاوة الشيخ محمد صديق المنشاوي:",
        chat_id=chat_id,
        message_id=msg_id,
        reply_markup=keyboard
    )

@bot.message_handler(commands=["start"])
def start(msg):
    user_id = msg.chat.id
    logger.info(f"مستخدم جديد بدأ البوت: {user_id}")


    add_user(user_id)


    is_subscribed, unsubscribed_channels = check_user_subscription(user_id)

    if not is_subscribed:
        show_subscription_required(user_id, unsubscribed_channels)
        return

    tasbih_count[user_id] = 0
    main_menu(user_id)

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    user_id = message.chat.id


    if user_id in user_states:
        state = user_states[user_id]

        if state == "waiting_broadcast_message" and user_id == ADMIN_ID:
            handle_broadcast_message(message)
        elif state == "waiting_channel_info" and user_id == ADMIN_ID:
            handle_add_channel(message)
        else:

            user_states.pop(user_id, None)


    is_subscribed, unsubscribed_channels = check_user_subscription(user_id)
    if not is_subscribed:
        show_subscription_required(user_id, unsubscribed_channels)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    cid = call.message.chat.id
    mid = call.message.message_id


    if cid != ADMIN_ID and call.data != "check_subscription":
        is_subscribed, unsubscribed_channels = check_user_subscription(cid)
        if not is_subscribed:
            bot.answer_callback_query(call.id, "❌ يجب الاشتراك في جميع القنوات أولاً!", show_alert=True)
            return

    if call.data == "back_main":
        main_menu(cid, mid)
        
    elif call.data == "bot_rights":
        show_bot_rights(cid, mid)
        
    elif call.data == "quran_menu":
        quran_menu(cid, mid)
    elif call.data == "quran_menu_delete":
        bot.delete_message(cid, mid)
        quran_menu(cid, None)
    elif call.data == "sbh":
        show_tasbih(call)
    elif call.data == "inc":
        tasbih_count[cid] = tasbih_count.get(cid, 0) + 1
        show_tasbih(call)
    elif call.data == "rst":
        tasbih_count[cid] = 0
        show_tasbih(call)
    elif call.data == "read_quran":
        user_page[cid] = 1
        show_quran_page(call, 1)
    elif call.data == "search_page":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, "أرسل رقم الصفحة التي تريد عرضها (من 1 إلى 604).")
        bot.register_next_step_handler_by_chat_id(cid, search_page_handler)
    elif call.data == "next_page":
        change_page(call, 1)
    elif call.data == "prev_page":
        change_page(call, -1)
    elif call.data.startswith("listen_quran_"):
        page = int(call.data.split("_")[2])
        show_sura_list(cid, mid, page)
    elif call.data.startswith("sura_"):
        sura_name = call.data.split("_", 1)[1]
        send_sura_audio(call, sura_name)


    elif call.data == "admin_panel" and cid == ADMIN_ID:
        show_admin_panel(cid, mid)
    elif call.data == "broadcast" and cid == ADMIN_ID:
        start_broadcast(cid, mid)
    elif call.data == "cancel_broadcast" and cid == ADMIN_ID:
        user_states.pop(cid, None)
        main_menu(cid, mid)
    elif call.data == "channels_management" and cid == ADMIN_ID:
        show_channels_management(cid, mid)
    elif call.data == "add_channel" and cid == ADMIN_ID:
        start_add_channel(cid, mid)
    elif call.data == "remove_channel" and cid == ADMIN_ID:
        show_channels_list_for_removal(cid, mid)
    elif call.data == "list_channels" and cid == ADMIN_ID:
        show_channels_list(cid, mid)
    elif call.data.startswith("remove_ch_") and cid == ADMIN_ID:
        channel_id = call.data.split("_", 2)[2]
        remove_channel(cid, mid, channel_id)
    elif call.data == "cancel_add_channel" and cid == ADMIN_ID:
        user_states.pop(cid, None)
        show_channels_management(cid, mid)
    elif call.data == "check_subscription":
        handle_check_subscription_callback(call)

def send_sura_audio(call, sura_name):
    audio_url = SURAS.get(sura_name)
    if audio_url:
        bot.answer_callback_query(call.id, f"جاري إرسال سورة {sura_name.split('.')[1].strip()}...")
        bot.send_chat_action(call.message.chat.id, 'upload_audio')
        bot.send_audio(
            chat_id=call.message.chat.id,
            audio=audio_url,
            title=sura_name,
            performer="محمد صديق المنشاوي",
            caption=f"سورة {sura_name} - تلاوة الشيخ محمد صديق المنشاوي"
        )
    else:
        bot.answer_callback_query(call.id, "عذراً، لم أجد رابط السورة.", show_alert=True)

def show_quran_page(call, page=1):
    uid = call.message.chat.id
    user_page[uid] = page
    img_url = f"https://quran.ksu.edu.sa/png_big/{page}.png"
    markup = InlineKeyboardMarkup(row_width=2)
    next_btn = InlineKeyboardButton("التالي ▶️", callback_data="next_page")
    prev_btn = InlineKeyboardButton("◀️ السابق", callback_data="prev_page")
    back_btn = InlineKeyboardButton("🔙 رجوع لقائمة القرآن", callback_data="quran_menu_delete")
    markup.add(prev_btn, next_btn)
    markup.add(back_btn)
    bot.delete_message(chat_id=uid, message_id=call.message.message_id)
    bot.send_photo(uid, img_url, caption=f"📖 رقم الصفحة: {page}", reply_markup=markup)

def search_page_handler(message):
    try:
        pagenum = int(message.text)
        if not 1 <= pagenum <= 604:
            bot.send_message(message.chat.id, "⚠️ رقم الصفحة غير صحيح! يجب أن يكون بين 1 و 604.")
            return
        img_url = f"https://quran.ksu.edu.sa/png_big/{pagenum}.png"
        key = InlineKeyboardMarkup()
        key.add(InlineKeyboardButton("🔙 رجوع لقائمة القرآن", callback_data="quran_menu"))
        bot.send_photo(message.chat.id, img_url, caption=f"📖 رقم الصفحة: {pagenum}", reply_markup=key)
    except (ValueError, TypeError):
        bot.send_message(message.chat.id, "⚠️ أدخل رقم صفحة صحيح!")

def change_page(call, direction):
    uid = call.message.chat.id
    pg_num = user_page.get(uid, 1) + direction
    if 1 <= pg_num <= 604:
        user_page[uid] = pg_num
        img_url = f"https://quran.ksu.edu.sa/png_big/{pg_num}.png"
        bot.edit_message_media(
            media=types.InputMediaPhoto(img_url, caption=f"📖 رقم الصفحة: {pg_num}"),
            chat_id=uid,
            message_id=call.message.message_id,
            reply_markup=call.message.reply_markup
        )
    else:
        bot.answer_callback_query(call.id, "📖 لا يوجد صفحات أخرى!")

def show_tasbih(call):
    cid = call.message.chat.id
    num = tasbih_count.get(cid, 0)
    key = InlineKeyboardMarkup(row_width=1)
    key.add(InlineKeyboardButton(f"📿 {num}", callback_data="inc"))
    key.add(InlineKeyboardButton("🔄 تصفير", callback_data="rst"),
            InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    try:
        bot.edit_message_text("اضغط على العداد للتسبيح:", cid, call.message.id, reply_markup=key)
    except telebot.apihelper.ApiTelegramException:
        bot.answer_callback_query(call.id)

def show_bot_rights(chat_id, msg_id):
    rights_text = """©️ حقوق البوت

جميع حقوق البوت محفوظة لدى:
👨‍💻 Saif Hassan

📞 للتواصل مع المطور: @S_S_F3
🛒 لتنصيب بوت قرآن كريم أو شراء الملف

شكراً لاستخدامك البوت! 🤍"""

    key = InlineKeyboardMarkup()
    key.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_main"))

    try:
        bot.edit_message_text(rights_text, chat_id, msg_id, reply_markup=key)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, rights_text, reply_markup=key)

def show_subscription_required(user_id, unsubscribed_channels):
    text = "🔒 يجب عليك الاشتراك في القنوات التالية لاستخدام البوت:\n\n"

    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in unsubscribed_channels:
        keyboard.add(InlineKeyboardButton(
            f"📢 {channel['name']}",
            url=f"https://t.me/{channel['username']}"
        ))

    keyboard.add(InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription"))

    bot.send_message(user_id, text, reply_markup=keyboard)

def show_admin_panel(chat_id, msg_id):
    users = load_users()
    channels = load_channels()

    text = f"""⚙️ لوحة الأدمن

📊 إحصائيات البوت:
👥 عدد المستخدمين: {len(users)}
📢 عدد القنوات: {len(channels)}

اختر العملية المطلوبة:"""

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("📢 إذاعة رسالة", callback_data="broadcast"))
    keyboard.add(InlineKeyboardButton("📺 قسم إدارة القنوات", callback_data="channels_management"))
    keyboard.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_main"))

    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def start_broadcast(chat_id, msg_id):
    user_states[chat_id] = "waiting_broadcast_message"

    text = """📢 إذاعة رسالة

أرسل الرسالة التي تريد إذاعتها لجميع المستخدمين:

ملاحظة: يمكنك إرسال نص، صورة، فيديو، أو أي نوع من الرسائل."""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("❌ إلغاء", callback_data="cancel_broadcast"))

    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def handle_broadcast_message(message):
    admin_id = message.chat.id
    user_states.pop(admin_id, None)

    users = load_users()
    if not users:
        bot.send_message(admin_id, "❌ لا يوجد مستخدمين لإرسال الرسالة إليهم!")
        return


    bot.send_message(admin_id, f"🔄 جاري إرسال الرسالة إلى {len(users)} مستخدم...")

    success_count = 0
    failed_count = 0

    for user_id in users:
        try:
            if message.content_type == 'text':
                bot.send_message(user_id, message.text)
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == 'video':
                bot.send_video(user_id, message.video.file_id, caption=message.caption)
            elif message.content_type == 'document':
                bot.send_document(user_id, message.document.file_id, caption=message.caption)
            elif message.content_type == 'audio':
                bot.send_audio(user_id, message.audio.file_id, caption=message.caption)
            elif message.content_type == 'voice':
                bot.send_voice(user_id, message.voice.file_id, caption=message.caption)
            elif message.content_type == 'sticker':
                bot.send_sticker(user_id, message.sticker.file_id)

            success_count += 1
            logger.info(f"تم إرسال الإذاعة للمستخدم: {user_id}")

        except Exception as e:
            failed_count += 1
            logger.error(f"فشل إرسال الإذاعة للمستخدم {user_id}: {e}")


    result_text = f"""✅ تم إنهاء الإذاعة

📊 النتائج:
✅ نجح الإرسال: {success_count}
❌ فشل الإرسال: {failed_count}
📊 المجموع: {len(users)}"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 العودة للوحة الأدمن", callback_data="admin_panel"))

    bot.send_message(admin_id, result_text, reply_markup=keyboard)

def show_channels_management(chat_id, msg_id):
    channels = load_channels()

    text = f"""📺 قسم إدارة القنوات

📊 عدد القنوات الحالية: {len(channels)}

اختر العملية المطلوبة:"""

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("➕ إضافة قناة اشتراك إجباري", callback_data="add_channel"))
    keyboard.add(InlineKeyboardButton("➖ إزالة قناة اشتراك إجباري", callback_data="remove_channel"))
    keyboard.add(InlineKeyboardButton("📋 قنوات الاشتراك الإجباري", callback_data="list_channels"))
    keyboard.add(InlineKeyboardButton("🔙 العودة للوحة الأدمن", callback_data="admin_panel"))

    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def start_add_channel(chat_id, msg_id):
    user_states[chat_id] = "waiting_channel_info"

    text = """➕ إضافة قناة اشتراك إجباري

أرسل معلومات القناة بالتنسيق التالي:
اسم القناة | @username | -100xxxxxxxxx

مثال:
قناة الأخبار | @news_channel | -1001234567890

ملاحظات مهمة:
• يجب أن يكون البوت أدمن في القناة
• ID القناة يبدأ بـ -100
• Username بدون علامة @"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("❌ إلغاء", callback_data="cancel_add_channel"))

    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def handle_add_channel(message):
    admin_id = message.chat.id
    user_states.pop(admin_id, None)

    try:
        parts = message.text.split(" | ")
        if len(parts) != 3:
            bot.send_message(admin_id, "❌ تنسيق خاطئ! استخدم: اسم القناة | @username | -100xxxxxxxxx")
            return

        channel_name = parts[0].strip()
        username = parts[1].strip().replace("@", "")
        channel_id = parts[2].strip()

        if not channel_id.startswith("-100"):
            bot.send_message(admin_id, "❌ ID القناة يجب أن يبدأ بـ -100")
            return

        try:
            channel_id = int(channel_id)
        except ValueError:
            bot.send_message(admin_id, "❌ ID القناة يجب أن يكون رقم صحيح")
            return

        try:
            bot_member = bot.get_chat_member(channel_id, bot.get_me().id)
            if bot_member.status not in ['administrator', 'creator']:
                bot.send_message(admin_id, "❌ البوت ليس أدمن في هذه القناة!")
                return
        except Exception as e:
            bot.send_message(admin_id, f"❌ خطأ في الوصول للقناة: {str(e)}")
            return

        channels = load_channels()

        for channel in channels:
            if channel['id'] == channel_id:
                bot.send_message(admin_id, "❌ هذه القناة موجودة مسبقاً!")
                return

        new_channel = {
            'name': channel_name,
            'username': username,
            'id': channel_id
        }

        channels.append(new_channel)
        save_channels(channels)

        success_text = f"""✅ تم إضافة القناة بنجاح!

📺 اسم القناة: {channel_name}
🔗 Username: @{username}
🆔 ID: {channel_id}"""

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🔙 العودة لإدارة القنوات", callback_data="channels_management"))

        bot.send_message(admin_id, success_text, reply_markup=keyboard)
        logger.info(f"تم إضافة قناة جديدة: {channel_name} ({channel_id})")

    except Exception as e:
        bot.send_message(admin_id, f"❌ حدث خطأ: {str(e)}")
        logger.error(f"خطأ في إضافة القناة: {e}")

def show_channels_list_for_removal(chat_id, msg_id):
    channels = load_channels()

    if not channels:
        text = "❌ لا توجد قنوات مضافة حالياً!"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🔙 العودة لإدارة القنوات", callback_data="channels_management"))
    else:
        text = "➖ اختر القناة التي تريد إزالتها:\n\n"
        keyboard = InlineKeyboardMarkup(row_width=1)

        for i, channel in enumerate(channels, 1):
            text += f"{i}. 📺 {channel['name']} (@{channel['username']})\n"
            keyboard.add(InlineKeyboardButton(
                f"🗑️ إزالة {channel['name']}",
                callback_data=f"remove_ch_{channel['id']}"
            ))

        keyboard.add(InlineKeyboardButton("🔙 العودة لإدارة القنوات", callback_data="channels_management"))

    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def remove_channel(chat_id, msg_id, channel_id):
    try:
        channel_id = int(channel_id)
        channels = load_channels()


        channel_found = None
        for i, channel in enumerate(channels):
            if channel['id'] == channel_id:
                channel_found = channels.pop(i)
                break

        if channel_found:
            save_channels(channels)
            text = f"""✅ تم حذف القناة بنجاح!

📺 القناة المحذوفة: {channel_found['name']}
🔗 Username: @{channel_found['username']}"""

            logger.info(f"تم حذف القناة: {channel_found['name']} ({channel_id})")
        else:
            text = "❌ لم يتم العثور على القناة!"

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🔙 العودة لإدارة القنوات", callback_data="channels_management"))

        try:
            bot.edit_message_text(text, chat_id, msg_id, reply_markup=keyboard)
        except telebot.apihelper.ApiTelegramException:
            bot.send_message(chat_id, text, reply_markup=keyboard)

    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ: {str(e)}")
        logger.error(f"خطأ في حذف القناة: {e}")

def show_channels_list(chat_id, msg_id):
    channels = load_channels()

    if not channels:
        text = "❌ لا توجد قنوات مضافة حالياً!"
    else:
        text = f"📋 قنوات الاشتراك الإجباري ({len(channels)}):\n\n"

        for i, channel in enumerate(channels, 1):
            text += f"{i}. 📺 **{channel['name']}**\n"
            text += f"   🔗 @{channel['username']}\n"
            text += f"   🆔 `{channel['id']}`\n\n"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔙 العودة لإدارة القنوات", callback_data="channels_management"))

    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=keyboard, parse_mode='Markdown')
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')

def handle_check_subscription_callback(call):
    user_id = call.message.chat.id

    is_subscribed, unsubscribed_channels = check_user_subscription(user_id)

    if is_subscribed:
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "✅ تم التحقق من اشتراكك بنجاح!")
        tasbih_count[user_id] = 0
        main_menu(user_id)
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات المطلوبة بعد!", show_alert=True)

def update_callback_handler():
    pass

print("🚀 البوت يعمل الآن...")
print(f"📊 تم تحميل {len(load_users())} مستخدم")
print(f"📺 تم تحميل {len(load_channels())} قناة")
logger.info("تم بدء تشغيل البوت بنجاح")

bot.polling(none_stop=True)
