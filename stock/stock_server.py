import asyncio
import re

from http_server import get_client
from tool import is_price_arrived


class STOCK_CLIENT:
    def __init__(self, goal_diff, BASE_URLS, goals):
        self.goal_diff = goal_diff
        self.BASE_URLS = BASE_URLS
        self.goals = goals

    def set_stock_params(self, stocks):
        arr = []
        for stock_code in stocks.keys():
            st = stocks[stock_code]
            str = st['code_prefix'] + stock_code
            arr.append(str)
        return arr

    async def get_stock_info(self, stocks_goal, base_url):
        stock_client = get_client(base_url=base_url)
        params = {'q': ','.join(self.set_stock_params(stocks_goal))}
        response = await stock_client.get(params=params)
        stocks_now = response['data'].split(';')
        return stocks_now

    @staticmethod
    def judge_stock(stocks_now, stocks_goal, goal_diff):
        str_arr = []
        for stock in stocks_now:
            match = re.search(r'"(.*?)"', stock)
            if match:
                stock_info_now = match.group(1).split('~')
                name = stock_info_now[1]
                code = stock_info_now[2]
                price = stock_info_now[3]
                # 距离买入价剩百分之多少
                buy = stocks_goal[code]['b']
                str = f'{name}({code})：当前价{price}-->目标价{buy}，'
                is_arrived, precent_spread = is_price_arrived(buy, price, goal_diff)
                if is_arrived:
                    str += f'仅需{100 * precent_spread:.2f}%,已接近目标价'
                else:
                    str += f'还需{100 * precent_spread:.2f}%'
                str_arr.append(str)
        return str_arr


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


if __name__ == '__main__':
    asyncio.run(stock_main())
