import asyncio

from app.services.get_moonshot_list import moonshot_main
# from app.services.tree_news_data import listen_to_tree_news
# from app.tg_stream import TgStream


# async def run_tg_stream():
#     tg = TgStream()
#     result = await tg.run()


# async def run_tree_news():
#     tree_news_result = await listen_to_tree_news()


async def moonshot_news():
    tree_news_result = await moonshot_main()


async def main():
    # 使用 asyncio.gather 来并行运行两个任务
    await asyncio.gather(
        # run_tg_stream(),
        # run_tree_news(),
        moonshot_news()
    )


if __name__ == '__main__':
    asyncio.run(main())
