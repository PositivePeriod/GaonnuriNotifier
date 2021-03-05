import json
import os
import webbrowser

from public.constant import header, requestLogin, reply, isNewNotice, isNewNotNotice
from notification import toast, multipleToast
from auth import loadJson, saveJson
from post import Post
from loggingManager import logger

import requests
from bs4 import BeautifulSoup

with open('./notifier/public/constant.json', encoding="UTF-8") as jsonFile:
    data = json.load(jsonFile)
    url = data["URL"]
    filePath = data["filePath"]
    board = data["board"]


def updateData(userID, userPW, language):
    # Use function in auth.py; tryToLogin
    with requests.Session() as session:
        lgUrl = url["loginUrl"]
        lgHeaders = header(url["baseUrl"], url["loginUrl"])
        lgData = requestLogin(userID, userPW)
        try:
            loginReply = session.post(lgUrl, headers=lgHeaders, data=lgData)
        except requests.exceptions.ConnectionError as e:
            logger.critical(f"Connection error - {e}")
            return "internetError"
        except Exception as e:
            logger.critical(f"Unexpected error - {e}")
            return "errorOccur"

        for state in reply:
            if loginReply.text == reply[state] and state != "success":
                return "state"

        for boardName in board["name"]:  # each board
            boardFilePath = filePath["boardPath"] + f'{boardName}.json'
            if not os.path.isfile(boardFilePath):
                state = initialData(session, boardName)
                if state != "success":
                    return state
                continue

            loadData = loadJson(boardName)
            confirmIndex = int(loadData['confirmIndex'])
            noticeTitle = loadData['noticeTitle']

            newConfirmIndex = confirmIndex
            newNotice = []
            newNotNotice = []
            newNoticeTitle = []

            pageNumber = 0
            verify = False
            while not verify:
                if pageNumber > 1:
                    logger.warning(f"Crawl {pageNumber} page from {boardName}")
                pageNumber += 1
                requestUrl = f"{url['mainUrl']}/index.php?mid={board['name'][boardName]}&page={pageNumber}"
                requestHeader = header(url["baseUrl"], url["baseUrl"])
                try:
                    requestBoard = session.get(
                        requestUrl, headers=requestHeader)
                except requests.exceptions.ConnectionError as e:
                    logger.critical(f"Connection error - {e}")
                    return "internetError"
                except Exception as e:
                    logger.critical(f"Unexpected error - {e}")
                    return "errorOccur"

                soup = BeautifulSoup(requestBoard.text, "html.parser")

                for tdElement in soup.find_all("td", class_="no"):
                    element = tdElement.find_next_siblings("td")
                    postData = [info.text.strip()
                                for info in [tdElement] + element]
                    title = board["itemOrder"][boardName].index('제목')
                    try:
                        # The post with comments; TODO how about tab; \t?
                        index = postData[title].index('\n')
                        postData[title] = postData[title][:index]
                    except ValueError:
                        # The post without comments
                        pass
                    postData = [' '.join(info.split()) for info in postData]

                    postUrl = element[title - 1].a['href']

                    post = Post(boardName, postData, postUrl)

                    if not post.isNotice and post.index >= confirmIndex:
                        verify = True
                        if post.index > confirmIndex:
                            newNotNotice.append(post)
                            newConfirmIndex = max(post.index, newConfirmIndex)
                    elif post.isNotice:
                        newNoticeTitle.append(post.title)
                        if post.title not in noticeTitle:
                            newNotice.append(post)

            boardData = {'confirmIndex': newConfirmIndex,
                         'noticeTitle': newNoticeTitle}
            saveJson(boardName, boardData)

            multipleToast(newNotice, isNewNotice(language, boardName))
            newNotNotice.sort(key=lambda post: post.index)
            multipleToast(newNotNotice, isNewNotNotice(language, boardName))
    return "success"


def initialData(session, boardName):
    confirmIndex = 0
    noticeTitle = []

    verify = False
    pageNumber = 0
    while not verify:
        pageNumber += 1
        requestUrl = f"{url['mainUrl']}/index.php?mid={board['name'][boardName]}&page={pageNumber}"
        requestHeaders = header(url["baseUrl"], url["baseUrl"])
        try:
            requestBoard = session.get(requestUrl, headers=requestHeaders)
        except requests.exceptions.ConnectionError as e:
            logger.critical(f"Connection error - {e}")
            return "internetError"
        except Exception as e:
            logger.critical(f"Unexpected error - {e}")
            return "errorOccur"
        soup = BeautifulSoup(requestBoard.text, "html.parser")

        for tdElement in soup.find_all("td", class_="no"):
            element = tdElement.find_next_siblings("td")
            postData = [info.text.strip()
                        for info in [tdElement] + element]

            title = board["itemOrder"][boardName].index('제목')
            number = board["itemOrder"][boardName].index('번호')

            try:
                # The post with comments; TODO how about tab; \t?
                index = postData[title].index('\n')
                postData[title] = postData[title][:index]
            except ValueError:
                # The post without comments
                pass

            postData = [' '.join(info.split()) for info in postData]

            if postData[number] == '공지':
                noticeTitle.append(postData[title])
            else:
                confirmIndex = max(int(postData[number]), confirmIndex)
                verify = True
                break

    boardData = {'confirmIndex': confirmIndex,
                 'noticeTitle': noticeTitle}
    saveJson(boardName, boardData)
    return "success"
