import asyncio
import traceback
from itertools import cycle

import loguru
import requests
from telethon.sync import TelegramClient

from app.utils.gpt_translation import get_gpt_china_translation, get_gpt_translation, get_gpt_english_translation


async def get_moonshot_list():
    try:
        url = 'https://srv.moonshot.money/categories?limit=10'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


async def moonhost_data_processing(cycle_selector):
    try:
        info_list = await get_moonshot_list()
        selected_id = next(cycle_selector)
        if info_list:
            for index, row in enumerate(info_list):
                rwo_id = row.get("id", None)
                # if rwo_id and rwo_id in ['top_gainers', 'top_volume', 'top_market_caps', 'dogs', 'cats', 'frogs', 'new',
                #                          'ai']:
                if rwo_id and rwo_id == selected_id:
                    result_title, result_data = moonhost_info_processing(data=row)
                    await tg_send_mseeage(title=result_title, data=result_data)
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


def moonhost_info_processing(data: dict):
    try:
        if data:
            info_id = data.get("id", None)
            info_name = data.get("name", None)
            coins = data.get("coins", [])

            if info_id == 'top_volume':
                title = "Top Volume"
            elif info_id == "new":
                title = "News"
            else:
                title = info_name
            symbol_list = list()
            if coins:
                for coin_index, coin_row in enumerate(coins):
                    symbol_name = coin_row.get('name', None)
                    symbol_symbol = coin_row.get('ticker', None)
                    symbol_chain = coin_row.get('chain', None)
                    symbol_address = coin_row.get('contractAddress', None)
                    symbol_circulatingSupply = coin_row.get('circulatingSupply', None)
                    symbol_day = coin_row.get('day', None)
                    symbol_price = None
                    symbol_volume = None
                    symbol_holders = None
                    if symbol_day:
                        symbol_volume = symbol_day.get('volume', None)
                        symbol_price = symbol_day.get('price', None)
                        symbol_holders = symbol_day.get('holders', None)

                    # symbol_market_cap = float(symbol_price * float(symbol_circulatingSupply))
                    information = {
                        "symbol_name": symbol_name,
                        "symbol_symbol": symbol_symbol,
                        "symbol_address": symbol_address,
                        "symbol_price": symbol_price,
                        # "symbol_market_cap": symbol_market_cap,
                        "symbol_holders": symbol_holders,
                        "symbol_volume": symbol_volume,
                        "symbol_chain": symbol_chain
                    }
                    symbol_list.append(information)
            return title, symbol_list
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


async def tg_send_mseeage(title: str, data: list):
    try:
        api_id = 20464789
        api_hash = "87c3a2090b3c3fd98ea22da5e4d39a44"
        client = TelegramClient('session_tree_moonshot', api_id, api_hash)

        result_message = f"🚀🚀🎉🎉 {title} 🎉🎉🚀🚀\n\n"
        for index, row in enumerate(data):
            market_cap = row.get('symbol_market_cap', 0) / 1000000
            volume = row.get('symbol_volume', 0) / 1000000
            message = (
                f"symbol:       {row.get('symbol_symbol', None)}\n"
                f"name:         {row.get('symbol_name', None)}\n"
                f"address:      {row.get('symbol_address', None)}\n"
                f"price:        ${row.get('symbol_price', 0):.8f}\n"  # 保留8位小数
                # f"market_cap:   ${market_cap:.2f}M\n"  # 保留2位小数
                f"holders:      {row.get('symbol_holders')}\n"  # 保留2位小数
                f"24H volume:   ${volume:.2f}M\n"  # 保留2位小数
                f"chain:        {row.get('symbol_chain', None)}\n"
            )
            result_message += message + '\n'

        chinese_result = await get_gpt_china_translation(result_message)
        result_data = await get_gpt_translation(result_message)
        english_result = await get_gpt_english_translation(result_message)

        await client.start()
        if chinese_result:
            if len(chinese_result) > 4096:
                chinese_result = chinese_result[:4093] + '...'
            await client.send_message(2312527705, f'{chinese_result}')
            # 测试频道
            # await client.send_message(2303279286, f'{chinese_result}')

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
            await client.send_message(2375526101, f'{english_result}')
            # 测试频道
            # await client.send_message(2303279286, f'{result_data}')
        await client.disconnect()
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


async def moonshot_main():
    # 创建一个循环迭代器，用于依次循环选择 ['top_gainers', 'top_volume', 'top_market_caps']
    cycle_selector = cycle(['top_gainers', 'top_volume', 'top_market_caps'])

    while True:
        # 每分钟运行一次
        await moonhost_data_processing(cycle_selector)
        await asyncio.sleep(60)  # 等待 60 秒


if __name__ == '__main__':
    asyncio.run(moonshot_main())
