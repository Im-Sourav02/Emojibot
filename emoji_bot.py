import json
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "Your_BOT_TOKEN"
JSON_FILE = "emoji_effects.json"

def save_to_json(data, filename):
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.append(data)

    with open(filename, "w") as f:
        json.dump(existing, f, indent=4)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    effect_id = getattr(msg, 'effect_id', None)

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "from": msg.from_user.username if msg.from_user else "unknown",
        "text": msg.text,
        "effect_id": effect_id if effect_id else "None"
    }

    save_to_json(data, JSON_FILE)

    if effect_id:
        reply = f"🧾 Effect ID of emoji: `{effect_id}`"
    else:
        reply = "⚠️ No effect ID found. This emoji may not have a premium animation."

    await msg.reply_text(reply, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()
