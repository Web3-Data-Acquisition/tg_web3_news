import asyncio
import traceback

import loguru

import openai
from openai import AsyncOpenAI

from app.con.config import settings

# open_ai_client = AsyncOpenAI(
#     api_key=settings.API_KEY,
#     base_url=settings.API_BASE
# )
API_BASE: str = "https://api.openai-sb.com/v1/"
API_KEY: str = "sb-4dddef154335adacb0a1afbd2898053710ddecd9b47ba009"
open_ai_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=API_BASE
)
async def get_gpt_translation(message):
    try:
        prompt = f"""
            Please translate all text in the following paragraph into Vietnamese:
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


async def get_gpt_china_translation(message):
    try:
        prompt = f"""
            Please translate all the text in the following paragraph into Chinese:
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
    message = """symbol: BICO 
Bithumb Listing: [이벤트] 바이코노미(BICO), 퍼퍼(PUFFER) 원화 마켓 추가 기념 에어드랍 이벤트
$BICO
————————————
2024-11-25 14:11:10
source: https://feed.bithumb.com/notice/1645254"""
    result = await get_gpt_translation(message)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
