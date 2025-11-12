import asyncio

from exchange_rate_server import EXCHANGE_RATE_CLIENT
from stock_server import STOCK_CLIENT


async def stock_main():
    goal_diff = 0.03
    BASE_URLS = {
        # 腾讯股票数据API eg: https://qt.gtimg.cn/q=sz000858
        "tencent_api": "https://qt.gtimg.cn"
    }
    api = 'tencent_api'
    base_url = BASE_URLS[api]

    stocks_goal = {'601127': {'b': 130.00, 'code_prefix': 'sh'}, '601021': {'b': 52.00, 'code_prefix': 'sh'},
                   '002583': {'b': 11.00, 'code_prefix': 'sz'},
                   '002765': {'b': 12.50, 'code_prefix': 'sz'}}
    stock = STOCK_CLIENT(goal_diff, BASE_URLS, stocks_goal)
    stocks_now = await stock.get_stock_info(stocks_goal, base_url)
    str_arr = STOCK_CLIENT.judge_stock(stocks_now, stocks_goal, goal_diff)
    print(str_arr)


async def exchange_rate_main():
    goal_diff = 0.01
    exchanges_goal = {'JPY': {'b': 22.00, 'R_to_currency': True}, 'USD': {'b': 7.00, 'R_to_currency': False},
                      'EUR': {'b': 7.50, 'R_to_currency': False}}
    rate = EXCHANGE_RATE_CLIENT(goal_diff, exchanges_goal)
    response = await rate.get_exchange_rate()
    cur_rates = response['data']['rates']
    str_arr = EXCHANGE_RATE_CLIENT.judge_exchange_rate(cur_rates=cur_rates, goals=exchanges_goal, goal_diff=goal_diff)
    print(str_arr)


async def run():
    # 并发执行
    tasks = [stock_main(), exchange_rate_main()]
    for coro in asyncio.as_completed(tasks):
        await coro


if __name__ == '__main__':
    asyncio.run(run())
