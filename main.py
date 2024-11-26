import asyncio

from app.services.tree_news_data import listen_to_tree_news
from app.tg_stream import TgStream


async def main():
    tg = TgStream()
    result = await tg.run()
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
