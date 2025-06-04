import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = '7744438470:AAEYORKBNhmVMyk4WTVjkpZ0R1EwGa_IBo8'
YANDEX_API_KEY = 'a54523ef-0fa8-4ed2-925a-eb0cf33bb0c1'

LATITUDE = 52.265
LONGITUDE = 104.261

CONDITION_TRANSLATION = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "drizzle": "морось",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "moderate-rain": "умеренный дождь",
    "heavy-rain": "сильный дождь",
    "continuous-heavy-rain": "длительный сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "thunderstorm-with-hail": "гроза с градом"
}

def keyboard_weather():
    buttons = [[KeyboardButton("/weather")]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def keyboard_spasibo():
    buttons = [[KeyboardButton("/spasibo")]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я - Владимир! Могу показать погоду в Иркутске. Нажми кнопку /weather или введи команду.",
        reply_markup=keyboard_weather()
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={LATITUDE}&lon={LONGITUDE}&lang=ru_RU"
    headers = {
        "X-Yandex-API-Key": YANDEX_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        fact = data.get('fact', {})
        temp = fact.get('temp', 'N/A')
        feels_like = fact.get('feels_like', 'N/A')
        condition = fact.get('condition', 'N/A')
        wind_speed = fact.get('wind_speed', 'N/A')
        humidity = fact.get('humidity', 'N/A')
        pressure_mm = fact.get('pressure_mm', 'N/A')

        condition_ru = CONDITION_TRANSLATION.get(condition, "неизвестно")

        weather_message = (
            f"Погода в Иркутске:\n"
            f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"Состояние: {condition_ru}\n"
            f"Ветер: {wind_speed} м/с\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {pressure_mm} мм рт. ст."
        )
        await update.message.reply_text(weather_message, reply_markup=keyboard_spasibo())

    except requests.RequestException as e:
        await update.message.reply_text("Не удалось получить данные о погоде. Попробуйте позже.")
        print(f"Ошибка запроса к Яндекс.Погоде: {e}")

async def spasibo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Какое спасибо, ты вообще с какого района будешь? Надо говорить: от души, братан!",
        reply_markup=ReplyKeyboardRemove()
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я не понимаю эту команду. Попробуйте использовать /weather, чтобы узнать погоду, или /spasibo."
    )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("spasibo", spasibo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))  # Обработка неизвестных текстовых сообщений
    app.add_handler(MessageHandler(filters.COMMAND, unknown))  # Обработка неизвестных команд

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
