import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time

projectsFile = open('./top10.txt', 'r')

urls = projectsFile.readlines()


class WebScraper(object):
    def __init__(self, urls):
        self.urls = urls
        # Global Place To Store The Data:
        self.all_data = []
        self.master_dict = []
        # Run The Scraper:
        asyncio.run(self.main())

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                text = await response.text()
                print(url)
                time.sleep(1)

                html = BeautifulSoup(text, features='html.parser')
                depTabs = html.find(
                    'a', {'id': 'package-tab-dependencies'})
                print(depTabs)

                if depTabs is not None:
                    depsNum = depTabs.find('span')
                    depStr = url + ', deps: ' + depsNum.get_text() + '\n'
                    print(depStr)
                    with open('depsinfo.txt', 'w') as f:
                        f.write(depStr)
                    return {'url': url, "deps: ": depsNum.get_text()}

        except Exception as e:
            print(str(e))

    async def extract_title_tag(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            return soup.title
        except Exception as e:
            print(str(e))

    # def executeFunc(headers, urls):

    async def main(self):
        tasks = []
        headers = {
            "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

        async with aiohttp.ClientSession(headers=headers) as session:

            for url in self.urls:
                tasks.append(self.fetch(session, url))

            htmls = await asyncio.gather(*tasks)
            self.all_data.extend(htmls)

            print(self.all_data)


loop = asyncio.get_event_loop()
loop_result = loop.run_until_complete(WebScraper(urls=urls, loop=loop))
# print(scraper.master_dict)
# print(len(scraper.all_data))
