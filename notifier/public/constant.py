reply = dict()

reply["success"] = \
    '''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>0</error>
<message>success</message>
<message_type></message_type>
</response>'''


reply["wrongID"] = \
    '''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>-1</error>
<message>존재하지 않는 회원 아이디입니다.</message>
<message_type></message_type>
</response>'''

reply["wrongPW"] = \
    '''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>-1</error>
<message>잘못된 비밀번호입니다.</message>
<message_type></message_type>
</response>'''

reply["errorOccur"] = \
    '''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body></html>'''

requestLogin = lambda user_id, user_pw: f'''<?xml version="1.0" encoding="UTF-8" ?>
<methodCall><params>
<user_id>{user_id}</user_id>
<password>{user_pw}</password>
<act>procMemberLogin</act>
</params></methodCall>'''


def welcome(language, userName):
    if language == 'ko':
        return f'{userName}님 환영해요'
    elif language == 'en':
        return f'Welcome {userName}'
    else:
        logger.warning(f'Impossible language - {language}')
        return f'{userName}'


def isNewNotice(language, board_name):
    if language == 'ko':
        return f'{board_name}의 새로운 공지'
    elif language == 'en':
        return f'New notice from {board_name}'
    else:
        logger.warning(f'Impossible language - {language}')
        return f'{board_name}'


def isNewNotNotice(language, board_name):
    if language == 'ko':
        return f'{board_name}의 새로운 글'
    elif language == 'en':
        return f'New post from {board_name}'
    else:
        logger.warning(f'Impossible language - {language}')
        return f'{board_name}'


def header(hostUrl, refererUrl):
    return {'Host': hostUrl[8:], 'Referer': refererUrl, 'Cache-Control': 'max-age=0'}
