import os
import time
from tkinter import Tk, simpledialog

from constant_string import file_path, icon_file_path, info_file_path, board_file_path
from constant_string import program_name, boards_url
from auth import get_data, login_success
from notification import toast

enter_id = "가온누리 아이디를 입력하세요"
enter_pw = "가온누리 비밀번호를 입력하세요"
start = "가온누리 알리미 서비스가 시작됩니다 :)"
login_failure = "아이디나 비밀번호가 틀렸습니다 :("
write_again = "다시 입력해 주세요"

no_icon = "아이콘을 찾을 수 없습니다"
plz_no_problem = "큰 문제가 없길 바라봅니다 :)"


def welcome(user_name):
    return f'{user_name}님 환영합니다'


def get_login_info(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            user_id = f.readline()[:-1]
            user_pw = f.readline()
    else:
        user_id, user_pw = ask_login_info()
        with open(path, 'w') as f:
            f.write(user_id + '\n' + user_pw)
    return user_id, user_pw


def ask_login_info():
    login = False
    user_id = None
    user_pw = None
    window = Tk()
    window.withdraw()
    while not login:
        user_id = simpledialog.askstring(program_name, enter_id)
        user_pw = simpledialog.askstring(program_name, enter_pw)
        if user_id is None and user_pw == None:
            import sys
            sys.exit('Stop the program')
        login = login_success(user_id, user_pw)
        if not login:
            toast(login_failure, write_again, duration=1)
    window.destroy()
    return user_id, user_pw


if __name__ == '__main__':
    if not os.path.isfile(icon_file_path):
        toast(no_icon, plz_no_problem, duration=1)
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    if not os.path.isdir(board_file_path):
        os.mkdir(board_file_path)

    info_id, info_pw = get_login_info(info_file_path)
    toast(start, welcome(info_id), duration=1)
    while True:
        success = get_data(info_id, info_pw, boards_url)
        if not success:
            toast(login_failure, write_again)
            break
        sleep_time = 300
        print(f'Sleep for {sleep_time}s')
        time.sleep(sleep_time)

# 글 읽는 순서가 거꾸로임  