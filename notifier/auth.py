import os
import json
import webbrowser
from functools import cmp_to_key

import requests
from bs4 import BeautifulSoup

from notifier.public.constant import reply, requestLogin, header
from notifier.loggingManager import logger
from notifier.notification import toast

with open('./public/constant.json', encoding="UTF-8") as jsonFile:
    data = json.load(jsonFile)
    url = data["URL"]
    filePath = data["filePath"]

def saveJson(boardName, data):
    boardFilePath = filePath["boardPath"] + f'{boardName}.json'
    with open(boardFilePath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def loadJson(boardName):
    boardFilePath = filePath["boardPath"] + f'{boardName}.json'
    with open(boardFilePath, 'r', encoding='utf-8') as f:
        return json.load(f)


def tryLogin(userID, userPW):
    with requests.Session() as session:
        loginReply = session.post(url["loginUrl"],
                                  headers=header(url["baseUrl"], url["loginUrl"]),
                                  data=requestLogin(userID, userPW))
        for state in reply:
            if loginReply == reply[state]:
                return state
        logger.error(f'Unexpected reply | {loginReply.text}')


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
                print('INITIAL TITLE', board_data_title, post_data[number])

                if post_data[number] != '공지':
                    post_data[number] = int(post_data[number])  # IMPORTANT

                if post_data[number] == '공지':
                    board_data['important'].append(post_data[title])
                    new_post.append(post_data)
                else:
                    board_data['verified_number'] = post_data[number]
                    new_post.append(post_data)
                    verify = True
                    break

    print(board_data)
    saveJson(board_name, board_data)
