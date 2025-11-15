import asyncio
from datetime import datetime

from email_server import MYMAIL
from exchange_rate_server import EXCHANGE_RATE_CLIENT
from stock_server import STOCK_CLIENT


def init_email():
    token = "1cce7d6061aa19710124f0e2ca013fd2"
    from_email = "hello@demomailtrap.co"
    to_email = "boenchen0839@gmail.com"
    return MYMAIL(token, from_email, to_email)


def send_email(email, subject, text):
    try:
        email.send_email(subject, text)
    except Exception as e:
        print(e)


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
    try:
        stocks_now = await stock.get_stock_info(stocks_goal, base_url)
        str_arr = STOCK_CLIENT.judge_stock(stocks_now, stocks_goal, goal_diff)
        print('获取股票信息成功')
    except Exception as e:
        print(e)
        str_arr = []
    return str_arr


async def exchange_rate_main():
    goal_diff = 0.01
    exchanges_goal = {'JPY': {'b': 22.00, 'R_to_currency': True}, 'USD': {'b': 7.00, 'R_to_currency': False},
                      'EUR': {'b': 7.50, 'R_to_currency': False}}
    rate = EXCHANGE_RATE_CLIENT(goal_diff, exchanges_goal)
    try:
        response = await rate.get_exchange_rate()
        cur_rates = response['data']['rates']
        str_arr = EXCHANGE_RATE_CLIENT.judge_exchange_rate(cur_rates=cur_rates, goals=exchanges_goal,
                                                           goal_diff=goal_diff)
        print('获取汇率成功')
    except Exception as e:
        print(e)
        str_arr = []

    return str_arr


async def run_once():
    print('------本次程序启动------')
    # 并发执行
    tasks = [stock_main(), exchange_rate_main()]
    results = []
    for coro in asyncio.as_completed(tasks):
        res = await coro
        results.append('\n'.join(res))

    time_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    email = init_email()
    subject = f'Adam播报：股票汇率行情 {time_now}'
    text = f'{'\n'.join(results)}'
    try:
        send_email(email, subject, text)
        print('邮件发送成功')
    except Exception as e:
        print('发送失败', e)


if __name__ == '__main__':
    asyncio.run(run_once())
