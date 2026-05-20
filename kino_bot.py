"""
🎬 Telegram Kino Bot
===================
O'rnatish:
  pip install pyTelegramBotAPI

Ishga tushirish:
  python kino_bot.py

Kerakli narsa:
  - @BotFather dan BOT_TOKEN oling
  - BOT_TOKEN ni pastdagi joyga kiriting
"""

import telebot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# ==========================================
# ⚙️ SOZLAMALAR - shu yerni to'ldiring
# ==========================================
BOT_TOKEN = "8153612756:AAEI8icbNrk_iwsIYoMxQL38ULyBiTDSNn4"
ADMIN_ID   = 6529179160                # Sizning Telegram ID
# ==========================================

bot = telebot.TeleBot(BOT_TOKEN)

# ==========================================
# 🎬 KINOLAR BAZASI
# Yangi kino qo'shish uchun shu ro'yxatga
# qo'shib boring. format:
# {
#   "id": "unikal_id",
#   "nomi": "Kino nomi",
#   "yil": 2023,
#   "janr": ["Janr1", "Janr2"],
#   "til": "O'zbek / Rus / ...",
#   "reyting": 8.5,
#   "tavsif": "Kino haqida qisqacha",
#   "link": "https://t.me/... yoki https://...",
#   "rasm": "https://... (ixtiyoriy)"
# }
# ==========================================

KINOLAR = [
    {
        "id": "avatar2",
        "nomi": "Avatar: Suvning Yo'li",
        "yil": 2022,
        "janr": ["Fantastika", "Sarguzasht"],
        "til": "O'zbek tilida",
        "reyting": 7.8,
        "tavsif": "Selly va Neytiri oilasi yangi qabila bilan yashash uchun Pandoraning okeanlariga ko'chib o'tadi.",
        "link": "https://t.me/example/1",
    },
    {
        "id": "topgun",
        "nomi": "Top Gun: Maverick",
        "yil": 2022,
        "janr": ["Боевик", "Drama"],
        "til": "O'zbek tilida",
        "reyting": 8.3,
        "tavsif": "Maverick eski do'stining o'g'lini o'z qo'li ostida o'qitishga majbur bo'ladi.",
        "link": "https://t.me/example/2",
    },
    {
        "id": "oppenheimer",
        "nomi": "Oppenheimer",
        "yil": 2023,
        "janr": ["Tarix", "Drama"],
        "til": "Rus tilida",
        "reyting": 8.5,
        "tavsif": "Atom bombasini yaratgan olim J. Robert Oppengeymerning hayoti.",
        "link": "https://t.me/example/3",
    },
    {
        "id": "barbie",
        "nomi": "Barbie",
        "yil": 2023,
        "janr": ["Komediya", "Fantaziya"],
        "til": "O'zbek tilida",
        "reyting": 7.0,
        "tavsif": "Barbie haqiqiy dunyoga tushib qoladi va o'zini qidira boshlaydi.",
        "link": "https://t.me/example/4",
    },
    {
        "id": "mission8",
        "nomi": "Mission: Impossible 8",
        "yil": 2024,
        "janr": ["Боевик", "Triller"],
        "til": "O'zbek tilida",
        "reyting": 8.1,
        "tavsif": "Ethan Hunt yangi xavfli missiyani bajaradi.",
        "link": "https://t.me/example/5",
    },
    {
        "id": "intouchables",
        "nomi": "1+1 (Intouchables)",
        "yil": 2011,
        "janr": ["Drama", "Komediya"],
        "til": "O'zbek tilida",
        "reyting": 8.5,
        "tavsif": "Boy nogironning kambag'al do'sti bilan do'stligi haqida.",
        "link": "https://t.me/example/6",
    },
    {
        "id": "inception",
        "nomi": "Inception",
        "yil": 2010,
        "janr": ["Fantastika", "Triller"],
        "til": "Rus tilida",
        "reyting": 8.8,
        "tavsif": "Dom Cobb odamlarning tushiga kirib sirlarni o'g'irlaydi.",
        "link": "https://t.me/example/7",
    },
    {
        "id": "shawshank",
        "nomi": "The Shawshank Redemption",
        "yil": 1994,
        "janr": ["Drama"],
        "til": "Rus tilida",
        "reyting": 9.3,
        "tavsif": "Nohaq qamalgan Andy Dufresne qamoqxonada umid va iroda bilan yashaydi.",
        "link": "https://t.me/example/8",
    },
]

# Barcha janrlar ro'yxati (avtomatik)
def barcha_janrlar():
    janrlar = set()
    for k in KINOLAR:
        for j in k["janr"]:
            janrlar.add(j)
    return sorted(janrlar)

