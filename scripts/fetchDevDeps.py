import requests
from bs4 import BeautifulSoup
import time

# projectsFile = open('./top5.txt', 'r')

with open('./top100.txt') as file:
    packages = [line.rstrip() for line in file]

# urls = projectsFile.readlines()
with open("top100install.txt", "a") as myfile:
    idx = 0
    for package in packages:
        idx += 1
        npmUrl = "https://www.npmjs.com/package/" + package
        page = requests.get(npmUrl)
        time.sleep(1)
        soup = BeautifulSoup(page.text, 'html.parser')
        pres = soup.find_all('pre')
        print(package + '***************\n')

        if pres is not None:
            hasInfo = False
            for pre in pres:
                if "npm install " in pre.get_text() or "&nbsp;npm&nbsp;install" in pre.get_text() or "npm i" in pre.get_text() and package in pre.get_text():
                    installText = pre.get_text()
                    print(installText)
                    myfile.write(str(idx) + "," + package + "," + installText + "\n")
                    hasInfo = True
            

        if not hasInfo:
            myfile.write(str(idx) + "," + package + ",No info\n")
