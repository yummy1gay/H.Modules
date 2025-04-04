# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact codwiz@yandex.ru.

# ---------------------------------------------------------------------------------
# Name: WindowsKeys
# Description: Provides you Windows activation keys
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: WindowsKeys
# scope: WindowsKeys 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------

import logging
import json
import requests

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class WindowsKeys(loader.Module):
    """Provides you Windows activation keys"""

    strings = {
        "name": "WindowsKeys",
        "winkey": "✅ Your key: <code>{}</code>\n\n⚠ Warning! This key is not a pirate key. It is taken from the official Microsoft site and is intended for further activation via KMS-server",
        "error": "❌ An error occurred while retrieving the key. Please try again later.",
    }

    strings_ru = {
        "winkey": "✅ Ваш ключ: <code>{}</code>\n\n⚠ Внимание! Указанный ключ не является пиратским. Он взят с официального сайта Microsoft и предназначен для дальнейшей активации посредством KMS-сервера",
        "error": "❌ Произошла ошибка при получении ключа. Попробуйте позже.",
    }

    @loader.command(
        ru_doc="Открывает выбор ключа для активации Windows",
        en_doc="Opens the Windows activation key selection",
    )
    async def winkey(self, message):
        await self.inline.form(
            text="🔓 Выберите версию и издание Windows, для которой вам необходим ключ",
            message=message,
            reply_markup=[
                [
                    {
                        "text": "Windows 10/11 Pro",
                        "callback": self._inline__give_key,
                        "args": ["win10_11pro"],
                    }
                ],
                [
                    {
                        "text": "Windows 10/11 Enterprise LTSC",
                        "callback": self._inline__give_key,
                        "args": ["win10_11enterpriseLTSC"],
                    }
                ],
                [
                    {
                        "text": "Windows 8.1 Pro",
                        "callback": self._inline__give_key,
                        "args": ["win8.1pro"],
                    }
                ],
                [
                    {
                        "text": "Windows 8 Pro",
                        "callback": self._inline__give_key,
                        "args": ["win8pro"],
                    }
                ],
                [
                    {
                        "text": "Windows 7 Pro",
                        "callback": self._inline__give_key,
                        "args": ["win7pro"],
                    }
                ],
                [
                    {
                        "text": "Windows Vista Business",
                        "callback": self._inline__give_key,
                        "args": ["winvistabusiness"],
                    }
                ],
                [
                    {
                        "text": "🎈 Закрыть",
                        "action": "close",
                    }
                ],
            ],
            force_me=False,
            silent=True,
        )

    async def _inline__give_key(self, call, winver):
        url = "https://raw.githubusercontent.com/C0dwiz/H.Modules/refs/heads/assets/winkeys.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            await call.edit(self.strings["winkey"].format(data[winver]))

        except requests.exceptions.RequestException as e:
            logger.error("Request error: %e", e)
            await call.answer(self.strings("error"), show_alert=True)
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %e", e)
            await call.answer(self.strings("error"), show_alert=True)
        except KeyError as e:
            logger.error("Key error: %e", e)
            await call.answer(self.strings("error"), show_alert=True)

        except Exception as e:
            logger.exception("An unexpected error occurred: %e", e)
            await call.answer(self.strings("error"), show_alert=True)