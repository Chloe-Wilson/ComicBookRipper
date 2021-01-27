import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from threading import Thread

def run(target):
    try:
        dir = 'D:/Books/' + target.split('/')[len(target.split('/')) - 2].replace('-', '')
        try:
            os.mkdir(dir)
        except:
            pass

        response = requests.get(target)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
        else:
            return
        links = soup.find_all('a', href=True, title=True)
        links.pop(0)
        links.pop(0)
        links = links[::-1]
        links.pop(0)

        issue = 0

        for link in links:
            issue += 1
            link['title'] = link['title'].replace('.', '')
            link['title'] = link['title'].replace('…', '')
            link['title'] = link['title'].replace(':', '')
            link['title'] = link['title'].replace('#', '')
            link['title'] = link['title'].replace('/', '')
            link['title'] = link['title'].replace('?', '')
            if link['title'][len(link['title']) - 1] != ' ':
                link['title'] = link['title'] + ' '
            link['title'] = link['title'] + str(issue)
            try:
                os.mkdir(dir + '/' + link['title'])
            except:
                if os.path.isfile(dir + '/' + link['title'] + '/Done.txt'):
                    continue
            print(link['title'] + '/' + str(len(links)))
            response = requests.get(link['href'])
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                continue
            picture = 0
            for pic in soup.find_all('img'):
                if 'blogspot' in str(pic):
                    picture += 1
                    if 'http' in pic['src']:
                        response = requests.get(pic['src'])
                    else:
                        response = requests.get('http:' + pic['src'])
                    file = open(dir + '/' + link['title'] + '/' + str(picture) + '.jpg', 'wb')
                    file.write(response.content)
                    file.close()
            file = open(dir + '/' + link['title'] + '/Done.txt', 'w+')
            file.close()
        if len(os.listdir(dir)) != 0:
            file = open(dir + '/Done.txt', 'w+')
            file.close()
            f = open('DoneBooks.txt', 'a+')
            f.write(target + '\n')
            f.close()
        else:
            os.rmdir(dir)
            f = open('DoneBooks.txt', 'a+')
            f.write(target + '\n')
            f.close()
    except Exception as e:
        print(e)


page = webdriver.Chrome()
page.get('http://readallcomics.com/')
targets = []
while True:
    inputTarget = input('Comic Book : ')
    if inputTarget == '':
        break
    targets.append(inputTarget)
page.close()

threads = []
for targ in targets:
    threads.append(Thread(target=run, args=(targ,)))
    threads[len(threads)-1].start()

for thread in threads:
    while thread.is_alive():
        pass

f = open('DoneBooks.txt', 'r')
booksDone = f.readlines()
f.close()
os.remove('DoneBooks.txt')
f = open('bookList.txt', 'r')
books = f.readlines()
f.close()
for done in booksDone:
    if done in books:
        books.remove(done)
f = open('bookList.txt', 'w+')
for book in books:
    f.write(book)
f.close()





