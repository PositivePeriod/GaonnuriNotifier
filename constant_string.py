from tkinter import Tk, StringVar, ttk, Button


class Translator:
    def __init__(self):
        self.language = None
        self.window = Tk()
        self.window.title('Gaonnuri Notifier')
        self.window.geometry(f'300x50+{self.window.winfo_screenwidth()//2-150}+{self.window.winfo_screenheight()//2-75}')
        self.window.resizable(False, False)
        self.window.iconbitmap('./data/icon.ico')
        string = StringVar()
        combobox = ttk.Combobox(textvariable=string, width=20, state='readonly')
        combobox['value'] = ('한글', 'English')
        combobox.current(0)

        def click():
            self.language = string.get()
        click_button = Button(text='Choose', command=click)
        combobox.pack(fill='both')
        click_button.pack()
        self.window.mainloop()
        print(self.language)


start = "가온누리 알리미 서비스가 시작됩니다 :)"
login_failure = "아이디나 비밀번호가 틀렸습니다 :("
write_again = "다시 입력해 주세요"


def welcome(user_name):
    return f'{user_name}님 환영합니다'


header_login_success = '''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>0</error>
<message>success</message>
<message_type></message_type>
</response>'''