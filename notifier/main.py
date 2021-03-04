import os
import time
from tkinter import Tk, simpledialog
import sys

from notifier.loggingManager import logger
from notifier.auth import get_data, tryLogin
from notifier.notification import toast
from notifier.public.constant import welcome

with open('./public/constant.json', encoding="UTF-8") as jsonFile:
    data = json.load(jsonFile)
    sentence = data["sentence"]
    filePath = data["filePath"]

with open('./public/info.json', encoding="UTF-8") as jsonFile:
    programName = json.load(jsonFile)["name"]


def register(sentence):
    window = Tk()
    window.withdraw()
    askID, askPW = None, None
    state = ''
    while not state == 'success':
        askID = simpledialog.askstring(programName, sentence["enterID"])
        askPW = simpledialog.askstring(programName, sentence["enterPW"])
        if askID is None and askPW is None:
            toast(sentence["close"], sentence["seeYouLater"], duration=1)
            logger.info('Stop the program during register')
            sys.exit()

        state = tryLogin(askID, askPW)
        if not state == 'success':
            toast(sentence[state], sentence["writeAgain"], duration=1)
    window.destroy()
    return askID, askPW


def run(language, updateCycle=300):
    sentence = sentence[language]
    iconPath = filePath["iconPath"]
    basePath = filePath["basePath"]
    boardPath = filePath["boardPath"]
    infoPath = filePath["infoPath"]

    if not os.path.isfile(iconPath):
        toast(sentence["noIcon"], sentence["wishNoProblem"], duration=1)
    if not os.path.isdir(basePath):
        os.mkdir(basePath)
    if not os.path.isdir(boardPath):
        os.mkdir(boardPath)

    if os.path.isfile(infoPath):
        with open(infoPath, 'r') as f:
            userID = f.readline()[:-1]  # reduce \n
            userPW = f.readline()
    else:
        userID, userPW = register(sentence)
        with open(path, 'w') as f:
            f.write(userID + '\n' + userPW)

    toast(sentence["start"], welcome(userID), duration=1)
    while True:
        state = get_data(userID, userPW, boards_url)
        if not state == 'success':
            toast(sentence[state], sentence["writeAgain"], duration=1)
        if state != "success":
            toast(sentence["wrongID"], sentence["writeAgain"])
            break

        logger.info(f'Wait for updating after {updateCycle}s')
        time.sleep(updateCycle)


if __name__ == '__main__':
    language = 'ko'
    run(language)
    # TODO
    # boards_url = dict(zip(boards.keys(), [f "{main_url}/index.php?mid={board}&page="for board in boards.values()]))

    # language setting
    # ICON + NAME CHANGE
