
import telebot
import os
from dotenv import load_dotenv
from data_handlers import load_daily_data, save_daily_data, reset_daily_data
from counters import increment_counter, get_all_counts
from dashboard import get_daily_dua

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

AZKAR = [
    "سبحان الله",
    "الحمد لله",
    "لا إله إلا الله",
    "الله أكبر",
    "اللهم صل وسلم على سيدنا محمد",
    "تصدق بدعوة",
    "📊 العداد"
]

def get_azkar_keyboard():
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup()
    for i in range(0, len(AZKAR)-1, 2):
        row = [
            InlineKeyboardButton(text=AZKAR[i], callback_data=AZKAR[i]),
            InlineKeyboardButton(text=AZKAR[i+1], callback_data=AZKAR[i+1])
        ]
        keyboard.row(*row)
    keyboard.row(InlineKeyboardButton(text=AZKAR[-1], callback_data=AZKAR[-1]))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🌟 شارك في حملة الذكر الجماعي! كل ضغطة منك بتزيد الأجر لنا كلنا.

اختر ذكرًا بالضغط عليه 👇", reply_markup=get_azkar_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    if call.data == "📊 العداد":
        counts = get_all_counts()
        msg = "📈 إحصائيات اليوم:
"
        for key, val in counts.items():
            msg += f"- {key}: {val}
"
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "تصدق بدعوة":
        dua = get_daily_dua()
        increment_counter("تصدق بدعوة")
        bot.send_message(call.message.chat.id, f"🤲 {dua}")
    else:
        increment_counter(call.data)
        responses = {
            "سبحان الله": "🌸 سبحان الله - تملأ الميزان 🌸",
            "الحمد لله": "🌼 الحمد لله - تملأ ما بين السماء والأرض 🌼",
            "لا إله إلا الله": "🌟 لا إله إلا الله - أعظم كلمة 🌟",
            "الله أكبر": "🕊️ الله أكبر - الله أعظم من كل شيء 🕊️",
            "اللهم صل وسلم على سيدنا محمد": "❤️ أكثروا من الصلاة على النبي ﷺ ❤️"
        }
        response = responses.get(call.data, "ذكر طيب 🌿")
        bot.answer_callback_query(call.id, f"✅ تم تسجيل: {call.data}")
        bot.send_message(call.message.chat.id, response)

def run_bot():
    bot.polling(non_stop=True)
