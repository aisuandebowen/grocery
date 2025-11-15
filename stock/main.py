import asyncio
import time

from main_task import run_once

INTERVAL_SEC = 0.1 * 60


def run():
    while True:
        try:
            asyncio.run(run_once())
        except Exception as e:
            print(e)

        time.sleep(INTERVAL_SEC)


if __name__ == '__main__':
    run()
