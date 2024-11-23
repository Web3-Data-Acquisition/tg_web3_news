import asyncio
import traceback

import loguru
from lingua import Language, LanguageDetectorBuilder

language = [Language.INDONESIAN, Language.ENGLISH, Language.FRENCH,
            Language.GERMAN, Language.SPANISH, Language.CHINESE]
detector = LanguageDetectorBuilder.from_languages(*language).build()


async def language_detection(tweet):
    """对输入的语言进行检测，"""
    try:
        result = detector.detect_language_of(tweet)
        return result
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


async def main():
    try:
        # tweet = "mbakk ini beneran udah ada wifi ?"  # INDONESIAN
        # tweet = "Every morning, the sun rises,"  # ENGLISH
        tweet = """Tree News: [🌲] TRUMP TEAM PREPARING TO ANNOUNCE BESSENT AS TREASURY SECRETARY: BBG
        Tree News: [🌲] 特朗普团队准备宣布贝森特出任财政部长：BBG

        ————————————
        2024-11-23 07:03:18
        source: https://twitter.com/News_Of_Alpha/status/1860096745494990861"""
        # tweet = "早上好啊！"  # CHINESE
        result = await language_detection(tweet=tweet)
        print(result)
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


if __name__ == '__main__':
    asyncio.run(main())
