"""
🎬 Telegram Kino Bot (Admin + User)
====================================
Admin: video yuboradi → bot saqlaydi
User: kino nomi yozadi → bot video yuboradi

O'rnatish:
  pip install pyTelegramBotAPI

Ishga tushirish:
  python kino_bot.py
"""

import telebot
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ==========================================
# ⚙️ SOZLAMALAR
# ==========================================
BOT_TOKEN = "8153612756:AAEI8icbNrk_iwsIYoMxQL38ULyBiTDSNn4"
ADMIN_ID  = 6529179160   # Faqat siz kino qo'sha olasiz
DB_FILE   = "kinolar.json"  # Kinolar shu faylda saqlanadi
# ==========================================

bot = telebot.TeleBot(BOT_TOKEN)

# ==========================================
# 💾 BAZA (JSON fayl)
# ==========================================
def db_load():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def db_save(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==========================================
# ADMIN holati (kino nomi kutilmoqda)
# ==========================================
admin_state = {}  # {admin_id: {"step": "wait_name", "file_id": "..."}}

# ==========================================
# KLAVIATURALAR
# ==========================================
def user_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🎬 Barcha kinolar"),
        KeyboardButton("ℹ️ Yordam")
    )
    return kb

def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("➕ Kino qo'shish"),
        KeyboardButton("🗑 Kino o'chirish"),
        KeyboardButton("📋 Kinolar ro'yxati"),
        KeyboardButton("🎬 Barcha kinolar"),
    )
    return kb

# ==========================================
# /start
# ==========================================
@bot.message_handler(commands=["start"])
def start(msg):
    ism = msg.from_user.first_name or "Do'stim"
    if msg.from_user.id == ADMIN_ID:
        bot.send_message(
            msg.chat.id,
            f"👋 Salom, Admin *{ism}*!\n\n"
            f"➕ *Kino qo'shish* — video yuborib kino qo'shing\n"
            f"🗑 *Kino o'chirish* — kino nomini o'chiring\n"
            f"📋 *Ro'yxat* — barcha kinolarni ko'ring\n\n"
            f"Foydalanuvchilar kino nomini yozib topadi! 🎬",
            parse_mode="Markdown",
            reply_markup=admin_menu()
        )
    else:
        bot.send_message(
            msg.chat.id,
            f"👋 Salom, *{ism}*!\n\n"
            f"🎬 Kino botga xush kelibsiz!\n\n"
            f"Kino nomini yozing — men topib beraman!\n"
            f"_(masalan: Avatar, Inception...)_",
            parse_mode="Markdown",
            reply_markup=user_menu()
        )

# ==========================================
# ADMIN: Kino qo'shish
# ==========================================
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text == "➕ Kino qo'shish")
def admin_add_start(msg):
    admin_state[ADMIN_ID] = {"step": "wait_video"}
    bot.send_message(
        msg.chat.id,
        "🎬 Kinoning video faylini yuboring:",
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )

# Admin video yubordi
@bot.message_handler(content_types=["video", "document"],
                     func=lambda m: m.from_user.id == ADMIN_ID and
                     admin_state.get(ADMIN_ID, {}).get("step") == "wait_video")
def admin_got_video(msg):
    if msg.video:
        file_id = msg.video.file_id
    else:
        file_id = msg.document.file_id

    admin_state[ADMIN_ID] = {"step": "wait_name", "file_id": file_id}
    bot.send_message(msg.chat.id, "✅ Video qabul qilindi!\n\n📝 Endi kino nomini yozing:\n_(masalan: Avatar 2022)_")

# Admin kino nomi yozdi
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and
                     admin_state.get(ADMIN_ID, {}).get("step") == "wait_name")
def admin_got_name(msg):
    nom = msg.text.strip()
    file_id = admin_state[ADMIN_ID]["file_id"]

    db = db_load()
    db[nom.lower()] = {
        "nom": nom,
        "file_id": file_id
    }
    db_save(db)

    admin_state.pop(ADMIN_ID, None)
    bot.send_message(
        msg.chat.id,
        f"✅ *{nom}* muvaffaqiyatli qo'shildi!\n\nFoydalanuvchilar endi bu kinoni topishi mumkin. 🎬",
        parse_mode="Markdown",
        reply_markup=admin_menu()
    )

# ==========================================
# ADMIN: Kino o'chirish
# ==========================================
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text == "🗑 Kino o'chirish")
def admin_delete_start(msg):
    db = db_load()
    if not db:
        bot.send_message(msg.chat.id, "❌ Hozircha kinolar yo'q.", reply_markup=admin_menu())
        return

    kb = InlineKeyboardMarkup(row_width=1)
    for key, val in db.items():
        kb.add(InlineKeyboardButton(f"🗑 {val['nom']}", callback_data=f"del_{key}"))

    bot.send_message(msg.chat.id, "Qaysi kinoni o'chirmoqchisiz?", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("del_") and c.from_user.id == ADMIN_ID)
