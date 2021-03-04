import json
from win10toast import ToastNotifier

with open('./public/constant.json', encoding="UTF-8") as jsonFile:
    iconPath = json.load(jsonFile)["filePath"]["iconPath"]


def toast(title, msg, func=None, duration=5):
    logger.info(f'Toast {title} {msg}')

    ToastNotifier().show_toast(title=title, msg=msg,
                               icon_path=iconPath,
                               duration=duration,
                               callback_on_click=func)
