from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.bot.constants import commands, states
from src.bot.keyboards import get_categories_keyboard, get_subcategories_keyboard, MENU_KEYBOARD
from src.core.services.user import UserService


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_service = UserService()
    await user_service.register_user(
        telegram_id=update.effective_chat.id,
        username=update.effective_chat.username,
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Начнём",
                    callback_data=commands.GREETING,
                )
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! 👋 \n\n"
        'Я бот платформы интеллектуального волонтерства <a href="https://procharity.ru/">ProCharity</a>. '
        "Буду держать тебя в курсе новых задач и помогу "
        "оперативно связаться с командой поддержки.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    return states.GREETING


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create button menu."""
    keyboard = MENU_KEYBOARD
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выбери, что тебя интересует:", reply_markup=reply_markup)


async def categories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = await get_categories_keyboard()
    context.user_data["parent_id"] = None
    await update.message.reply_text("Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=reply_markup,
    )


async def subcategories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    parent_id = int(query.data.split("_")[1])
    context.user_data["parent_id"] = parent_id

    reply_markup = await get_subcategories_keyboard(parent_id, context)
    await query.message.edit_text("Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=reply_markup,
    )


async def select_subcategory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    subcategory_match = context.match

    if subcategory_match:
        subcategory_id = int(subcategory_match.group(1))
        selected_categories = set(context.user_data.get("selected_categories", []))
        if subcategory_id in selected_categories:
            selected_categories.remove(subcategory_id)
        else:
            selected_categories.add(subcategory_id)
        context.user_data["selected_categories"] = list(selected_categories)

        parent_id = context.user_data["parent_id"]
        reply_markup = await get_subcategories_keyboard(parent_id, context)

    await query.message.edit_text("Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=reply_markup,
    ) 


async def back_subcategory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    back_to_match = context.match
    if back_to_match:
        reply_markup = await get_categories_keyboard()

    await query.message.edit_text("Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=reply_markup,
    )
