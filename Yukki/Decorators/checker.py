from Yukki import BOT_USERNAME, LOG_GROUP_ID, app
from Yukki.Database import blacklisted_chats, is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "Lu __Admin Anonim__ Goblok!\nBalikin dulu ke akun asli lu."
            )
        blacklisted_chats_list = await blacklisted_chats()
        if message.chat.id in blacklisted_chats_list:
            await message.reply_text(
                f"**Blacklisted Chat**\n\nObrolan Lu Di Blacklist Sama Sudo User.Minta __SUDO USER__ buat whitelist obrolan lu.\nPeriksa Daftar Sudo User [Disini](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
            return await app.leave_chat(message.chat.id)
        if await is_on_off(1):
            if int(message.chat.id) != int(LOG_GROUP_ID):
                return await message.reply_text(
                    f"Bot lagi dalam masa Pemeliharaan. Maaf atas ketidaknyamanannya!"
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**Gbanned User**\n\nlu di gbanned buat make Bot.Minta __SUDO USER__ buat ungban.\nPeriksa Daftar Sudo User [Disini](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        blacklisted_chats_list = await blacklisted_chats()
        if CallbackQuery.message.chat.id in blacklisted_chats_list:
            return await CallbackQuery.answer(
                "Blacklisted Chat", show_alert=True
            )
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOG_GROUP_ID):
                return await CallbackQuery.answer(
                    "Bot lagi dalam masa Pemeliharaan. Maaf atas ketidaknyamanannya!",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "You're Gbanned", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
