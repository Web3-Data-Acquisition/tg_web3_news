import asyncio
import traceback

import loguru
from telethon import TelegramClient, events

from app.core.base_worker import BaseWorker

API_ID = 20464789
API_HASH = "87c3a2090b3c3fd98ea22da5e4d39a44"

client = TelegramClient("session", API_ID, API_HASH)


class TgStream(BaseWorker):
    def __init__(self):
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.queue = asyncio.Queue()

        self.client = TelegramClient("tg_session", self.api_id, self.api_hash)

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
        channel_name_to_id = {'Cointime中文资讯': 1895128149,
                              'Crypto_獵捕者合約帝': 1793451069,
                              '币圈新闻即时快讯🅥': 1668307169,
                              'BlockBeats': 1387109317,
                              '链捕手 ChainCatcher': 1515681710,
                              'Foresight News': 1526765830,
                              '金色财经/币圈快讯7*24小时': 1549184965,
                              '金色财经新闻频道': 1748596288,
                              'Telo News 简体中文 - 加密货币｜DeFi ｜Web3': 1525379130,
                              'TechFlow 深潮 ｜ News Feed': 1735732363,
                              '分叉财经(crypto news)': 1515857362,
                              '方程式新闻 BWEnews': 1279597711,
                              '半只香蕉News丨📣📣': 2117032512,
                              '【以太坊】币圈行情分析频道': 1880448894}
        self.client.add_event_handler(
            self.event_handler,
            events.NewMessage(
                chats=[
                    1895128149,
                    1793451069,
                    1668307169,
                    1387109317,
                    1515681710,
                    1526765830,
                    1549184965,
                    1748596288,
                    1525379130,
                    1735732363,
                    1515857362,
                    1279597711,
                    2117032512,
                    1880448894,
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
                await self.client.start()
                await self.client.send_message(2312527705, f'{result}')
            else:
                loguru.logger.error(f"不符合发送消息{result}")

