import re

import httpx


def run():
    stock_code = "sz000858"
    base_url = f"https://qt.gtimg.cn"
    url = f"{base_url}/q={stock_code}"
    res = httpx.get(url)
    content_arr = get_content_arr(res.text)
    price_now = get_price(content_arr)
    print(price_now)


def get_content_arr(str):
    pattern = r'"([^"]*)"'
    match = re.search(pattern, str)
    arr = []
    if match:
        content = match.group(1)
        arr = content.split("~")
    return arr


def get_price(content_arr):
    return content_arr[3]


if __name__ == "__main__":
    run()
