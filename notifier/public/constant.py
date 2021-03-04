reply = dict()

reply["success"] =
'''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>0</error>
<message>success</message>
<message_type></message_type>
</response>'''

reply["wrongID"] =
'''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>-1</error>
<message>존재하지 않는 회원 아이디입니다.</message>
<message_type></message_type>
</response>'''

reply["wrongPW"] =
'''<?xml version="1.0" encoding="UTF-8"?>
<response>
<error>-1</error>
<message>잘못된 비밀번호입니다.</message>
<message_type></message_type>
</response>'''

requestLogin = lambda user_id, user_pw:
f'''<?xml version="1.0" encoding="utf-8" ?>
<methodCall><params>
<user_id>{user_id}</user_id>
<password>{user_pw}</password>
<act>procMemberLogin</act>
</params></methodCall>'''


def welcome(language, userName):
    if language == 'ko':
        return f'{user_name}님 환영해요'
    if language == 'en':
        return f'Welcome {user_name}'
    else:
        logger.warning(f'Impossible language | {language}')
        return f'{user_name}'


def isNewNotice(language, board_name):
    if language == 'ko':
        return f'{board_name}에 새로운 공지가 올라왔어요'
    if language == 'en':
        return f'New notice from {board_name}'
    else:
        logger.warning(f'Impossible language | {language}')
        return f'{board_name}'


def isNewNotNotice(language, board_name):
        if language == 'ko':
        return f'{board_name}에 새로운 글이 올라왔어요'
    if language == 'en':
        return f'New post from {board_name}'
    else:
        logger.warning(f'Impossible language | {language}')
        return f'{board_name}'

def header(hostUrl, refererUrl):
    return {'Host': hostUrl[8:], 'Referer': refererUrl, 'Cache-Control': 'max-age=0'}
