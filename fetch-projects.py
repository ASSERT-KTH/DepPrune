import requests
from bs4 import BeautifulSoup

req = requests.get('https://gist.github.com/anvaka/8e8fa57c7ee1350e3491')
req.encoding = 'utf-8'

soup = BeautifulSoup(req.text, features='html.parser')

divWithLinks = soup.find(
    'div', {'id': 'file-01-most-dependent-upon-md-readme'})

with open('readme.txt', 'w') as f:

    for link in divWithLinks.find_all('a'):
        projectLink = link.get('href') + '\n'
        print(projectLink)
        f.write(projectLink)
    # hrefInLink = link.get('href')

    # subReq = requests.get(hrefInLink)
    # subReq.encoding = 'utf-8'

    # subSoup = BeautifulSoup(subReq.text, features='html.parser')
    # depsNum = subSoup.find('a', {'id': 'package-tab-dependencies'})
    # print(depsNum.find('span'))
