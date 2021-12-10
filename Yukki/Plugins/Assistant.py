from inspect import getfullargspec

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import (ASSID, ASSISTANT_PREFIX, ASSNAME, BOT_ID, BOT_USERNAME,
                   LOG_GROUP_ID, MUSIC_BOT_NAME, SUDOERS, app, userbot)
from Yukki.Database import (approve_pmpermit, disapprove_pmpermit,
                            is_pmpermit_approved)

__MODULE__ = "Assistant"
__HELP__ = f"""

**Note:**
- Only for Sudo Users



{ASSISTANT_PREFIX[0]}block [ Reply to a User Message] 
- Memblokir Pengguna dari Akun Asisten.

{ASSISTANT_PREFIX[0]}unblock [ Reply to a User Message] 
- Buka blokir Pengguna dari Akun Asisten.

{ASSISTANT_PREFIX[0]}approve [ Reply to a User Message] 
- Menyetujui Pengguna untuk DM.

{ASSISTANT_PREFIX[0]}disapprove [ Reply to a User Message] 
- Menolak Pengguna untuk DM.

{ASSISTANT_PREFIX[0]}pfp [ Reply to a Photo] 
- Mengubah PFP akun Asisten.

{ASSISTANT_PREFIX[0]}bio [Bio text] 
- Perubahan Bio Akun Asisten.

"""

flood = {}


@userbot.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDOERS)
)
async def awaiting_message(_, message):
    user_id = message.from_user.id
    if await is_pmpermit_approved(user_id):
        return
    async for m in userbot.iter_history(user_id, limit=6):
        if m.reply_markup:
            await m.delete()
    if str(user_id) in flood:
        flood[str(user_id)] += 1
    else:
        flood[str(user_id)] = 1
    if flood[str(user_id)] > 5:
        await message.reply_text("Spam Terdeteksi. Pengguna Diblokir")
        await userbot.send_message(
            LOG_GROUP_ID,
            f"**Deteksi Spam Blok Pada Asisten**\n\n- **Pengguna yang Diblokir:** {message.from_user.mention}\n- **ID pengguna:** {message.from_user.id}",
        )
        return await userbot.block_user(user_id)
    results = await userbot.get_inline_bot_results(
        BOT_ID, f"permit_to_pm {user_id}"
    )
    await userbot.send_inline_bot_result(
        user_id,
        results.query_id,
        results.results[0].id,
        hide_via=True,
    )


