<!-- ABOUT THE PROJECT -->
## About The Project

Gaonnuri Notifier

### Requirements

* [Python](https://www.python.org/) : 3.8.5
* [requests](https://pypi.org/project/requests/) : 2.24.0
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) : 4.9.1
* [win10toast](https://github.com/Charnelx/Windows-10-Toast-Notifications) which is forked by Charnelx

win10toast is inevitably included in the code as [win10toast.py](./win10toast.py) since it cannot be downloaded easily with pypi.

<!-- GETTING STARTED -->
### Getting Started

Caution : 본 repository는 실제 사용보다는 연구 목적으로 KSA 정보부의 허락을 받지 않고 사용하여 일어난 모든 결과에 대해서 개발자는 어떠한 책임도 지지 않습니다

1. Make venv  
`python -m venv venv`

2. Install libaries  
`pip install -r requirements.txt`

3. Start  
`python notifier/main.py`

## Tip
Use ~ + Left Shift + Left Ctrl to start venv in vsc  
Use [Shift+Alt+F](https://code.visualstudio.com/docs/languages/json) for JSON Formatting in vsc  
Use autopepe8 formatter by `pip install autopep8`

<!-- ROADMAP -->
## Roadmap

* Make GUI | Language option / Ask ID & PW / Select sleep time for each board
* If user_id or user_pw contains \n, it might cause error
* auth.py does not concerned with authentication
* More compact code
* Thread between crawling and alert


<!-- LICENSE -->
## License
I'm not sure for external libraries that I used
However, my code is MIT