def admin_delete_confirm(call):
    key = call.data[4:]
    db = db_load()
    if key in db:
        nom = db[key]["nom"]
        del db[key]
        db_save(db)
        bot.edit_message_text(f"✅ *{nom}* o'chirildi!", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

# ==========================================
# ADMIN: Ro'yxat
# ==========================================
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text == "📋 Kinolar ro'yxati")
def admin_list(msg):
    db = db_load()
    if not db:
        bot.send_message(msg.chat.id, "❌ Hozircha kinolar yo'q.", reply_markup=admin_menu())
        return

    xabar = f"📋 *Jami {len(db)} ta kino:*\n\n"
    for i, (key, val) in enumerate(db.items(), 1):
        xabar += f"{i}. 🎬 {val['nom']}\n"

    bot.send_message(msg.chat.id, xabar, parse_mode="Markdown", reply_markup=admin_menu())

# ==========================================
# USER + ADMIN: Barcha kinolar
# ==========================================
@bot.message_handler(func=lambda m: m.text == "🎬 Barcha kinolar")
def all_movies(msg):
    db = db_load()
    if not db:
        bot.send_message(msg.chat.id, "❌ Hozircha kinolar yo'q.")
        return

    kb = InlineKeyboardMarkup(row_width=1)
    for key, val in db.items():
        kb.add(InlineKeyboardButton(f"🎬 {val['nom']}", callback_data=f"watch_{key}"))

    bot.send_message(msg.chat.id, f"🎬 *{len(db)} ta kino mavjud:*", parse_mode="Markdown", reply_markup=kb)

# ==========================================
# USER: Kino nomi yozib qidirish
# ==========================================
@bot.message_handler(func=lambda m: m.text not in ["🎬 Barcha kinolar", "ℹ️ Yordam",
                                                     "➕ Kino qo'shish", "🗑 Kino o'chirish",
                                                     "📋 Kinolar ro'yxati"] and
                     not admin_state.get(m.from_user.id))
def search_movie(msg):
    so_rov = msg.text.strip().lower()
    db = db_load()

    # To'liq mos
    if so_rov in db:
        k = db[so_rov]
        bot.send_video(msg.chat.id, k["file_id"], caption=f"🎬 *{k['nom']}*", parse_mode="Markdown")
        return

    # Qisman mos
    natijalar = [(key, val) for key, val in db.items() if so_rov in key or so_rov in val["nom"].lower()]

    if not natijalar:
        bot.send_message(
            msg.chat.id,
            f"😔 *'{msg.text}'* topilmadi.\n\n"
            f"To'g'ri nom bilan yozing yoki 🎬 *Barcha kinolar* tugmasini bosing.",
            parse_mode="Markdown"
        )
        return

    if len(natijalar) == 1:
        key, val = natijalar[0]
        bot.send_video(msg.chat.id, val["file_id"], caption=f"🎬 *{val['nom']}*", parse_mode="Markdown")
    else:
        kb = InlineKeyboardMarkup(row_width=1)
        for key, val in natijalar[:8]:
            kb.add(InlineKeyboardButton(f"🎬 {val['nom']}", callback_data=f"watch_{key}"))
        bot.send_message(msg.chat.id, f"🔍 *{len(natijalar)} ta natija topildi:*", parse_mode="Markdown", reply_markup=kb)

# Inline tugma orqali kino yuborish
@bot.callback_query_handler(func=lambda c: c.data.startswith("watch_"))
def send_movie(call):
    key = call.data[6:]
    db = db_load()
    if key in db:
        val = db[key]
        bot.send_video(call.message.chat.id, val["file_id"], caption=f"🎬 *{val['nom']}*", parse_mode="Markdown")
    bot.answer_callback_query(call.id)

# ==========================================
# Yordam
# ==========================================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Yordam")
def help_msg(msg):
    bot.send_message(
        msg.chat.id,
        "ℹ️ *Yordam*\n\n"
        "🔍 Kino nomini yozing — bot topib yuboradi\n"
        "🎬 *Barcha kinolar* — ro'yxatdan tanlang\n\n"
        "Savol bo'lsa admin bilan bog'laning.",
        parse_mode="Markdown"
    )

# ==========================================
# 🚀 ISHGA TUSHIRISH
# ==========================================
if __name__ == "__main__":
    print("🎬 Kino bot ishga tushdi...")
    bot.infinity_polling()
