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


def set_stock_params(stocks):
    arr = []
    for stock_code in stocks.keys():
        st = stocks[stock_code]
        str = st['code_prefix'] + stock_code
        arr.append(str)
    return arr


async def get_stock_info(stocks_goal, base_url):
    stock_client = get_client(base_url=base_url)
    params = {'q': ','.join(set_stock_params(stocks_goal))}
    response = await stock_client.get(params=params)
    stocks_now = response['data'].split(';')
    return stocks_now


def get_price_spread(goal, price):
    '''
    获取价差百分比
    :param goal: 目标价
    :param price: 当前价
    :return:
    '''
    goal = float(goal)
    price = float(price)
    return round((goal - price) / goal, 3)


def is_price_arrived(goal, price, goal_diff):
    '''
    判断价格是否达到预期（误差范围内）
    :param goal: 目标价
    :param price: 当前价
    :param goal_diff: 目标误差百分比
    :return:
    '''
    precent_spread = get_price_spread(goal, price)

    return abs(precent_spread) < goal_diff, precent_spread


def judge_stock(stocks_now, stocks_goal, goal_diff):
    for stock in stocks_now:
        match = re.search(r'"(.*?)"', stock)
        if match:
            stock_info_now = match.group(1).split('~')
            name = stock_info_now[1]
            code = stock_info_now[2]
            price = stock_info_now[3]
            # 距离买入价剩百分之多少
            buy = stocks_goal[code]['b']
            str = f'{name}({code})，当前价{price}-->目标价{buy}，'
            is_arrived, precent_spread = is_price_arrived(buy, price, goal_diff)
            if is_arrived:
                str += f'仅需{100 * precent_spread:.2f}%,已接近目标价'
            else:
                str += f'还需{100 * precent_spread:.2f}%'
            print(str)


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
    stocks_now = await get_stock_info(stocks_goal, base_url)
    judge_stock(stocks_now, stocks_goal, goal_diff)


async def exchange_rate_main():
    response = await get_exchange_rate()
    exchange_rates = response['data']['rates']
    goal_diff = 0.01

    exchanges_goal = {'JPY': {'b': 22.00, 'R_to_currency': True}, 'USD': {'b': 7.00, 'R_to_currency': False},
                      'EUR': {'b': 7.50, 'R_to_currency': False}}
    for cur_name, cur_goal in exchanges_goal.items():
        rate_now = exchange_rates[cur_name]
        b_goal = cur_goal['b']
        if cur_goal['R_to_currency']:
            my_rate = rate_now
            str_atob = f'RMB->{cur_name}'
        else:
            my_rate = 1 / rate_now
            str_atob = f'{cur_name}->RMB'
        str = f'{str_atob}: {my_rate}，目标价：{b_goal}，'

        is_arrived, precent_spread = is_price_arrived(b_goal, my_rate, goal_diff)
        if is_arrived:
            str += f'仅需{100 * precent_spread:.2f}%,已接近目标价'
        else:
            str += f'还需{100 * precent_spread:.2f}%'
        print(str)


async def job():
    await stock_main()
    await exchange_rate_main()


async def main():
    await job()


if __name__ == "__main__":
    asyncio.run(main())
