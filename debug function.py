import requests
from bs4 import BeautifulSoup

import constant_string

base_url = 'https://gaonnuri.ksain.net'
main_url = f'{base_url}/xe'
login_url = f'{main_url}/login'
boards = {'공지사항 게시판': 'board_notice',
          '임시 게시판': 'board_LoAj77',
          '규정 게시판': 'board_KbST22',
          '자유 게시판': 'board_free',
          '분실물 게시판': 'board_lostfound',
          '선발 공모 게시판': 'board_select',
          '학생회 말말말': 'board_jMJE99',
          '입시 정보 게시판': 'board_entrance',
          '수리 요청 게시판': 'board_repair'}

boards_url = dict(zip(boards.keys(), [f'{main_url}/index.php?mid={board}&page=' for board in boards.values()]))


def header(base_url_, full_url):
    return {
        'Host': base_url_[8:],
        'Referer': full_url,
        'Cache-Control': 'max-age=0'}


def get_board_group(user_id, user_pw, urls):
    with requests.Session() as session:
        request_login = session.post(login_url, headers=header(base_url, login_url),
                                     data=constant_string.post_data(user_id, user_pw))
        if request_login.text != constant_string.header_login_success:
            return None
        for url_name in urls.keys():
            request_board = session.get(urls[url_name]+'1', headers=header(base_url, base_url))
            soup = BeautifulSoup(request_board.text, features="html.parser")
            print(f"'{url_name}':", '(' + ', '.join("'"+''.join(group.text.strip().split())+"'" for group in soup.find("thead", class_="bg_f_f9").tr.find_all('th')) + '),')


if __name__=='__main__':
    get_board_group(input(), input(), boards_url)


