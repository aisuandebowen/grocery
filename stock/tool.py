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
