import asyncio
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters, ClientSession


# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里我们使用 uv 来运行 web_search.py
    command='uv',
    # 运行的参数
    args = [
        "--directory",
        "tool/yahoo-finance-mcp",
        "run",
        "server.py",
    ]
    # 环境变量，默认为 None，表示使用当前环境变量
    # env=None
)


async def main():
    # 创建 stdio 客户端
    async with stdio_client(server_params) as (stdio, write):
        # 创建 ClientSession 对象
        async with ClientSession(stdio, write) as session:
            # 初始化 ClientSession
            await session.initialize()

            # 列出可用的工具
            response = await session.list_tools()
            # print(response)

            # 调用工具
            response = await session.call_tool('get_historical_stock_prices', {
                'ticker': 'NVDA',
                'period': '5d',
                'interval': '1d',
            })
            print('回复：', response)
            ## 时间缓冲
            await asyncio.sleep(0.5)
    


if __name__ == '__main__':
    asyncio.run(main())