@userbot.on_message(
    filters.command("approve", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def pm_approve(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Balas pesan pengguna untuk menyetujui."
        )
    user_id = message.reply_to_message.from_user.id
    if await is_pmpermit_approved(user_id):
        return await eor(message, text="User is already approved to pm")
    await approve_pmpermit(user_id)
    await eor(message, text="Pengguna disetujui untuk pm")


@userbot.on_message(
    filters.command("disapprove", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def pm_disapprove(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Balas pesan pengguna untuk menolak."
        )
    user_id = message.reply_to_message.from_user.id
    if not await is_pmpermit_approved(user_id):
        await eor(message, text="Pengguna sudah tidak disetujui untuk pm")
        async for m in userbot.iter_history(user_id, limit=6):
            if m.reply_markup:
                try:
                    await m.delete()
                except Exception:
                    pass
        return
    await disapprove_pmpermit(user_id)
    await eor(message, text="Pengguna tidak disetujui untuk pm")


@userbot.on_message(
    filters.command("block", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def block_user_func(_, message):
    if not message.reply_to_message:
        return await eor(message, text="Balas pesan pengguna untuk diblokir.")
    user_id = message.reply_to_message.from_user.id
    await eor(message, text="Berhasil memblokir pengguna")
    await userbot.block_user(user_id)


@userbot.on_message(
    filters.command("unblock", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def unblock_user_func(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Balas pesan pengguna untuk membuka blokir."
        )
    user_id = message.reply_to_message.from_user.id
    await userbot.unblock_user(user_id)
    await eor(message, text="Berhasil membuka blokir pengguna")


    
@userbot.on_message(
    filters.command("pfp", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def set_pfp(_, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text="Balas ke foto.") 
    photo = await message.reply_to_message.download()
    try: 
        await userbot.set_profile_photo(photo=photo)   
        await eor(message, text="Berhasil Mengubah PFP.")
    except Exception as e:
        await eor(message, text=e)
    
    
@userbot.on_message(
    filters.command("bio", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def set_bio(_, message):
    if len(message.command) == 1:
        return await eor(message , text="Berikan beberapa teks untuk ditetapkan sebagai bio.") 
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try: 
            await userbot.update_profile(bio=bio) 
            await eor(message , text="Bio diubah.") 
        except Exception as e:
            await eor(message , text=e) 
    else:
        return await eor(message , text="Berikan beberapa teks untuk ditetapkan sebagai bio.") 

flood2 = {}

@app.on_callback_query(filters.regex("pmpermit"))
async def pmpermit_cq(_, cq):
    user_id = cq.from_user.id
    data, victim = (
        cq.data.split(None, 2)[1],
        cq.data.split(None, 2)[2],
    )
    if data == "approve":
        if user_id != ASSID:
            return await cq.answer("Tombol Ini Bukan Untuk Anda")
        await approve_pmpermit(int(victim))
        return await app.edit_inline_text(
            cq.inline_message_id, "Pengguna Telah Disetujui Untuk PM."
        )

    if data == "block":
        if user_id != ASSID:
            return await cq.answer("Tombol Ini Bukan Untuk Anda")
        await cq.answer()
        await app.edit_inline_text(
            cq.inline_message_id, "Berhasil memblokir pengguna."
        )
        await userbot.block_user(int(victim))
        return await userbot.send(
            DeleteHistory(
                peer=(await userbot.resolve_peer(victim)),
                max_id=0,
                revoke=False,
            )
        )

    if user_id == ASSID:
        return await cq.answer("Ini Untuk Orang Lain.")

    if data == "to_scam_you":
        async for m in userbot.iter_history(user_id, limit=6):
            if m.reply_markup:
                await m.delete()
        await userbot.send_message(user_id, "Diblokir, Pergi scam orang lain.")
        await userbot.send_message(
            LOG_GROUP_ID,
            f"**Blokir Penipuan Pada Asisten**\n\n- **Pengguna yang Diblokir:** {cq.from_user.mention}\n- **ID pengguna:** {user_id}",
        )
        await userbot.block_user(user_id)
        await cq.answer()
    if data == "for_pro":
        async for m in userbot.iter_history(user_id, limit=6):
            if m.reply_markup:
                await m.delete()
        await userbot.send_message(user_id, f"Diblokir, Tidak Ada Promosi.")
        await userbot.send_message(
            LOG_GROUP_ID,
            f"**Blok Promosi Di Asisten**\n\n- **Pengguna yang Diblokir:** {cq.from_user.mention}\n- **ID Pengguna:** {user_id}",
        )
        await userbot.block_user(user_id)
        await cq.answer()
    elif data == "approve_me":
        await cq.answer()
        if str(user_id) in flood2:
            flood2[str(user_id)] += 1
        else:
            flood2[str(user_id)] = 1
        if flood2[str(user_id)] > 5:
            await userbot.send_message(
                user_id, "SPAM TERDETEKSI, PENGGUNA DIBLOKIR."
            )
            await userbot.send_message(
                LOG_GROUP_ID,
                f"**Deteksi Spam Blok Pada Asisten**\n\n- **Pengguna yang Diblokir:** {cq.from_user.mention}\n- **ID Pengguna:** {user_id}",
            )
            return await userbot.block_user(user_id)
        await userbot.send_message(
            user_id,
            "Gua lagi sibuk sekarang, akan segera menyetujui, JANGAN SPAM.",
        )


async def pmpermit_func(answers, user_id, victim):
    if user_id != ASSID:
        return
    caption = f"Hi, Gua {ASSNAME}, Ngapain lu kesini?, Lu diblokir kalo ngirim pesan spam lebih dari 5."
    audio_markup2 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"Add {MUSIC_BOT_NAME} Ke grup lu",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="To Scam You",
                    callback_data=f"pmpermit to_scam_you a",
                ),
                InlineKeyboardButton(
                    text="For Promotion", callback_data=f"pmpermit for_pro a"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Approve me", callback_data=f"pmpermit approve_me a"
                ),
                InlineKeyboardButton(
                    text="Approve", callback_data=f"pmpermit approve {victim}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"Support", url=f"https://t.me/fandasupport"
                ),
                InlineKeyboardButton(
                    text=f"Updates", url=f"https://t.me/fandaproject"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Blokir & Hapus", callback_data="pmpermit block {victim}"
                )
            ],
        ]
    )
    answers.append(
        InlineQueryResultArticle(
            title="do_not_click_here",
            reply_markup=audio_markup2,
            input_message_content=InputTextMessageContent(caption),
        )
    )
    return answers


@app.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.strip().lower()
        answers = []
        if text.split()[0] == "permit_to_pm":
            user_id = query.from_user.id
            victim = text.split()[1]
            answerss = await pmpermit_func(answers, user_id, victim)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )
    except:
        return


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
