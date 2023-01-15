import requests
from bs4 import BeautifulSoup


for num in range(85,101):
    curLink = 'https://libraries.io/search?keywords=nodejs&order=desc&page=' + str(num) + '&platforms=npm&sort=rank'

    req = requests.get(curLink)
    req.encoding = 'utf-8'

    soup = BeautifulSoup(req.text, features='html.parser')

    divWithLinks = soup.find_all(
        'div', {'class': 'project'})

    with open('top3000.txt', 'a') as f:

        for link in divWithLinks:
            projectLink = link.find('a').get('href') + '\n'
            f.write(projectLink)
    # hrefInLink = link.get('href')

    # subReq = requests.get(hrefInLink)
    # subReq.encoding = 'utf-8'

    # subSoup = BeautifulSoup(subReq.text, features='html.parser')
    # depsNum = subSoup.find('a', {'id': 'package-tab-dependencies'})
    # print(depsNum.find('span'))
