from typing import Dict, List, Union

from Yukki import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "Gua perlu jadi admin dengan beberapa izin:\n"
                + "\n- **Manage_Video_Chats:** Untuk mengelola obrolan suara"
                + "\n- **Ban_Users:** Untuk menggunakan perintah Gban"
                + "\n- **Delete_Messages:** Untuk menghapus Sampah yang Dicari Bot"
                + "\n- **Invite_Users**: Untuk mengundang asisten ke dalam grup."
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "Gua ga punya izin yang diperluin buat melakukan tindakan ini."
                + "\n**Izin:** __MANAGE VOICE CHATS__"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "Gua ga punya izin yang diperluin buat melakukan tindakan ini."
                + "\n**Izin:** __DELETE MESSAGES__"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "Gua ga punya izin yang diperluin buat melakukan tindakan ini."
                + "\n**Izin:** __INVITE USERS VIA LINK__"
            )
            return
        return await mystic(_, message)

    return wrapper
