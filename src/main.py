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
@File       : main.py

@Author     : hsn

@Date       : 2024/8/11 下午10:36
"""
import argparse
import asyncio
import logging
import tomllib
from pathlib import Path
from typing import Callable

from telebot.async_telebot import AsyncTeleBot

from .handlers import start,quote_handler


def handle_builder(bot: AsyncTeleBot):
    def _add_handler(handler: Callable, **kwargs):
        @bot.message_handler(**kwargs)
        async def _handler(message):
            await handler(bot=bot, message=message)

    return _add_handler


def main():
    # logging
    logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    logger = logging.getLogger('main')
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="config file path.", default="config.toml")
    config_path = Path(parser.parse_args().config)
    logger.info(f"config path: {config_path}")
    if not config_path.exists():
        logger.error(f"config file not found.")
        return

    try:
        with config_path.open("rb") as f:
            config = tomllib.load(f)
    except Exception as e:
        logger.error(f"error loading config file: {e}")
        return

    token: str = config.get("telegram", {}).get("token", "")
    if token is None or token == "":
        logger.error(f"token not found in config file.")
        return
    bot = AsyncTeleBot(token)
    add_handler = handle_builder(bot)
    add_handler(start, commands=["start"])
    add_handler(quote_handler, commands=["quote"])
    asyncio.run(bot.infinity_polling())

