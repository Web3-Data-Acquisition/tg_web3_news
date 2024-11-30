import asyncio
import signal
import ssl
import traceback

import loguru
import websockets
import json
from loguru import logger
from telethon.sync import TelegramClient, events

from app.utils.gpt_translation import get_gpt_translation, get_gpt_china_translation, get_gpt_english_translation


def close_ws(loop, ws):
    loop.call_soon_threadsafe(ws.close)


async def safe_websockets(*args, **kwargs):
    go_continue = True
    while go_continue:
        loop = asyncio.get_running_loop()
        ws = None
        try:
            ws = await websockets.connect(*args, **kwargs)
            loop.add_signal_handler(signal.SIGTERM, close_ws, loop, ws)
            yield ws
        except Exception as e:
            loguru.logger.error(f"{e}||{traceback.format_exc()}")
            go_continue = False
            # await ws.close()
        finally:
            if ws is not None:
                await ws.close()
            if signal.SIGTERM in loop._signal_handlers:
                loop.remove_signal_handler(signal.SIGTERM)


API_ID = 20464789
API_HASH = "87c3a2090b3c3fd98ea22da5e4d39a44"


#
# client = TelegramClient("session", API_ID, API_HASH)


async def listen_to_tree_news():
    while True:  # 持续尝试连接
        try:
            # cookie = "tree_login_cookie=s%3A8Ymw67Jgjoi17eCg4zlEArABYU1ITAvC.cZfzz12wgwFEq3acfrot8370gLMmWXMqunkTZRf39%2Fo"
            cookie = "tree_login_cookie=s%3ALHAPUfLQATiyC6OsD2y5_WwPDUXYXSNw.03pXdK2G7nVaSqQ9b9ARLtyihurFo6vutjsc59Ib8yE"

            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            extra_headers = {"Cookie": cookie}
            uri = "wss://news.treeofalpha.com/ws"  # 将此更改为您要连接的WebSocket服务器地址
            async with websockets.connect(
                    uri,
                    extra_headers=extra_headers,
                    ssl=ssl_context,
                    ping_interval=10,
                    ping_timeout=10
            ) as ws:
                async for response in ws:
                    response = json.loads(response)
                    print(response)
                    title = response.get("title", None)
                    body = response.get("body", None)
                    link = response.get("link", None)
                    source = response.get("source", None)

                    if source in ['Proposals', 'Binance EN', 'Arkham']:
                        continue

                    if title and body and link:
                        result = f"{title}" + "\n" + body + "\n" + link
                    elif title and body:
                        result = f"{title}" + "\n" + body
                    elif title:
                        result = f"{title}"
                    elif body:
                        result = f"{body}"
                    else:
                        continue
                    chinese_result = await get_gpt_china_translation(result)
                    result_data = await get_gpt_translation(result)
                    english_result = await get_gpt_english_translation(result)

                    async with TelegramClient('session_tree', API_ID, API_HASH) as client:
                        # 中文频道
                        if chinese_result:
                            if len(chinese_result) > 4096:
                                chinese_result = chinese_result[:4093] + '...'
                            await client.send_message(2312527705, f'{chinese_result}')
                            # 测试频道
                            # await client.send_message(2303279286, f'{result}')

                        # 越南语频道
                        if result_data:
                            if len(result_data) > 4096:
                                result_data = result_data[:4093] + '...'
                            await client.send_message(2186132517, f'{result_data}')
                            # 测试频道
                            # await client.send_message(2303279286, f'{result_data}')
                        if english_result:
                            if len(english_result) > 4096:
                                english_result = english_result[:4093] + '...'
                            await client.send_message(2429590708, f'{english_result}')
                            # 测试频道
                            # await client.send_message(2303279286, f'{english_result}')
        except Exception as e:
            print(f"Failed to connect to WebSocket: {e}")
        finally:
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)  # 等待 5 秒后重新连接
        await asyncio.sleep(1)


async def main():
    result = await listen_to_tree_news()


# 运行函数
asyncio.run(main())
