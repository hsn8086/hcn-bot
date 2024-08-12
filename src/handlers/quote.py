#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Copyright (C) 2024. Suto-Commune
#  _
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  _
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  _
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File       : quote.py

@Author     : hsn

@Date       : 2024/8/12 上午11:21
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from io import BytesIO

from PIL import Image
from anyquote import quote
from anyquote import quote_twitter
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def async_quote_twitter(url):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, quote_twitter, url)


async def quote_handler(bot: AsyncTeleBot, message: Message):
    reply_msg = message.reply_to_message

    if len(sl := message.text.split(" ")) == 2:
        url = sl[1]

        m = await bot.send_message(message.chat.id, "generating quote...", reply_to_message_id=message.message_id)

        # img = await async_quote_twitter(url)
        _img = await async_quote_twitter(url)
        _io = BytesIO()
        _img.save(_io, format="PNG")
        _io.seek(0)
        await bot.delete_message(message.chat.id, m.message_id)

        await bot.send_photo(message.chat.id, photo=_io, reply_to_message_id=message.message_id)

    elif reply_msg:
        if u := reply_msg.forward_from:
            uid = u.id
            user_id = u.username
            user_name = " ".join(filter(lambda x: bool(x), [u.first_name, u.last_name]))
        else:
            u = reply_msg.from_user
            uid = u.id
            user_id = u.username
            user_name = " ".join(filter(lambda x: bool(x), [u.first_name, u.last_name]))
        text = reply_msg.text
        aviators = await bot.get_user_profile_photos(uid)

        aviator_fid = aviators.photos[0][-1].file_id
        f_path = (await bot.get_file(aviator_fid)).file_path
        ba = await bot.download_file(f_path)
        aviator_img = Image.open(BytesIO(ba))

        text = text.replace(chr(8203), "")
        text = text.replace(chr(8288), "")
        msg_url = "https://t.me/c/{}/{}".format(reply_msg.chat.id, reply_msg.message_id)
        date = datetime.utcfromtimestamp(reply_msg.date)
        quote_img = quote(user_name=user_name, user_id=user_id, context=text, user_avatar=aviator_img,
                          _time=date, source=msg_url)
        _io = BytesIO()
        quote_img.save(_io, format="PNG")
        _io.seek(0)
        await bot.send_photo(message.chat.id, photo=_io, reply_to_message_id=message.message_id)
    else:
        await bot.send_message(message.chat.id, "please reply to a message or provide a twitter url to quote.",
                               reply_to_message_id=message.message_id)

    return
