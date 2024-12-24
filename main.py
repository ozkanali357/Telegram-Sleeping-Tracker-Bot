import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

sleep_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command from user %s",
                update.message.from_user.username)
    await update.message.reply_text(
        'Hi! Use /sleep when you go to bed and /wake when you wake up.')


async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    sleep_time = datetime.datetime.now()
    sleep_data[user.id] = {'sleep': sleep_time}
    logger.info("User %s (%s) went to sleep at %s", user.username, user.id,
                sleep_time)
    await update.message.reply_text(f'Good night, {user.first_name}!')


async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    wake_time = datetime.datetime.now()
    if user.id in sleep_data and 'sleep' in sleep_data[user.id]:
        sleep_time = sleep_data[user.id]['sleep']
        sleep_duration = wake_time - sleep_time
        logger.info("User %s (%s) woke up at %s after sleeping for %s",
                    user.username, user.id, wake_time, sleep_duration)
        await update.message.reply_text(
            f'Good morning, {user.first_name}! You slept for {sleep_duration}.'
        )
    else:
        logger.info("User %s (%s) used /wake without a recorded sleep time",
                    user.username, user.id)
        await update.message.reply_text(
            'I don\'t have your sleep time recorded.')


def main() -> None:
    application = ApplicationBuilder().token(
        "the key for the bot").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sleep", sleep))
    application.add_handler(CommandHandler("wake", wake))

    application.run_polling()


if __name__ == '__main__':
    main()
