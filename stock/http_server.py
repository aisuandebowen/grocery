import json

import httpx


class APIClient:
    def __init__(self, base_url: str, timeout: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def request(self, method: str, endpoint: str, params: dict = None):
        # 去除base_url后面多余斜杠、endpoint开头多余斜杠
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = await self.client.request(method.upper(), url, params=params)
            '''处理返回值'''
            return self.handle_response(response)
        except httpx.RequestError as e:
            return {"error": f"Request failed: {e}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}"}

    def handle_response(self, response):
        content_type = response.headers.get('Content-Type').lower()
        result = {"status_code": response.status_code}
        # 处理JSON响应
        if 'application/json' in content_type:
            try:
                result['data'] = response.json()
                result['format'] = 'json'
                return result
            except json.JSONDecodeError:
                # JSON格式声明但解析失败，降级为文本处理
                pass

        # 处理文本响应
        # 提取编码（从Content-Type的charset中，如"text/html; charset=gbk"）
        charset = 'utf-8'  # 默认编码
        if 'charset=' in content_type:
            charset = content_type.split('charset=')[-1].strip().lower()
            # 处理可能的异常编码名（如GB2312大写）
            charset = {'gb2312': 'gbk', 'gbk2312': 'gbk'}.get(charset, charset)

        # 尝试解码（优先用提取的编码，失败则尝试utf-8和gbk）
        content = response.content
        for encoding in [charset, 'utf-8', 'gbk']:
            try:
                text = content.decode(encoding)
                result['data'] = text
                result['format'] = 'text'
                result['encoding'] = encoding
                return result
            except UnicodeDecodeError:
                continue

        # 所有编码都失败，返回原始字节（作为最后的降级）
        result['data'] = content  # 字节类型
        result['format'] = 'binary'
        result['error'] = '无法解码响应内容，返回原始字节'
        return result

    async def get(self, endpoint: str = '', params: dict = None):
        return await self.request("GET", endpoint, params)

    async def close(self):
        await self.client.aclose()


# 🔧 工厂函数
def get_client(base_url: str) -> APIClient:
    return APIClient(base_url=base_url)
