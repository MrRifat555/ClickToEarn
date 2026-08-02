from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ref = None

    if context.args:
        ref = context.args[0]

    await update.message.reply_text(
        f"""
🎉 Welcome to Click To Earn

Referral:
{ref}
"""
    )
