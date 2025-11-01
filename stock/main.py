import asyncio  # 导入asyncio模块

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
    response = await exchange_api_client.get(endpoint=path)
    print(response)


async def get_stock_info():
    BASE_URLS = {
        # 腾讯股票数据API eg: https://qt.gtimg.cn/q=sz000858
        "tencent_api": "https://qt.gtimg.cn"
    }
    stock_client = get_client(base_url=BASE_URLS["tencent_api"])
    params = {'q': 'sz000858'}
    response = await stock_client.get(params=params)
    print(response)


def job():
    get_stock_info()


async def main():
    # await get_stock_info()
    await get_exchange_rate()


if __name__ == "__main__":
    asyncio.run(main())
