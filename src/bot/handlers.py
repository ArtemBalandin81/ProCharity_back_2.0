from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.bot.services.category import CategoryService


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Это бот платформы интеллектуального волонтерства " "ProCharity",
    )


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create button menu."""
    keyboard = [
        [InlineKeyboardButton(
            "Посмотреть открытые задания",
            callback_data="view_tasks"
        )],
        [InlineKeyboardButton(
            "Изменить компетенции",
            callback_data='change_category'
        )],
        [InlineKeyboardButton(
            "Отправить предложение/ошибку",
            callback_data="send_error_or_proposal"
        )],
        [InlineKeyboardButton(
            "Задать свой вопрос",
            callback_data="ask_your_question"
        )],
        [InlineKeyboardButton(
            "О платформе",
            callback_data="about_project"
        )],
        [InlineKeyboardButton(
            "⏹️ Остановить / ▶️ включить подписку на задания",
            callback_data="job_subscription"
        )],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выбери, что тебя интересует:", reply_markup=reply_markup
    )


async def categories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    category_service = CategoryService()
    categories = await category_service.get_unarchived_parents()

    categories_buttons = [
        [InlineKeyboardButton(category.name, callback_data=f"category_{category.id}")] for category in categories]
    keyboard.extend(categories_buttons)

    keyboard.extend([
        [InlineKeyboardButton(
            "Нет моих компетенций 😕",
            callback_data="add_categories"
        )],
        [InlineKeyboardButton(
            "Готово 👌",
            callback_data="confirm_categories"
        )]])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        "несколько). После этого, нажми на пункт \"Готово 👌\"",
        reply_markup=reply_markup
    )


async def subcategories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    category_service = CategoryService()
    parent_id = int(update.callback_query.data.split('_')[1])
    subcategories = await category_service.get_unarchived_subcategories(parent_id)

    categories_buttons = [
        [InlineKeyboardButton(category.name, callback_data=f'category_{parent_id}')] for category in subcategories]
    keyboard.extend(categories_buttons)

    keyboard.append(
        [InlineKeyboardButton(
            "Назад ⬅️",
            callback_data="change_category"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text(
        "Выберите категории",
        reply_markup=reply_markup
    )
