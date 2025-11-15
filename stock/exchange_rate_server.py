import asyncio  # 导入asyncio模块

from http_server import get_client
from tool import is_price_arrived


class EXCHANGE_RATE_CLIENT:
    def __init__(self, goal_diff, goals):
        self.goal_diff = goal_diff
        self.goals = goals

    async def get_exchange_rate(self):
        BASE_URLS = {
            # 更新频率：天
            'exchangerate-api': "https://api.exchangerate-api.com"
        }
        path = 'v4/latest/CNY'
        exchange_api_client = get_client(base_url=BASE_URLS["exchangerate-api"])
        return await exchange_api_client.get(endpoint=path)

    @staticmethod
    def judge_exchange_rate(cur_rates, goals, goal_diff):

        str_arr = []
        for cur_name, cur_goal in goals.items():
            rate_now = cur_rates[cur_name]
            b_goal = cur_goal['b']
            if cur_goal['R_to_currency']:
                my_rate = rate_now
                str_atob = f'RMB->{cur_name}'
            else:
                my_rate = 1 / rate_now
                str_atob = f'{cur_name}->RMB'
            str = f'{str_atob}: {my_rate}：目标价：{b_goal}，'

            is_arrived, precent_spread = is_price_arrived(b_goal, my_rate, goal_diff)
            if is_arrived:
                str += f'仅需{100 * precent_spread:.2f}%,已接近目标价'
            else:
                str += f'还需{100 * precent_spread:.2f}%'
            str_arr.append(str)
        return str_arr


async def exchange_rate_main():
    goal_diff = 0.01
    exchanges_goal = {'JPY': {'b': 22.00, 'R_to_currency': True}, 'USD': {'b': 7.00, 'R_to_currency': False},
                      'EUR': {'b': 7.50, 'R_to_currency': False}}
    rate = EXCHANGE_RATE_CLIENT(goal_diff, exchanges_goal)
    response = await rate.get_exchange_rate()
    cur_rates = response['data']['rates']
    str_arr = EXCHANGE_RATE_CLIENT.judge_exchange_rate(cur_rates=cur_rates, goals=exchanges_goal, goal_diff=goal_diff)
    print(str_arr)


if __name__ == "__main__":
    asyncio.run(exchange_rate_main())
