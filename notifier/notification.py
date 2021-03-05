import json
from win10toast import ToastNotifier
import webbrowser

from loggingManager import logger

with open('./notifier/public/constant.json', encoding="UTF-8") as jsonFile:
    iconPath = json.load(jsonFile)["filePath"]["iconPath"]


def toast(title, msg, func=None, duration=5):
    logger.info(f'Toast - {title} - {msg}')
    ToastNotifier().show_toast(title=title, msg=msg,
                               icon_path=iconPath,
                               duration=duration,
                               callback_on_click=func)


def multipleToast(posts, toastTitle):
    for post in posts:
        toastMSG = post.title
        toast(toastTitle, toastMSG, openUrl(post.url))


def openUrl(url):
    return lambda: webbrowser.open(url, new=2)