# Kino qidirish (nomi bo'yicha)
def kino_qidir(so_rov):
    so_rov = so_rov.lower().strip()
    natija = []
    for k in KINOLAR:
        if so_rov in k["nomi"].lower():
            natija.append(k)
    return natija

# Janr bo'yicha filter
def janr_filter(janr):
    return [k for k in KINOLAR if janr in k["janr"]]

# Kino ma'lumotini chiroyli format qilish
def kino_xabar(k):
    yulduzlar = "⭐" * round(k["reyting"] / 2)
    janrlar = " · ".join(k["janr"])
    return (
        f"🎬 *{k['nomi']}* ({k['yil']})\n"
        f"🎭 Janr: {janrlar}\n"
        f"🌐 Til: {k['til']}\n"
        f"⭐ Reyting: {k['reyting']}/10 {yulduzlar}\n\n"
        f"📝 {k['tavsif']}"
    )

# Asosiy menyu klaviaturasi
def asosiy_menyu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton("🔍 Kino qidirish"),
        KeyboardButton("🎭 Janrlar bo'yicha"),
        KeyboardButton("🔥 Mashhur kinolar"),
        KeyboardButton("🆕 Yangi kinolar"),
        KeyboardButton("ℹ️ Yordam"),
    )
    return kb

# Janrlar klaviaturasi
def janrlar_klaviatura():
    kb = InlineKeyboardMarkup(row_width=2)
    tugmalar = [
        InlineKeyboardButton(j, callback_data=f"janr_{j}")
        for j in barcha_janrlar()
    ]
    kb.add(*tugmalar)
    kb.add(InlineKeyboardButton("🔙 Orqaga", callback_data="orqaga"))
    return kb

# Kino ko'rish tugmasi
def kino_tugmasi(kino_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("▶️ Kinoni ko'rish", url=KINOLAR_ID[kino_id]["link"]))
    return kb

# ID bo'yicha tez qidirish uchun dict
KINOLAR_ID = {k["id"]: k for k in KINOLAR}

# ==========================================
# 📨 HANDLER lar
# ==========================================

@bot.message_handler(commands=["start"])
def start(msg):
    ism = msg.from_user.first_name or "Do'stim"
    bot.send_message(
        msg.chat.id,
        f"👋 Salom, *{ism}*!\n\n"
        f"🎬 *Kino Bot*ga xush kelibsiz!\n\n"
        f"Bu botda:\n"
        f"• 🔍 Kino nomi bo'yicha qidirish\n"
        f"• 🎭 Janr bo'yicha tanlash\n"
        f"• ▶️ To'g'ridan-to'g'ri tomosha qilish\n\n"
        f"Pastdagi tugmalardan foydalaning 👇",
        parse_mode="Markdown",
        reply_markup=asosiy_menyu()
    )

@bot.message_handler(commands=["help"])
def help_cmd(msg):
    bot.send_message(
        msg.chat.id,
        "ℹ️ *Yordam*\n\n"
        "🔍 *Qidirish* — kino nomini yozing\n"
        "🎭 *Janrlar* — kategoriya bo'yicha tanlang\n"
        "🔥 *Mashhur* — top reytingli kinolar\n"
        "🆕 *Yangi* — oxirgi qo'shilgan kinolar\n\n"
        "Savol bo'lsa: @admin",
        parse_mode="Markdown",
        reply_markup=asosiy_menyu()
    )

