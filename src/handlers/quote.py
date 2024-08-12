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
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO

from PIL import Image
from anyquote import quote, quote_twitter
from telegram import Update


async def async_quote_twitter(url):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        img = await loop.run_in_executor(pool, quote_twitter, url)
async def quote_handler(update: Update, context):
    reply_msg = update.message.reply_to_message

    if len(sl := update.message.text.split(" ")) == 2:
        url = sl[1]
        m = await update.message.reply_text("generating quote...")

        #img = await async_quote_twitter(url)
        await asyncio.sleep(10)
        _img=quote_twitter(url)
        _io = BytesIO()
        img.save(_io, format="PNG")
        _io.seek(0)
        await m.delete()
        await update.message.reply_photo(photo=_io, reply_to_message_id=update.message.message_id)

    elif reply_msg:
        bot = update.message.get_bot()
        if u := reply_msg.api_kwargs.get("forward_from", {}):
            uid = u.get("id")
            user_id = u.get("username")
            user_name = " ".join(filter(lambda x: bool(x), [u.get("first_name"), u.get("last_name")]))
        else:
            u = reply_msg.from_user
            uid = u.id
            user_id = u.username
            user_name = " ".join(filter(lambda x: bool(x), [u.first_name, u.last_name]))
        text = reply_msg.text
        aviators = await bot.get_user_profile_photos(uid)
        aviator_fid = aviators.photos[0][-1].file_id
        ba = await (await bot.get_file(aviator_fid)).download_as_bytearray()

        aviator_img = Image.open(BytesIO(ba))
        print(reply_msg)
        print(reply_msg.date.strftime("%Y-%m-%d %H:%M:%S"))
        text = text.replace(chr(8203), "")
        text = text.replace(chr(8288), "")
        msg_url = reply_msg.link
        quote_img = quote(user_name=user_name, user_id=user_id, context=text, user_avatar=aviator_img,
                          _time=reply_msg.date.astimezone(reply_msg.date.tzinfo), source=msg_url)
        _io = BytesIO()
        quote_img.save(_io, format="PNG")
        _io.seek(0)
        await update.message.reply_photo(photo=_io, reply_to_message_id=reply_msg.message_id, quote=True)
    else:
        await update.message.reply_text("please reply to a message or provide a twitter url to quote.", quote=True)
    return
