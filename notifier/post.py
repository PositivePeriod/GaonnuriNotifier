import json


def getBoardData():
    with open('./notifier/public/constant.json', encoding="UTF-8") as jsonFile:
        boardData = json.load(jsonFile)["board"]
    return boardData


class Post:
    boardData = getBoardData()

    def __init__(self, boardName, postData, url):
        self.boardName = boardName
        self.boardPath = Post.boardData["name"][self.boardName]
        self.url = url
        self.postID = None  # TODO
        self.comments = None  # TODO

        boardItemOrder = Post.boardData["itemOrder"][self.boardName]

        findItem = lambda item: postData[boardItemOrder.index(item)] if item in boardItemOrder else None

        self.index = findItem("번호")
        self.title = findItem("제목")
        self.author = findItem("글쓴이")
        self.date = findItem("날짜")
        self.view = findItem("조회수")

        if self.index == "공지":
            self.isNotice = True
        else:
            self.isNotice = False
            self.index = int(self.index)
        self.category = findItem("분류")
        self.authorID = findItem("아이디")
        self.deadline = findItem("마감기한")
