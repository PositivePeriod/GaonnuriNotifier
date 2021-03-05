import os
import time
from tkinter import Tk, simpledialog
import sys
import json

from loggingManager import logger
from auth import tryLogin
from notification import toast
from public.constant import welcome
from crawl import updateData

with open('./notifier/public/constant.json', encoding="UTF-8") as jsonFile:
    constantData = json.load(jsonFile)
    filePath = constantData["filePath"]
    iconPath = filePath["iconPath"]
    basePath = filePath["basePath"]
    boardPath = filePath["boardPath"]
    infoPath = filePath["infoPath"]
    wholeSentence = constantData["sentence"]


with open('./notifier/public/info.json', encoding="UTF-8") as jsonFile:
    infoData = json.load(jsonFile)
    programName = infoData["name"]


class GaonnuriNotifier:
    def __init__(self, language):
        self.language = language
        self.sentence = wholeSentence[language]

    def run(self, updateCycle=300):
        if not os.path.isfile(iconPath):
            toast(self.sentence["noIcon"],
                  self.sentence["wishNoProblem"], duration=1)
        if not os.path.isdir(basePath):
            os.mkdir(basePath)
        if not os.path.isdir(boardPath):
            os.mkdir(boardPath)

        userID, userPW = self.getInfo()
        toast(self.sentence["start"], welcome(
            self.language, userID), duration=1)

        while True:
            state = updateData(userID, userPW, self.language)  # TODO
            if state == "internetError":
                toast(self.sentence["errorOccur"],
                      self.sentence["internetError"], duration=1)
                self.stop()
            elif state == "errorOccur":
                toast(self.sentence["errorOccur"],
                      self.sentence["close"], duration=1)
                self.stop()
            elif state != "success":  # TODO login error?
                toast(self.sentence["errorOccur"],
                      self.sentence["close"], duration=1)
                self.stop()

            logger.info(f'Wait for updating after {updateCycle}s')
            time.sleep(updateCycle)

    def getInfo(self, reset=False):
        if os.path.isfile(infoPath) and not reset:
            with open(infoPath, 'r') as f:
                userID = f.readline()[:-1]  # reduce \n
                userPW = f.readline()
        else:
            userID, userPW = self.register()
            with open(path, 'w') as f:
                f.write(userID + '\n' + userPW)
        return userID, userPW

    def register(self):
        window = Tk()
        window.withdraw()
        askID, askPW = None, None
        state = ''
        while not state == 'success':
            askID = simpledialog.askstring(
                programName, self.sentence["enterID"])
            askPW = simpledialog.askstring(
                programName, self.sentence["enterPW"])
            if askID is None and askPW is None:
                self.stop()
            state = tryLogin(askID, askPW)
            if state == "internetError":
                toast(self.sentence["errorOccur"],
                      self.sentence["internetError"], duration=1)
                self.stop()
            elif state == "errorOccur":
                toast(self.sentence["errorOccur"],
                      self.sentence["close"], duration=1)
                self.stop()
            elif not state == 'success':
                toast(self.sentence[state],
                      self.sentence["writeAgain"], duration=1)
        window.destroy()
        return askID, askPW

    def stop(self):
        toast(self.sentence["close"], self.sentence["seeYouLater"], duration=1)
        logger.info('Stop the program during register')
        sys.exit()


if __name__ == '__main__':
    notifier = GaonnuriNotifier('ko')
    notifier.run()

    # language setting
    # ICON + NAME CHANGE
