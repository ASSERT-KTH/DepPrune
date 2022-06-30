import requests
from bs4 import BeautifulSoup

curLink = 'https://libraries.io/search?keywords=nodejs&languages=&order=desc&page=2&platforms=npm&sort=dependents_count'

req = requests.get(curLink)
req.encoding = 'utf-8'

soup = BeautifulSoup(req.text, features='html.parser')

divWithLinks = soup.find_all(
    'div', {'class': 'project'})

with open('top31_60.txt', 'w') as f:

    for link in divWithLinks:
        projectLink = link.find('a').get('href') + '\n\n\n'
        f.write(projectLink)
    # hrefInLink = link.get('href')

    # subReq = requests.get(hrefInLink)
    # subReq.encoding = 'utf-8'

    # subSoup = BeautifulSoup(subReq.text, features='html.parser')
    # depsNum = subSoup.find('a', {'id': 'package-tab-dependencies'})
    # print(depsNum.find('span'))
