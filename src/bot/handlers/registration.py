from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from src.bot.constants import commands
from src.bot.keyboards import get_start_keyboard, get_confirm_keyboard
from src.core.logging.utils import logger_decor
from src.core.services.user import UserService


@logger_decor
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_chat.id
    user_service = UserService()
    await user_service.register_user(
        telegram_id=telegram_id,
        username=update.effective_chat.username,
    )
    keyboard = await get_start_keyboard(telegram_id=telegram_id)

    await context.bot.send_message(
        chat_id=telegram_id,
        text="Привет! 👋 \n\n"
        'Я бот платформы интеллектуального волонтерства <a href="https://procharity.ru/">ProCharity</a>. '
        "Буду держать тебя в курсе новых задач и помогу "
        "оперативно связаться с командой поддержки.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


@logger_decor
async def confirm_chosen_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_confirm_keyboard()

    user_service = UserService()
    telegram_id = update.effective_chat.id
    categories = await user_service.get_user_categories(telegram_id)
    text = ", ".join(categories.values())

    await context.bot.send_message(
        chat_id=telegram_id,
        text=f"Вот список твоих профессиональных компетенций: *{text}* Все верно?",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )


def init_app(app: Application):
    app.add_handler(CommandHandler(commands.START, start_command))
    app.add_handler(CallbackQueryHandler(confirm_chosen_categories, pattern=commands.GREETING_REGISTERED_USER))
