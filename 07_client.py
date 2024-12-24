import sys
from datetime import datetime, timedelta

import httpx
import asyncio
import platform
from pprint import PrettyPrinter

pp = PrettyPrinter(depth=5, width=100, compact=False)

class HttpError(Exception):
    pass


async def request(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        # test = await client.get('https://www.google.com')
        # print(test.text)
        if r.status_code == 200:
            result = r.json()
            return result
        else:
            raise HttpError(f"Error status: {r.status_code} for {url}")


async def main(index_day):
    d = datetime.now() - timedelta(days=int(index_day))
    if datetime.now() - timedelta(days=int(10)) <= d <= datetime.now():
        shift = d.strftime("%d.%m.%Y")
        try:
            response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
            return pp.pprint(response)
        except HttpError as err:
            print(err)
            return None


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(sys.argv)
    r = asyncio.run(main(sys.argv[1]))
    print(r)
