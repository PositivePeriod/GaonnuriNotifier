import os
import json
import webbrowser

import requests
from bs4 import BeautifulSoup

from constant_string import login_url, boards_info, board_file_path, base_url, boards_url
from notification import toast

header_login_success = '''<?xml version="1.0" encoding="UTF-8"?><response><error>0</error>
<message>success</message><message_type></message_type></response>'''

login_data = lambda user_id, user_pw: f'''<?xml version="1.0" encoding="utf-8" ?><methodCall><params>
<user_id>{user_id}</user_id><password>{user_pw}</password><act>procMemberLogin</act></params></methodCall>'''

new_important = lambda board_name: f'{board_name}에 새로 올라온 공지'
new_normal = lambda board_name: f'{board_name}에 새로 올라온 글'


def open_url(url):
    return lambda: webbrowser.open(url, new=2)


def header(base_url_, full_url):
    return {'Host': base_url_[8:], 'Referer': full_url, 'Cache-Control': 'max-age=0'}


def get_data(user_id, user_pw, urls):
    with requests.Session() as session:
        request_login = session.post(login_url, headers=header(base_url, login_url), data=login_data(user_id, user_pw))

        if request_login.text != header_login_success:
            return False

        for board_name in urls.keys():  # each board
            page_number = 0
            number = boards_info[board_name].index('번호')
            title = boards_info[board_name].index('제목')

            if not os.path.isfile(board_file_path + f'{board_name}.json'):
                initial_board(session, board_name)
            load_data = json_board_data('load', board_name)

            verified_number = load_data['verified_number']
            verify = False
            board_data = {'verified_number': 0, 'important': [], 'normal': []}
            board_data_title = []
            while not verify:  # each page
                page_number += 1
                request_board = session.get(urls[board_name] + str(page_number), headers=header(base_url, base_url))
                soup = BeautifulSoup(request_board.text, features="html.parser")
                for post in soup.find_all("td", class_="no"):
                    post_data = [info.text.strip() for info in [post] + post.find_next_siblings("td")]
                    try:
                        # erase the number of comments
                        post_data[title] = post_data[title][:post_data[title].index('\n')]
                    except ValueError:
                        pass  # the post without comments
                    finally:
                        post_data = [' '.join(info.split()) for info in post_data]
                        post_data.append(post.find_next_siblings("td")[title - 1].a['href'])
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
            for post in board_data['normal']:
                if post[number] > verified_number:
                    new_post.append(post)
                    new_verified_number = max(post[number], new_verified_number)
            board_data['verified_number'] = new_verified_number
            for post in board_data['important']:
                if post[title] not in load_data['important']:
                    new_post.append(post)
            del board_data['normal']
            board_data['important'] = [post[title] for post in board_data['important']]
            json_board_data('save', board_name, board_data)
            for post in new_post:
                toast_title = new_important(board_name) if post[title] == '공지' else new_normal(board_name)
                toast_msg = post[title]
                toast(toast_title, toast_msg, open_url(post[-1]))
        return True


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
        request_login = session.post(login_url, headers=header(base_url, login_url), data=login_data(user_id, user_pw))
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
        request_board = session.get(boards_url[board_name] + str(page_number), headers=header(base_url, base_url))
        soup = BeautifulSoup(request_board.text, features="html.parser")
        for post in soup.find_all("td", class_="no"):
            post_data = [info.text.strip() for info in [post] + post.find_next_siblings("td")]
            try:
                # erase the number of comments
                post_data[title] = post_data[title][:post_data[title].index('\n')]
            except ValueError:
                pass  # the post without comments
            finally:
                post_data = [' '.join(info.split()) for info in post_data]
            if post_data[title] not in board_data_title:
                board_data_title.append(post_data[title])
                if post_data[number] == '공지':
                    board_data['important'].append(post_data[title])
                    new_post.append(post_data)
                else:
                    board_data['verified_number'] = post_data[number]
                    new_post.append(post_data)
                    verify = True
                    break

    json_board_data('save', board_name, board_data)
