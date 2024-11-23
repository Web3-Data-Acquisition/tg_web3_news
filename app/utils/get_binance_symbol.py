import asyncio
import re

import requests

BASE_URL = "https://api.binance.com"


async def get_support_symbols():
    """获取binance所有币对"""
    res = []
    end_point = "/api/v3/exchangeInfo"
    resp = requests.get(BASE_URL + end_point)

    for symbol_info in resp.json()["symbols"]:
        if symbol_info["status"] == "TRADING":
            symbol = "{}/{}".format(symbol_info["baseAsset"].upper(), symbol_info["quoteAsset"].upper())
            res.append(symbol)

    symbol_list = list()
    for symbol in res:
        symbol_split = symbol.split("/")

        symbol_list.append(symbol_split[0])

    symbol_list = list(set(symbol_list))
    return symbol_list

async def check_symbols_in_tweet(tweet):
    # 获取支持的符号列表
    symbol_list = await get_support_symbols()
    # 检查每个符号是否在tweet中出现
    symbols_in_tweet = [symbol for symbol in symbol_list if symbol in tweet]
    return symbols_in_tweet


def extract_symbols(text):
    # 使用正则表达式查找所有以$符号开始的词
    symbols = re.findall(r'\$(\w+)', text)
    return symbols

async def main():
    tweet = """BWENEWS AUTO: SUI: Sui Enters Strategic Partnership with Franklin Templeton Digital Assets
方程式新闻自动发布: SUI：Sui 与富兰克林邓普顿数字资产建立战略合作伙伴关系


$SUI
————————————
2024-11-22 22:00:14"""

    symbol_list = extract_symbols(tweet)
    print(symbol_list)


if __name__ == '__main__':
    asyncio.run(main())
