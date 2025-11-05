import asyncio  # 导入asyncio模块
import re

from http_server import get_client


def send_email(data):
    pass


async def get_exchange_rate():
    BASE_URLS = {
        # 更新频率：天
        'exchangerate-api': "https://api.exchangerate-api.com"
    }
    path = 'v4/latest/CNY'
    exchange_api_client = get_client(base_url=BASE_URLS["exchangerate-api"])
    return await exchange_api_client.get(endpoint=path)


async def get_stock_info():
    BASE_URLS = {
        # 腾讯股票数据API eg: https://qt.gtimg.cn/q=sz000858
        "tencent_api": "https://qt.gtimg.cn"
    }
    stock_client = get_client(base_url=BASE_URLS["tencent_api"])
    stocks_goal = {'sh601127': {'b': 130.00}, 'sh601021': {'b': 52.00}, 'sz002583': {'b': 11.00},
                   'sz002765': {'b': 12.50}}
    params = {'q': ','.join(stocks_goal.keys())}
    response = await stock_client.get(params=params)
    box = response['data'].split(';')[0]
    match = re.search(r'"(.*?)"', box)
    if match:
        stock_info = match.group(1).split('~')
        code = stock_info[2]
        price = stock_info[3]
        print(code, price)


def job():
    get_stock_info()


async def main():
    await get_stock_info()
    # response = await get_exchange_rate()
    # exchange_rates = response['data']['rates']
    # to_JPY = exchange_rates['JPY']
    # to_USD = exchange_rates['USD']
    # to_EUR = exchange_rates['EUR']
    # exchange_goal = {'JPY': 22.00, 'USD': 7.00, 'EUR': 7.50}
    # RMB_to_JPY = to_JPY
    # USD_to_RMB = 1 / to_USD
    # EUR_to_RMB = 1 / to_EUR


if __name__ == "__main__":
    asyncio.run(main())
