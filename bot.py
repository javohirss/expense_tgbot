from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand, Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import settings
from services.expense import ExpenseService


BOT_TOKEN = settings.BOT_TOKEN
BASE_URL = settings.BASE_URL

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found")

if not BASE_URL:
    raise ValueError("BASE_URL not found")

WEBHOOK_PATH = "/telegram/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

router = Router()


@router.message(Command("month"))
async def month_stats_handler(message: Message):
    telegram_user_id = message.from_user.id
    totals = await ExpenseService.get_current_month_totals_by_category(telegram_user_id)

    if not totals:
        await message.answer("За текущий месяц расходов пока нет.")
        return

    lines = [f"{item['category']}: {item['total_amount']}" for item in totals]
    answer = "Расходы по категориям с начала месяца:\n" + "\n".join(lines)
    await message.answer(answer)


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет. Отправь сообщение с тратами, а команда /month покажет расходы по категориям за текущий месяц."
    )


@router.message()
async def echo_handler(message: Message):
    raw_text = message.text

    if not raw_text:
        await message.answer("Отправь текстовое сообщение с расходами.")
        return

    telegram_user_id = message.from_user.id
    expenses = await ExpenseService.insert_expenses(telegram_user_id, raw_text)

    if not expenses:
        await message.answer("Не удалось распознать расходы.")
        return

    expenses_text = "\n".join(
        f"Трата `{expense.title}` добавлена в категорию `{expense.category}`."
        for expense in expenses
    )
    amounts_text = f"\n\nТраты на сумму: {sum(expense.amount for expense in expenses)} сомони"
    answer = expenses_text + amounts_text

    await message.answer(answer)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(WEBHOOK_URL)
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="month", description="Показать траты за текущий месяц"),
    ])
    print(f"Webhook set: {WEBHOOK_URL}")


async def on_shutdown(bot: Bot) -> None:
    await bot.session.close()
    print("Bot session closed")


def main():
    app = web.Application()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host="127.0.0.1", port=80)


if __name__ == "__main__":
    main()
