import os
import time
import json
import webbrowser
from tkinter import Tk, simpledialog

from win10toast import ToastNotifier
import requests
from bs4 import BeautifulSoup

import constant_string


def toast(title, msg, func=None, duration=5):
    if func is None:
        ToastNotifier().show_toast(title=title, msg=msg, icon_path=icon_file_path, duration=duration)
    else:
        ToastNotifier().show_toast(title=title, msg=msg, icon_path=icon_file_path, duration=duration,
                                   callback_on_click=func)


def open_url(url):
    return lambda: webbrowser.open(url, new=2)


def header(base_url_, full_url):
    return {
        'Host': base_url_[8:],
        'Referer': full_url,
        'Cache-Control': 'max-age=0'}


def login_data(user_id, user_pw):
    return f'''<?xml version="1.0" encoding="utf-8" ?>
<methodCall>
<params>
<user_id>{user_id}</user_id>
<password>{user_pw}</password>
<act>procMemberLogin</act>
</params>
</methodCall>'''


def get_data(user_id, user_pw, urls):
    with requests.Session() as session:
        request_login = session.post(login_url, headers=header(base_url, login_url), data=login_data(user_id, user_pw))
        if request_login.text != constant_string.header_login_success:
            toast(constant_string.login_failure, constant_string.write_again)
            return None
        for board_name in urls.keys():
            page_number = 0
            number = boards_info[board_name].index('번호')
            title = boards_info[board_name].index('제목')

            if not os.path.isfile(board_file_path+f'{board_name}.json'):
                initial_board(session, board_name)

            load_data = json_board_data('load', board_name)
            verified_number = load_data['verified_number']

            verify = False
            board_data = {'verified_number': 0, 'important': [], 'normal': []}
            board_data_title = []
            while not verify:
                print(board_name, page_number)
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
                        post_data.append(post.find_next_siblings("td")[title-1].a['href'])
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
                toast_title = f'{board_name}에 새로 올라온 공지' if post[title] == '공지' else f'{board_name}에 새로 올라온 글'
                toast_msg = post[title]
                toast(toast_title, toast_msg, open_url(post[-1]))
            print('finish', board_name)


def json_board_data(option, board_name, data=None):
    board_data_path = board_file_path+f'{board_name}.json'
    if option == 'save':
        with open(board_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    elif option == 'load':
        with open(board_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def get_login_info(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            user_id = f.readline()[:-1]
            user_pw = f.readline()
    else:
        login = False
        window = Tk()
        window.withdraw()
        user_id = None
        user_pw = None
        while not login:
            user_id = simpledialog.askstring('Gaonnuri Notifier', 'Enter your Gaonnuri ID')
            user_pw = simpledialog.askstring('Gaonnuri Notifier', 'Enter your Gaonnuri PW')
            # user_id = input('Write your Gaoonuri ID : ')
            # user_pw = input('Write your Gaonnuri PW : ')
            login = login_success(user_id, user_pw)
        window.destroy()
        with open(path, 'w') as f:
            f.write(user_id + '\n' + user_pw)
    toast(constant_string.start, f'{user_id}님 환영합니다', duration=1)
    return user_id, user_pw


def login_success(user_id, user_pw):
    with requests.Session() as session:
        request_login = session.post(login_url, headers=header(base_url, login_url),
                                     data=login_data(user_id, user_pw))
        if request_login.text == constant_string.header_login_success:
            return True
        else:
            toast(constant_string.login_failure, constant_string.write_again, duration=1)
            return False


def initial_board(session, board_name):
    print('Initial', board_name)
    page_number = 0
    number = boards_info[board_name].index('번호')
    title = boards_info[board_name].index('제목')

    verify = False
    new_post = []
    board_data = {'verified_number': 0, 'important': []}
    board_data_title = []
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


if __name__ == '__main__':
    # TODO gui asking / login_info & change board & time(10, 30, 1h)
    # TODO option - English / Korea - notice name

    info_file_path = './data/info.txt'
    board_file_path = './data/board/'
    icon_file_path = './data/icon.ico'

    base_url = 'https://gaonnuri.ksain.net'
    main_url = f'{base_url}/xe'
    login_url = f'{main_url}/login'
    boards = {'공지사항 게시판': 'board_notice',
              '임시 게시판': 'board_LoAj77',
              '규정 게시판': 'board_KbST22',
              '자유 게시판': 'board_free',
              '분실물 게시판': 'board_lostfound',
              '선발 공모 게시판': 'board_select',
              '학생회 말말말': 'board_jMJE99',
              '입시 정보 게시판': 'board_entrance',
              '수리 요청 게시판': 'board_repair'}

    boards_info = {'공지사항 게시판': ('번호', '분류', '제목', '날짜', '조회수'),
                   '임시 게시판': ('번호', '제목', '글쓴이', '날짜', '조회수'),
                   '규정 게시판': ('번호', '제목', '글쓴이', '날짜', '조회수'),
                   '자유 게시판': ('번호', '제목', '아이디', '글쓴이', '날짜', '조회수'),
                   '분실물 게시판': ('번호', '분류', '제목', '글쓴이', '날짜', '조회수'),
                   '선발 공모 게시판': ('번호', '제목', '글쓴이', '날짜', '마감기한', '조회수'),
                   '학생회 말말말': ('번호', '분류', '제목', '날짜', '조회수'),
                   '입시 정보 게시판': ('번호', '제목', '날짜'),
                   '수리 요청 게시판': ('번호', '분류', '제목', '글쓴이', '날짜', '조회수')}

    boards_url = dict(zip(boards.keys(), [f'{main_url}/index.php?mid={board}&page=' for board in boards.values()]))

    if not os.path.isdir('./data'):
        os.mkdir('./data')
    if not os.path.isdir('./data/board'):
        os.mkdir('./data/board')
    info_id, info_pw = get_login_info(info_file_path)
    while True:
        get_data(info_id, info_pw, boards_url)
        print('Time to sleep')
        time.sleep(600)
