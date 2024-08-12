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
import logging
import tomllib
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from .handlers import start, quote_handler


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

    token = config.get("telegram", {}).get("token", None)
    if token is None or token == "":
        logger.error(f"token not found in config file.")
        return

    app = Application.builder().token(token=token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quote", quote_handler))
    app.run_polling()
