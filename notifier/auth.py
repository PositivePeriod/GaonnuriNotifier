import os
import json
import requests

from public.constant import reply, requestLogin, header
from loggingManager import logger
from notification import toast

from bs4 import BeautifulSoup

with open('./notifier/public/constant.json', encoding="UTF-8") as jsonFile:
    data = json.load(jsonFile)
    url = data["URL"]
    filePath = data["filePath"]


def saveJson(boardName, data):
    boardFilePath = filePath["boardPath"] + f'{boardName}.json'
    with open(boardFilePath, 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False)


def loadJson(boardName):
    boardFilePath = filePath["boardPath"] + f'{boardName}.json'
    with open(boardFilePath, 'r', encoding='UTF-8') as f:
        return json.load(f)


def tryLogin(userID, userPW):
    with requests.Session() as session:
        loginUrl = url["loginUrl"]
        loginHeaders = header(url["baseUrl"], url["loginUrl"])
        loginData = requestLogin(userID, userPW)
        try:
            loginReply = session.post(
                loginUrl, headers=loginHeaders, data=loginData)
        except requests.exceptions.ConnectionError as e:
            logger.critical(f"Connection error - {e}")
            return "internetError"
        except Exception as e:
            logger.critical(f"Unexpected error - {e}")
            return "errorOccur"
    for state in reply:
        if loginReply.text == reply[state]:
            return state

    logger.error(f'Unexpected reply - {loginReply.text}')
    return "errorOccur"