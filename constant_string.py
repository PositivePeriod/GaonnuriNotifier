program_name = 'Gaonnuri Notifier'

file_path = './data'
icon_file_path = './data/icon.ico'
info_file_path = './data/info.txt'
board_file_path = './data/board/'

base_url = 'https://gaonnuri.ksain.net'
main_url = f'{base_url}/xe'
login_url = f'{main_url}/login'
boards = {'공지사항 게시판': 'board_notice', '임시 게시판': 'board_LoAj77', '규정 게시판': 'board_KbST22',
          '자유 게시판': 'board_free', '분실물 게시판': 'board_lostfound', '선발 공모 게시판': 'board_select',
          '학생회 말말말': 'board_jMJE99', '입시 정보 게시판': 'board_entrance', '수리 요청 게시판': 'board_repair'}

boards_info = {'공지사항 게시판': ('번호', '분류', '제목', '날짜', '조회수'),
               '임시 게시판': ('번호', '제목', '글쓴이', '날짜', '조회수'),
               '규정 게시판': ('번호', '제목', '글쓴이', '날짜', '조회수'),
               '자유 게시판': ('번호', '제목', '아이디', '글쓴이', '날짜', '조회수'),
               '분실물 게시판': ('번호', '분류', '제목', '글쓴이', '날짜', '조회수'),
               '선발 공모 게시판': ('번호', '제목', '글쓴이', '날짜', '마감기한', '조회수'),
               '학생회 말말말': ('번호', '분류', '제목', '날짜', '조회수'),
               '입시 정보 게시판': ('번호', '제목', '날짜'),
               '수리 요청 게시판': ('번호', '분류', '제목', '글쓴이', '날짜', '조회수')}

boards_url = dict(zip(boards.keys(), [f'{main_url}/index.php?mid={board}&page=' for board in boards.values()]))
