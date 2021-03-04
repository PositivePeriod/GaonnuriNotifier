import os
import json
import webbrowser
from functools import cmp_to_key

import requests
from bs4 import BeautifulSoup

from constant_string import login_url, boards_info, board_file_path, base_url, boards_url
from notification import toast

header_login_success = \
    '''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>0</error>
<message>success</message>
<message_type></message_type>
</response>'''


def login_data(user_id, user_pw): return f'''<?xml version="1.0" encoding="utf-8" ?><methodCall><params>
<user_id>{user_id}</user_id><password>{user_pw}</password><act>procMemberLogin</act></params></methodCall>'''


def new_important(board_name): return f'{board_name}에 새로 올라온 공지'
def new_normal(board_name): return f'{board_name}에 새로 올라온 글'


def open_url(url):
    return lambda: webbrowser.open(url, new=2)


def header(base_url_, full_url):
    return {'Host': base_url_[8:], 'Referer': full_url, 'Cache-Control': 'max-age=0'}


def get_data(user_id, user_pw, urls):
    with requests.Session() as session:
        request_login = session.post(login_url, headers=header(
            base_url, login_url), data=login_data(user_id, user_pw))

        if request_login.text != header_login_success:
            print('get_data', request_login.text)
            return False

        for board_name in urls.keys():  # each board
            number = boards_info[board_name].index('번호')
            title = boards_info[board_name].index('제목')

            if not os.path.isfile(board_file_path + f'{board_name}.json'):
                initial_board(session, board_name)
            load_data = json_board_data('load', board_name)

            if board_name == '학운위 공지사항':
                print('LOAD DATA', load_data)

            verified_number = int(load_data['verified_number'])
            verify = False
            board_data = {'verified_number': 0, 'important': [], 'normal': []}
            board_data_title = []
            page_number = 0
            while not verify:  # each page
                page_number += 1
                request_board = session.get(
                    urls[board_name] + str(page_number), headers=header(base_url, base_url))
                soup = BeautifulSoup(request_board.text,
                                     features="html.parser")

                # 33333333333333
                if board_name == '학운위 공지사항':
                    with open('./학운위 공지사항.html', 'w', encoding='utf8') as f:
                        f.write(request_board.text)
                # 333333333333333333

                for post in soup.find_all("td", class_="no"):
                    post_data = [info.text.strip()
                                 for info in [post] + post.find_next_siblings("td")]

                    if board_name == '학운위 공지사항':
                        print('CRAWL', post_data) # CRAWL

                    try:
                        # erase the number of comments
                        post_data[title] = post_data[title][:post_data[title].index(
                            '\n')]  # TODO how about tab; \t?
                    except ValueError:
                        pass  # the post without comments
                    finally:
                        post_data = [' '.join(info.split())
                                     for info in post_data]
                        post_data.append(post.find_next_siblings("td")[
                                         title - 1].a['href'])

                    if post_data[number] != '공지':
                        post_data[number] = int(post_data[number]) # IMPORTANT

                    if post_data[number] != '공지' and post_data[number] <= verified_number:
                        verify = True
                    if post_data[title] not in board_data_title:
                        board_data_title.append(post_data[title])
                        if post_data[number] == '공지':
                            board_data['important'].append(post_data)
                        else:
                            board_data['normal'].append(post_data)

            new_post = []
            new_verified_number = verified_number
            print('INIT NUMBER', new_verified_number, verified_number)
            for post in board_data['normal']:
                if post[number] > verified_number:
                    new_post.append(post)

                    if board_name == '학운위 공지사항':
                        print('NEW POST ||', new_verified_number, verified_number, post[number], type(post[number]), type(verified_number), type(new_verified_number))
                    new_verified_number = max(post[number], new_verified_number)


            board_data['verified_number'] = new_verified_number

            for post in board_data['important']:
                if post[title] not in load_data['important']:
                    new_post.append(post)
            del board_data['normal']
            board_data['important'] = [post[title]
                                       for post in board_data['important']]
            json_board_data('save', board_name, board_data)

            if board_name == '학운위 공지사항':
                print('UPDATED NEW POST', new_post)

            new_post.sort(key=cmp_to_key(cmp))
                
            for post in new_post:
                toast_title = new_important(
                    board_name) if post[number] == '공지' else new_normal(board_name)
                toast_msg = post[title]
                toast(toast_title, toast_msg, open_url(post[-1]))
        return True

def cmp(x, y):
    if x == '공지':
        return -1
    elif y == '공지':
        return 1
    elif x > y:
        return 1
    else:
        return -1

def json_board_data(option, board_name, data=None):
    board_data_path = board_file_path + f'{board_name}.json'
    assert (option == 'save') or (option == 'load')
    if option == 'save':
        with open(board_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    elif option == 'load':
        with open(board_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def login_success(user_id, user_pw):
    with requests.Session() as session:
        request_login = session.post(login_url, headers=header(
            base_url, login_url), data=login_data(user_id, user_pw))
        print('ERROR HANLDING l', request_login.text)
        return request_login.text == header_login_success


def initial_board(session, board_name):
    number = boards_info[board_name].index('번호')
    title = boards_info[board_name].index('제목')

    board_data = {'verified_number': 0, 'important': []}
    board_data_title = []
    new_post = []

    verify = False
    page_number = 0
    while not verify:
        page_number += 1
        request_board = session.get(
            boards_url[board_name] + str(page_number), headers=header(base_url, base_url))
        soup = BeautifulSoup(request_board.text, features="html.parser")
        for post in soup.find_all("td", class_="no"):
            post_data = [info.text.strip()
                         for info in [post] + post.find_next_siblings("td")]
            try:
                # erase the number of comments
                post_data[title] = post_data[title][:post_data[title].index(
                    '\n')]
            except ValueError:
                # the post without comments
                pass
            finally:
                post_data = [' '.join(info.split()) for info in post_data]
            if post_data[title] not in board_data_title:
                board_data_title.append(post_data[title])
                print('INITIAL TITLE', board_data_title, post_data[number]) ##

                if post_data[number] != '공지':
                    post_data[number] = int(post_data[number]) # IMPORTANT

                if post_data[number] == '공지':
                    board_data['important'].append(post_data[title])
                    new_post.append(post_data)
                else:
                    board_data['verified_number'] = post_data[number]
                    new_post.append(post_data)
                    verify = True
                    break

    print(board_data)
    json_board_data('save', board_name, board_data)


# <?xml version="1.0" encoding="UTF-8"?>
# <response>
# <error>-1</error>
# <message>잘못된 비밀번호입니다.</message>
# <message_type></message_type>
# </response>

# <?xml version="1.0" encoding="UTF-8"?>
# <response>
# <error>-1</error>
# <message>존재하지 않는 회원 아이디입니다.</message>
# <message_type></message_type>
# </response>

# <?xml version="1.0" encoding="UTF-8"?>
# <response>
# <error>0</error>
# <message>success</message>
# <message_type></message_type>
# </response>
