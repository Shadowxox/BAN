import os
import logging
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, FloodWait, RPCError

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Config vars
API_ID = int(os.getenv("API_ID", "25297643"))
API_HASH = os.getenv("API_HASH", "f72c62f1eb9aeaf5feb35de38e3b30c3"))
BOT_TOKEN = os.getenv("BOT_TOKEN", "8257141650:AAH7IfehJm2EhNf2ov_qN8Ngdts3TLLHzBA"))
OWNER = int(os.getenv("OWNER", "8188588913"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "Sunomusicrebot")  # replace with your bot username

app = Client("banall", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# /start command
@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user = message.from_user
    await message.reply_photo(
        photo="https://files.catbox.moe/qej5mx.jpg",
        caption=(
            f"✦ » Hey {user.mention}\n"
            "✦ » This is a simple BanAll bot based on Pyrogram.\n\n"
            "✦ » Use /banall in any group (with admin power) to remove everyone.\n\n"
            "✦ » Powered By » @ll_ALPHA_BABY_lll"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚜️ Add Me ⚜️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton("🔸 Owner 🔸", url="https://t.me/ll_ALPHA_BABY_lll"),
                    InlineKeyboardButton("▫️ Updates ▫️", url="https://t.me/PURVI_SUPPORT"),
                ],
            ]
        ),
    )


# /banall command
@app.on_message(filters.command("banall") & filters.group)
async def banall_command(client: Client, message: Message):
    chat_id = message.chat.id
    sender = message.from_user

    if sender.id != OWNER:
        await message.reply_text("🚫 Only the owner can use this command.")
        return

    try:
        me = await client.get_me()
        bot_member = await client.get_chat_member(chat_id, me.id)
        if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
            await message.reply_text("❌ I need 'Ban Members' permission.")
            return
    except ChatAdminRequired:
        await message.reply_text("❌ I'm not admin in this group.")
        return

    await message.reply_text("⚔️ BanAll process started...")

    count = 0
    skipped_admins = 0
    skipped_owner = 0
    errors = 0

    async for member in client.get_chat_members(chat_id):
        user_id = member.user.id

        # Skip owner and bot itself
        if user_id == OWNER:
            skipped_owner += 1
            continue
        if user_id == me.id:
            continue

        # Skip admins
        if member.status in ("administrator", "creator"):
            skipped_admins += 1
            continue

        try:
            await client.ban_chat_member(chat_id, user_id)
            count += 1
            logging.info(f"Banned {user_id} from {chat_id}")
            await asyncio.sleep(0.2)  # small delay to avoid FloodWait
        except FloodWait as e:
            logging.warning(f"FloodWait: sleeping {e.value} seconds...")
            await asyncio.sleep(e.value)
        except RPCError as e:
            errors += 1
            logging.warning(f"Failed to ban {user_id}: {e}")
        except Exception as e:
            errors += 1
            logging.warning(f"Unexpected error banning {user_id}: {e}")

    await message.reply_text(
        f"✅ **BanAll Completed!**\n\n"
        f"🚷 Banned: {count}\n"
        f"⚙️ Skipped Admins: {skipped_admins}\n"
        f"👑 Skipped Owner: yes\n"
        f"⚠️ Errors: {errors}"
    )

    logging.info(f"BanAll finished: {count} banned, {skipped_admins} admins skipped.")


if __name__ == "__main__":
    app.start()
    print("🔥 BanAll Bot Started Successfully")
    idle()