import asyncio
import traceback

import loguru
from telethon import TelegramClient, events

from app.core.base_worker import BaseWorker
from app.utils.delete_chinese import remove_chinese_translation
from app.utils.get_binance_symbol import get_support_symbols, extract_symbols
from app.utils.get_symbol_price import get_symbol_price
from app.utils.gpt_translation import get_gpt_translation
from app.utils.language_detection import language_detection

API_ID = 20464789
API_HASH = "87c3a2090b3c3fd98ea22da5e4d39a44"

client = TelegramClient("session1", API_ID, API_HASH)


class TgStream(BaseWorker):
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.queue = asyncio.Queue()

        self.client = TelegramClient("tg_session1", self.api_id, self.api_hash)

    async def event_handler(self, event):
        result = dict()
        try:
            channel_id = event.message.peer_id.channel_id

            # 获取群聊名字信息
            entity = await self.client.get_entity(channel_id)

            publish_time = event.date
            publish_time = int(publish_time.timestamp() * 1000)

            text = event.text
            channel_name = entity.title
            loguru.logger.info(f"title: {channel_name} | 频道id{channel_id} | 群名:{entity.title}"
                               f" | 内容:{text} | 时间:{publish_time}")

            # result["body"] = text
            # result["title"] = channel_name
            # result["time"] = publish_time

            await self.queue.put(text)

        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    async def run(self):
        await self.client.connect()
        channel_name_to_id = {
                              '方程式新闻 BWEnews': 1279597711,}
        self.client.add_event_handler(
            self.event_handler,
            events.NewMessage(
                chats=[
                    1279597711,

                ]
            )
        )

        await self.client.start()

        loguru.logger.info("start tuple")

        async for dialog in self.client.iter_dialogs():
            try:
                channel_name_to_id[dialog.name] = dialog.message.peer_id.channel_id
                loguru.logger.debug(f"{dialog.message.peer_id.channel_id} {dialog.name} {dialog.id}")
            except Exception as e:
                print(f"{dialog} {e}")

        while True:
            result = await self.queue.get()  # get the result from the queue

            if result != {}:
                loguru.logger.debug(result)

                symbol = None
                symbol_price = None
                if result:
                    results = remove_chinese_translation(result)
                    if results:
                        symbol_result = extract_symbols(results)
                        if symbol_result:
                            symbol = symbol_result[0]
                            symbols = symbol + 'USDT'
                            try:
                                symbol_price = await get_symbol_price(symbols)
                            except Exception as e:
                                symbol_price = None
                if symbol_price and symbol:
                    data = f"symbol: {symbol} " + "\n" + f"price: {symbol_price}" + "\n" + result
                elif symbol:
                    data = f"symbol: {symbol} " + "\n" + result
                else:
                    data = result

                Vietnamese_data = await get_gpt_translation(data)

                await self.client.start()
                if data:
                    await self.client.send_message(2312527705, f'{data}')
                if Vietnamese_data:
                    await self.client.send_message(2186132517, f'{Vietnamese_data}')

            else:
                loguru.logger.error(f"不符合发送消息{result}")
