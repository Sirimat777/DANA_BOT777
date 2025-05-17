import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN переменная окружения не установлена!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kaspi_url = "https://kaspi.kz/transfer/77761677049"
    message = (
        "Ақпаратты жүктеп алу үшін Kaspi арқылы төлем жасауыңыз қажет.\n\n"
        "Kaspi Gold: +7 776 167 7049\n"
        "Сома: 1000 тг\n\n"
        "Төмендегі батырма арқылы төлем жасаңыз:"
    )
    keyboard = [[InlineKeyboardButton("Kaspi төлем жасау", url=kaspi_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup)
    await update.message.reply_text("Төлем жасағаннан кейін, чек скриншотын немесе фотосын осында жіберіңіз.")

async def handle_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Чек қабылданды. Міне, сіздің PDF файлыңыз:")
        with open("attached_assets/Баланы дұрыс дамыту сатылары.pdf", "rb") as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="Баланы дұрыс дамыту сатылары.pdf"
            )
    except Exception as e:
        await update.message.reply_text("Кешіріңіз, файлды жіберу кезінде қате шықты. Әкімшіге хабарласыңыз.")
        print(f"❌ Ошибка при отправке PDF: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.PDF, handle_payment_proof))
    print("✅ Бот запущен.")
    application.run_polling()

if __name__ == "__main__":
    main()