'''
"C:\Users\Jeuk Hwang\PycharmProjects\GaonnuriNotifier\venv\Scripts\python.exe" "C:/Users/Jeuk Hwang/PycharmProjects/GaonnuriNotifier/main.py"
['공지', '교무연구부', '[전교생 필독] 2020-2학기 수강 정정 완료 현황 ([Must Read] Completion of Course Modification for 2020 Fall Semester]', '2020.09.09', '135']
['공지', '학생회', '3주차(09.09-09.12) 운동시설 사용 공지 (Notice on the use of exercise facilities on 3rd week(09.09-09.12))', '2020.09.09', '113']
['공지', '학부 공지', '3학년 금주 영어 모의 면접 실시 안내(9월10일)', '2020.09.07', '256']
['공지', '학부 공지', 'ECC English Weekly 2', '2020.09.07', '101']
['공지', '교무연구부', '2020학년도 KSA 창의연구활동 중간발표회(2020 Creative Research Activity Mid-term Presentation)', '2020.09.07', '546']
['공지', '학생회', '2020 1학기 연구회 최종 연구보고서 공개', '2020.09.05', '639']
['공지', '학부 공지', '2020학년도 수리정보과학부 POW8 시행 안내(Announcement on Implementation of the 2020 POW8)', '2020.09.04', '352']
['공지', '상담실', '2020학년도 2학기 3주차 담임활동 자료 안내 ( 2020 2nd semester 3rd week guide of data on homeroom activities )', '2020.09.04', '108']
['공지', '학생생활부', '2학년 귀교 관련 안내! Information on 2nd grade returning to school', '2020.09.04', '1055']
['공지', '학생회', '2020년 2학기 라인 대표 선발 2020 2nd Semester Line Representatives Selection', '2020.09.04', '388']
['공지', '도서관', '카이스트 도서관 전자정보 교외접속 서비스 로그인 URL 안내(Announcements regarding the KAIST library Electronic Information Access Service Login URL)', '2020.09.03', '204']
['공지', '학부 공지', '창조관 천문대 태풍 피해 관련 학생 주의 당부 (Notice for Students on Typhoon Damage at Changjo-Gwan Observatory)', '2020.09.03', '370']
['공지', '학부 공지', 'PeerWise 게임형 물리 랭킹전 시상 및 단체활동 부여 안내', '2020.09.03', '216']
['공지', '학부 공지', '[3학년 필독] (개인별) 물리 심층면접 실시 안내 ([Must-read for Senior students] (Individual) Physics depth interview)', '2020.09.01', '241']
['공지', '학생생활부', 'KSA 학생들에게 드리는 글', '2020.08.28', '958']
['공지', '학부 공지', '[3학년 필독] 영어모의면접 실시 안내 (ECC Senior Interview) [For Korean Seniors Only]', '2020.08.28', '315']
['공지', '학부 공지', '[수업방식 추가 공지] 2020-2학기 ECC 수강학생 및 시간표 공지 / ECC timetable and students list for the fall semester', '2020.08.25', '691']
['공지', '상담실', '2020학년도 2학기 폭력예방교육 안내 (필참, ~9월 25일까지) 2020 2nd semester violence prevention education (Necessary. ~September 25th)', '2020.08.25', '197']
['공지', '학생회', '정보부에서 학교 구성원 여러분께 고하는 글', '2020.08.24', '900']
['공지', '학부 공지', '2020-2학기 화학생물학부 온라인 수업 플랫폼 공지 (Announcement of Online Class Platform for Department of Chemistry and Biology of 2020 2nd Semester)', '2020.08.24', '250']
['공지', '학생생활부', '[전교생 필독] 귀교 후 학교 생활지도 집중기간 알림 Announcement of the instruction for school life. (school life guidance concentration term after returning to school))', '2020.08.23', '1289']
['공지', '교무연구부', '2020학년도 2학기 수업 강의실 배정표(Class Assignment)', '2020.08.21', '871']
['공지', '학생생활부', '2020학년도 2학기 귀교일정 안내문(0820) (Notice for 2020 2nd semester return schedules(0820))', '2020.08.20', '1302']
['공지', '보건실', '[건강상태 자가진단] 시행 안내 ([Self health condition check] implementation guide)', '2020.08.19', '1200']
['공지', '학생회', '2020 2학기 연구회 모집 2020 2nd Semester Research Group Enrollment (개학 연기에 따른 기한 수정)(Deadlines Changed)', '2020.08.16', '602']
['공지', '', '2020학년도 제17회 인문학술발표대회 개최 안내 (17th Humanities Conference) Guidance for the 17th Humanities Conference in 2020', '2020.06.04', '494']
['328', '학생생활부', '[필독] 제10호 태풍 하이선 관련 학생 생활안전 안내(9.7.월. 온라인 원격수업 실시)[Requirement] Guidance on student life safety related to Typhoon No. 10 HAISHEN (9.7. Mon Conducting online remote classes)', '2020.09.04', '598']
['327', '학생생활부', '[필독]교내 전지역에 노란색 잔여물 접촉 금지 안내 ([Must Read] Guides Against Contact with Yellow Residues Throughout the School)', '2020.09.03', '304']
['326', '학생회', '제29대 학생운영위원회 1학년 차장단 선발 결과 공고', '2020.09.02', '508']
['325', '학생회', '2020 2학기 멘토링 멘티 모집 2020 2nd Semester Mentee Recruitment', '2020.09.02', '415']
['324', '보건실', '사회적 거리두기 2단계 방역 강화조치( ~9.6.일요일까지 연장 시행) 안내 [Social distancing Level 2 is extended and strengthened until 9.6, Sun]', '2020.09.02', '212']
['323', '상담실', '2020학년도 9월 예절교육 안내', '2020.09.01', '55']

['23', '[회의록] 2학기 학생운영위원회 회의록 [Conference Minutes] 2nd Semester Student Committee Conference Minutes', '총무부', '2020.08.31', '206']
['22', '[회의록] 2020학년도 1학기 학생운영위원회 회의록', '총무부', '2020.07.01', '176']
['21', '2020 6/21 일요일 부분일식 관측행사 (2020 6/21 Sunday partial solar eclipse observation event)', '송준서', '2020.06.20', '93']
['20', '19-087 이혜라, 19-100 정진 학생 물밑 사과문', '학예부', '2020.05.02', '462']
['19', '연구회 관련 써장회의 판결문', '학예부', '2020.04.29', '363']
['18', "힙합부 '그루브' 홍보글", '학예부', '2020.03.27', '168']
['17', "방송부 '놀소리' 홍보글", '학예부', '2020.03.27', '194']
['16', "사진 촬영부 '누리빛' 홍보글", '학예부', '2020.03.27', '233']
['15', "마술부 '딜라이트' 홍보글", '학예부', '2020.03.27', '107']
['14', "어쿠스틱 밴드부 '루니' 홍보글", '학예부', '2020.03.27', '160']
['13', "보드게임부 '루비콘' 홍보글", '학예부', '2020.03.27', '121']
['12', "댄스부 '별보라' 홍보글", '학예부', '2020.03.27', '162']
['11', "미술부 '비나리' 홍보글", '학예부', '2020.03.27', '85']
['10', "도서 문화부 '서향' 홍보글", '학예부', '2020.03.27', '133']
['9', "락 밴드부 '스터전' 홍보글", '학예부', '2020.03.27', '144']
['8', "연극부 '쏠' 홍보글", '학예부', '2020.03.27', '108']
['7', "사물놀이부 '어우러짐' 홍보글", '학예부', '2020.03.27', '93']
['6', "신문 교지부 'ESRA' 홍보글", '학예부', '2020.03.27', '109']
['5', "영화 촬영부 'MC FILM' 홍보글", '학예부', '2020.03.27', '109']
['4', "컴퓨터부 'EOS' 홍보글", '학예부', '2020.03.27', '134']

['2', '한국과학영재학교 학생회실 사용 규정', '총무부', '2020.07.28', '155']
['1', '.KAIST 부설 한국과학영재학교 학생회칙', '총무부', '2020.07.27', '67']

['2', '[ver 1.1 업데이트]영독작 단어 중복 찾아주는 프로그램 DoubleCross', 'ksa19124', '19-124', '2020.08.29', '238']
['1', '수강 계획 파일 Zamong(2020.08.12)', 'ksa18087', '이민석', '2020.08.12', '206']

['7', 'LOST', '휴대폰을 찾습니다', '18-105', '2020.09.09', '15']
['6', 'FOUND', '휴대폰 찾아가세요', '장완주', '2020.09.08', '209']
['5', 'LOST', '에어팟 프로 찾고 있습니다.', '20-104', '2020.09.02', '60']
['4', 'SOLVED', '골전도식 이어폰 하나를 찾습니다', '20-089', '2020.09.01', '80']
['3', 'FOUND', '분실물 습득', '학생지원부', '2020.06.18', '309']
['2', '', '6월 10일 예지관 검정 아이폰(파란색 케이스) 분실물 획득', '학생지원부', '2020.06.10', '124']
['1', 'SOLVED', '저희 학교 개학일좀 찾아주세요', '19-108', '2020.04.07', '578']

['공지', '국제과학영재 학술대회 JAPAN SUPER SCIENCE FAIR Online(JSSF) 2020 참여 학생 선발', '연구팀', '2020.09.09', '2020-09-14', '100']
['공지', '제5회 세계청소년올림피아드 온라인 KIYO4i 2020', '연구팀', '2020.08.31', '2020-09-20', '294']
['공지', '[기한연장] 제14회 노벨과학에세이대회 참가학생 모집(~9.7)', '연구팀', '2020.08.24', '2020-09-07', '356']
['공지', '2020 KSA 저널 "Research Connect" 투고 논문 모집(~10.16)', '연구팀', '2020.08.19', '2020-10-16', '300']
['공지', '2020년도 대한민국 인재상 선발 안내', '학생생활부', '2020.08.04', '2020-08-31', '437']
['공지', '[2020 대한민국 청소년 온라인 창업경진대회]', '학생생활부', '2020.07.24', '2020-09-04', '169']
['27', '물리문제연구회 일반전형 2단계 합격자 안내', '19-120', '2020.09.04', '', '220']
['26', '2020년 2학기 번역버디 추가모집', '번역버디', '2020.08.30', '2020-08-31', '293']
['25', '물리문제연구회 일반전형 1단계 합격자 및 특별전형 합격자 안내', '19-120', '2020.08.22', '', '301']
['24', '[장학금] 4차 산업혁명 영재 장학생 선발', '학생생활부', '2020.08.14', '2020-08-21', '416']
['23', '제14회 청소년 119안전뉴스 경진대회 개최 계획', '학생생활부', '2020.08.03', '2020-09-29', '73']
['22', '2020학년도 2학기 물리문제연구회 신입 연구회원(2기) 선발안내', '홍원기', '2020.07.31', '2020-08-15', '198']
['21', 'AI기반 프로젝트학습 경진대회', '연구팀', '2020.07.29', '', '222']
['20', '환경보전 및 에너지 절감 아이디어 공모전', '학생생활부', '2020.07.24', '2020-07-31', '84']
['19', '2020 부산발명아이디어그리기대회 및 지역교육청 학생발명대회 취소 알림', '연구팀', '2020.07.22', '', '73']
['18', '[ 내가만드는 해양교육문화박람회 공모 ] _ 국립해양박물관', '학생생활부', '2020.07.16', '2020-08-03', '111']
['17', '제5회 부산 지역탐구대회 개최 안내', '연구팀', '2020.07.02', '', '234']
['16', '사사사 선발 결과 공고', '강라엘', '2020.07.01', '', '411']
['15', '[교무연구부] 제10회 e-ICON 세계대회 국내 참가 대상자 모집 안내(~7.3)([Office of Academics and Research] Recruiting domestic participants for the 10th e-ICON World Contest (~7.3))', '연구팀', '2020.06.26', '2020-07-03', '262']
['14', '인기폭발 꿀 봉사단체 ♡♥♡사사사♡♥♡의 신규 단원을 모집합니다!!!!', '강라엘', '2020.06.21', '2020-06-26', '516']

['공지', '잡담', '학생회 말말말 변경사항에 대해서 공지드립니다.', '2020.08.31', '404']
['공지', '', '정보부에서 알립니다', '2020.08.27', '1029']
['70', '잡담', '양심고백)사실 학교에남고싶었는데', '2020.09.09', '124']
['69', '잡담', '정말 화', '2020.09.09', '120']
['68', '잡담', '기상송은 누가 정하는거야', '2020.09.09', '157']
['67', '잡담', '2학년 귀교 후 체육 시설에 대해', '2020.09.08', '397']
['66', '잡담', '지금 말말말 분위기 좋다', '2020.09.08', '291']
['65', '잡담', 'ㅇㅅㅇ...', '2020.09.08', '299']
['64', '잡담', '배고프당 ㅠㅅㅠ', '2020.09.08', '411']
['63', '학교 선생님께', '멘토링 신청지금은 어려울까요ㅠ', '2020.09.08', '261']
['62', '잡담', '지극히 개인적인 노래 추천 공간!', '2020.09.08', '524']
['61', '잡담', '순환등교의 방역효과가 문제가 아니라', '2020.09.08', '211']
['60', '학교 선생님께', '기숙학교 2/3 순환등교의 의의가 무엇인가요?', '2020.09.07', '253']
['59', '잡담', '20학번이 귀가를 반대하는 글이 없는 이유?', '2020.09.07', '346']
['58', '잡담', '아래 입시 관련 게시물을 읽고 쓰는 글', '2020.09.07', '434']
['57', '잡담', '후배들을 위한 입시 설명', '2020.09.06', '412']
['56', '잡담', '크사 대숲', '2020.09.06', '254']
['55', '잡담', '죄송합니다 말머리생각을 안하고 있었어요', '2020.09.06', '368']
['54', '학교 선생님께', '1학년귀교가 도대체 무슨문제가있는건지 모르겠네', '2020.09.06', '358']
['53', '학교 선생님께', '오진호 선생님께- 학생회 회의록을 읽고 질문드립니다.', '2020.09.06', '494']
['52', '잡담', '기숙사 와이파이', '2020.09.06', '172']
['51', '학교 선생님께', '18-107 조찬우입니다', '2020.09.04', '318']

['20', '2021학년도 주요대학 입시일정 및 추천서 일정', '2020.07.02']
['19', '3학년 자기소개서 검토 안내(필독)', '2020.06.23']
['18', '2021학년도 주요대학 입시설명회 일정(수정)', '2020.06.15']
['17', '2021학년도 서울대학교 입시요강 및 각종 서식', '2020.06.04']
['16', '2021학년도 서울대학교 입시요강 및 작년 면접 문항', '2020.04.22']
['15', '화학생물학부 잡지 화기생기 연구회원 모집(Recruitment of members of the magazine of the Department of Chemistry and Biology ‘Feel Chemistry, Feel Life!’)', '2020.03.25']
['14', '작년 성균관대 입시요강(주요내용 정리)', '2020.03.17']
['13', '작년 한양대 입시요강(주요내용 정리)', '2020.03.17']
['12', '작년 고려대 입시요강(주요내용 정리)', '2020.03.17']
['11', '작년 연세대 입시요강(주요내용 정리)', '2020.03.17']
['10', '작년 지스트 입시요강(주요내용 정리)', '2020.03.17']
['9', '작년 유니스트 입시요강(주요내용 정리)', '2020.03.17']
['8', '작년 포스텍 입시요강(주요내용 정리)', '2020.03.17']
['7', '작년 서울대 입시요강(주요내용 정리)', '2020.03.17']
['6', '작년 카이스트 입시요강(주요내용 정리)', '2020.03.17']
['5', '포스텍 입시 기출', '2020.03.05']
['4', '주요대학 면접기출 링크', '2020.03.05']
['3', '주요대학 면접 복기 파일', '2020.03.05']
['2', '작년 카이스트, 서울대, 포스텍 등 주요대학 자기소개서 양식(17학번 입시자료)', '2020.03.05']
['1', '2021학년도 대학입시 게시판(18학번 대상)', '2020.03.04']

['5', '대기', '견우관 235호 스탠드 수리', '18-099', '2020.09.09', '16']
['4', '대기', '직녀관 209호 스탠드 수리', '18-078', '2020.08.25', '20']
['3', '대기', '기숙사 와이파이가 잡히지 않습니다.', '19-012', '2020.07.09', '59']
['2', '대기', '창조관 8층 자습실 형광등이 들어오지 않습니다', '19-044', '2020.06.29', '54']
['1', '대기', '형설관 3층 정수기에서 온수가 샙니다', '18-101', '2020.06.26', '58']


'''