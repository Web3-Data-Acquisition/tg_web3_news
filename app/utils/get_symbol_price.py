import traceback

import loguru
from curl_cffi.requests import AsyncSession
from starlette.responses import JSONResponse

from app.con.config import settings


async def get_symbol_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        async with AsyncSession() as s:
            # r = await s.get(url, proxies=settings.proxies)
            r = await s.get(url)
            json_data = r.json()
            loguru.logger.info(json_data)
            data = json_data.get("price", None)
            return data

    except Exception as e:
        loguru.logger.exception(e)
        loguru.logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "code": 500},
        )
