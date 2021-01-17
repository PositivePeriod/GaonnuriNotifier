from constant_string import icon_file_path
from win10toast import ToastNotifier


def toast(title, msg, func=None, duration=5):
    if func is None:
        ToastNotifier().show_toast(title=title, msg=msg, icon_path=icon_file_path, duration=duration)
    else:
        ToastNotifier().show_toast(title=title, msg=msg, icon_path=icon_file_path, duration=duration,
                                   callback_on_click=func)