# Asosiy menyu tugmalari
@bot.message_handler(func=lambda m: m.text in [
    "🔍 Kino qidirish", "🎭 Janrlar bo'yicha",
    "🔥 Mashhur kinolar", "🆕 Yangi kinolar", "ℹ️ Yordam"
])
def menyu_handler(msg):
    t = msg.text

    if t == "🔍 Kino qidirish":
        bot.send_message(
            msg.chat.id,
            "🔍 Qidirmoqchi bo'lgan kino nomini yozing:\n\n"
            "_(masalan: Avatar, Inception, 1+1)_",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler(msg, qidirish_natija)

    elif t == "🎭 Janrlar bo'yicha":
        bot.send_message(
            msg.chat.id,
            "🎭 Janrni tanlang:",
            reply_markup=janrlar_klaviatura()
        )

    elif t == "🔥 Mashhur kinolar":
        mashhurlar = sorted(KINOLAR, key=lambda x: x["reyting"], reverse=True)[:5]
        xabar = "🔥 *Top 5 mashhur kinolar:*\n\n"
        for i, k in enumerate(mashhurlar, 1):
            xabar += f"{i}. 🎬 *{k['nomi']}* — ⭐{k['reyting']}\n"
        
        kb = InlineKeyboardMarkup(row_width=1)
        for k in mashhurlar:
            kb.add(InlineKeyboardButton(
                f"🎬 {k['nomi']} ({k['yil']})",
                callback_data=f"kino_{k['id']}"
            ))
        
        bot.send_message(msg.chat.id, xabar, parse_mode="Markdown", reply_markup=kb)

    elif t == "🆕 Yangi kinolar":
        yangilar = sorted(KINOLAR, key=lambda x: x["yil"], reverse=True)[:5]
        
        kb = InlineKeyboardMarkup(row_width=1)
        for k in yangilar:
            kb.add(InlineKeyboardButton(
                f"🎬 {k['nomi']} ({k['yil']})",
                callback_data=f"kino_{k['id']}"
            ))
        
        bot.send_message(
            msg.chat.id,
            "🆕 *Eng yangi kinolar:*",
            parse_mode="Markdown",
            reply_markup=kb
        )

    elif t == "ℹ️ Yordam":
        help_cmd(msg)

# Qidiruv natijasi
def qidirish_natija(msg):
    so_rov = msg.text.strip()
    natijalar = kino_qidir(so_rov)

    if not natijalar:
        bot.send_message(
            msg.chat.id,
            f"😔 *'{so_rov}'* bo'yicha hech narsa topilmadi.\n\n"
            f"Boshqa nom bilan urinib ko'ring.",
            parse_mode="Markdown",
            reply_markup=asosiy_menyu()
        )
        return

    if len(natijalar) == 1:
        k = natijalar[0]
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("▶️ Kinoni ko'rish", url=k["link"]))
        bot.send_message(
            msg.chat.id,
            kino_xabar(k),
            parse_mode="Markdown",
            reply_markup=kb
        )
    else:
        kb = InlineKeyboardMarkup(row_width=1)
        for k in natijalar:
            kb.add(InlineKeyboardButton(
                f"🎬 {k['nomi']} ({k['yil']})",
                callback_data=f"kino_{k['id']}"
            ))
        bot.send_message(
            msg.chat.id,
            f"🔍 *'{so_rov}'* bo'yicha {len(natijalar)} ta natija:",
            parse_mode="Markdown",
            reply_markup=kb
        )

# Inline tugmalar
@bot.callback_query_handler(func=lambda c: True)
def callback_handler(call):
    data = call.data

    if data.startswith("kino_"):
        kino_id = data[5:]
        k = KINOLAR_ID.get(kino_id)
        if k:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("▶️ Kinoni ko'rish", url=k["link"]))
            kb.add(InlineKeyboardButton("🔙 Orqaga", callback_data="orqaga"))
            bot.edit_message_text(
                kino_xabar(k),
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=kb
            )

    elif data.startswith("janr_"):
        janr = data[5:]
        kinolar = janr_filter(janr)
        if kinolar:
            kb = InlineKeyboardMarkup(row_width=1)
            for k in kinolar:
                kb.add(InlineKeyboardButton(
                    f"🎬 {k['nomi']} ({k['yil']}) ⭐{k['reyting']}",
                    callback_data=f"kino_{k['id']}"
                ))
            kb.add(InlineKeyboardButton("🔙 Janrlarga", callback_data="janrlar"))
            bot.edit_message_text(
                f"🎭 *{janr}* janridagi kinolar ({len(kinolar)} ta):",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown",
                reply_markup=kb
            )

    elif data == "janrlar":
        bot.edit_message_text(
            "🎭 Janrni tanlang:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=janrlar_klaviatura()
        )

    elif data == "orqaga":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    bot.answer_callback_query(call.id)

# Matn bo'yicha avtomatik qidirish
@bot.message_handler(func=lambda m: True)
def avtomatik_qidirish(msg):
    if len(msg.text) < 2:
        return
    natijalar = kino_qidir(msg.text)
    if natijalar:
        kb = InlineKeyboardMarkup(row_width=1)
        for k in natijalar[:5]:
            kb.add(InlineKeyboardButton(
                f"🎬 {k['nomi']} ({k['yil']})",
                callback_data=f"kino_{k['id']}"
            ))
        bot.send_message(
            msg.chat.id,
            f"🔍 Topildi:",
            reply_markup=kb
        )

# ==========================================
# 🚀 BOTNI ISHGA TUSHIRISH
# ==========================================
if __name__ == "__main__":
    print("🎬 Kino bot ishga tushdi...")
    print(f"📽️ Bazada {len(KINOLAR)} ta kino bor")
    bot.infinity_polling()
