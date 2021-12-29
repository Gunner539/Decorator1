from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import os.path


def write_to_file(log_path, log):
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log + '\n')

def logger(path_to_log):

    if path_to_log == '':
        path_to_log = os.getcwd() + '\logs1.txt'

    def decorator(func):

            def do_func(*args, **kwargs):
                start = time.time()
                res = func(*args, **kwargs)

                end = time.time()
                write_to_file(log_path=path_to_log, log=f'{datetime.today().strftime("%m-%d-%y %H:%M:%S")} | Функция {func.__name__} | Время выполнения: {round(end-start, 0)} секунд | Параметры: {args} | Результат: {"; ".join(res)}')
                return res
            return do_func
    return decorator


@logger(path_to_log='')
def get_info(KEYWORDS):

    KeyWords_string = '|'.join(KEYWORDS)
    pattern = re.compile(KeyWords_string, re.IGNORECASE)


    res = requests.get(url='https://habr.com/ru/all/')
    res.raise_for_status()
    soup = BeautifulSoup(res.text, features='html.parser')
    articles = soup.findAll('article')

    my_list = []

    for article in articles:

        article_title = article.find('a', class_='tm-article-snippet__title-link')

        if article_title == None:
            continue

        all_article_text = article_title.text

        article_tags = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
        if len(article_tags) > 0:
            for tag in article_tags:
                all_article_text += '\n' + tag.text

        article_text = article.find_all('p')
        if len(article_text) > 0:
            for paragraph in article_text:
                all_article_text += '\n' + paragraph.text

        href = article.find('a', class_='tm-article-snippet__title-link')

        res = re.findall(pattern, all_article_text)
        if len(res) > 0:
            print(f'{article.find("time")["title"]} - {article_title.text} - https://habr.com{href["href"]}')
            my_list.append(f'https://habr.com{href["href"]}')
        else:
            art_page = requests.get(url='https://habr.com' + href['href'], timeout=5)
            art_page.raise_for_status()
            a_soup = BeautifulSoup(art_page.text, features='html.parser')
            art_block = a_soup.find('article')
            a_res = re.findall(pattern, art_block.text)
            if len(a_res) > 0:
                # print(article_title.text)
                print(f'{article.find("time")["title"]} - {article_title.text} - https://habr.com{href["href"]}')
                my_list.append(f'https://habr.com{href["href"]}')

    return my_list

if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    res = get_info(KEYWORDS)
