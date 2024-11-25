import asyncio
import traceback

import loguru

import openai
from openai import AsyncOpenAI

from app.con.config import settings

open_ai_client = AsyncOpenAI(
    api_key=settings.API_KEY,
    base_url=settings.API_BASE
)


async def get_gpt_translation(message):
    try:
        prompt = f"""
            Please translate the following text into Vietnamese:
            "{message}"
        """
        second_retry_limit = 3
        second_retry_count = 0
        second_successful_completion = False

        while (
                second_retry_count < second_retry_limit
                and not second_successful_completion
        ):
            try:
                result = await open_ai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                )
                second_successful_completion = True  # 标记成功
            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                second_retry_count += 1  # 递增重试次数

            answer = result.choices[0].message.content
            return answer
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())


async def main():
    message = """Bybit Listing: Bybit to list MORPHOUSDT Perpetual Contract
————————————
2024-11-22 16:58:00
source: https://www.bybit.com/trade/usdt/MORPHOUSDT"""
    result = await get_gpt_translation(message)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
