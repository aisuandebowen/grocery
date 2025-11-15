import asyncio
import time
from datetime import datetime

from main_task import run_once

INTERVAL_SEC = 60 * 60


def check_time(time_goal=17):
    now = datetime.now()
    hour = now.hour

    return time_goal == hour


def run():
    while True:
        try:
            flag = check_time()
            if flag:
                asyncio.run(run_once())
        except Exception as e:
            print(e)

        time.sleep(INTERVAL_SEC)


if __name__ == '__main__':
    run()
