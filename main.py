from js import document, window
from pyodide.ffi import create_proxy
import random
from time import time

main_container = document.getElementById('main-container')
loading_div = document.getElementById('loading')
footer_info = document.getElementById('footer-info')
author_name = document.getElementById('author-name')

# 切換連結顯示
def toggle_links(event):
    if footer_info.classList.contains('show'):
        footer_info.classList.remove('show')
    else:
        footer_info.classList.add('show')

author_name.addEventListener('click', create_proxy(toggle_links))

# ========== 韓文資料定義 ==========
RAW_TEXTS = {
    4: "ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ",
    5: "ㅏ ㅑ ㅓ ㅕ ㅗ ㅛ ㅜ ㅠ ㅡ ㅣ ㅐ ㅒ ㅔ ㅖ ㅘ ㅙ ㅚ ㅝ ㅞ ㅟ ㅢ",
    6: ("가 거 고 구 그 기 갸 겨 교 규 게 계 "
        "나 너 노 누 느 니 냐 녀 뇨 뉴 네 녜 "
        "다 더 도 두 드 디 댜 더 됴 듀 데 뎨 "
        "라 러 로 루 르 리 랴 려 료 류 레 례 "
        "마 머 모 무 므 미 먀 먀 묘 뮤 메 몌 "
        "바 버 보 부 브 비 뱌 벼 뵤 뷰 베 볘 "
        "사 서 소 수 스 시 샤 셔 쇼 슈 세 셰 "
        "아 어 오 우 으 이 야 여 요 유 예 예 "
        "자 저 조 주 즈 지 쟈 져 죠 쥬 제 졔 "
        "차 처 초 추 츠 치 챠 처 쵸 츄 체 쳬 "
        "카 커 코 쿠 크 키 캬 커 쿄 큐 케 켸 "
        "타 터 토 투 트 티 탸 터 툐 튜 테 톄 "
        "파 퍼 포 푸 프 피 퍄 퍼 표 퓨 페 폐 "
        "하 허 호 후 흐 히 햐 혀 효 휴 헤 혜"),
    7: ("개 걔 괘 괴 궤 귀 긔 "
        "내 냬 놰 뇌 눼 뉘 늬 "
        "대 댸 돼 되 뒈 뒈 듸 "
        "래 럐 뢔 뢰 뤠 뤼 릐 "
        "매 먜 뫠 뫼 뭬 뮈 믜 "
        "배 뱨 봬 뵈 붸 뷔 븨 "
        "새 쌔 쇄 쇠 쉐 쉬 싀 "
        "애 얘 왜 외 웨 위 의 "
        "재 쨰 좨 죄 줴 쥐 즤 "
        "채 쳬 쵀 최 췌 츄 츼 "
        "캐 컈 쾌 쾨 퀘 퀴 킈 "
        "태 턔 퇘 퇴 퉤 튀 틔 "
        "패 퍠 퐤 푀 풰 퓌 픠 "
        "해 햬 홰 회 훼 휘 희")
}

BASE_CHINESE = {
    'ㄱ': 'k', 'ㄲ': 'kk', 'ㄴ': 'n', 'ㄷ': 't', 'ㄸ': 'tt', 'ㄹ': 'r',
    'ㅁ': 'm', 'ㅂ': 'p', 'ㅃ': 'pp', 'ㅅ': 's', 'ㅆ': 'ss', 'ㅇ': '',
    'ㅈ': 'j', 'ㅉ': 'jj', 'ㅊ': 'ch', 'ㅋ': 'kh', 'ㅌ': 'th', 'ㅍ': 'ph', 'ㅎ': 'h',
    'ㅏ': 'a', 'ㅑ': 'ya', 'ㅓ': 'eo', 'ㅕ': 'yeo', 'ㅗ': 'o', 'ㅛ': 'yo',
    'ㅜ': 'u', 'ㅠ': 'yu', 'ㅡ': 'eu', 'ㅣ': 'i',
    'ㅐ': 'ae', 'ㅒ': 'yae', 'ㅔ': 'e', 'ㅖ': 'ye',
    'ㅘ': 'wa', 'ㅙ': 'wae', 'ㅚ': 'oe', 'ㅝ': 'wo', 'ㅞ': 'we', 'ㅟ': 'wi', 'ㅢ': 'ui',
    '가': 'ga', '거': 'geo', '고': 'go', '구': 'gu', '그': 'geu', '기': 'gi',
    '갸': 'gya', '겨': 'gyeo', '교': 'gyo', '규': 'gyu', '게': 'ge', '계': 'gye',
    '나': 'na', '너': 'neo', '노': 'no', '누': 'nu', '느': 'neu', '니': 'ni',
    '냐': 'nya', '녀': 'nyeo', '뇨': 'nyo', '뉴': 'nyu', '네': 'ne', '녜': 'nye',
    '다': 'da', '더': 'deo', '도': 'do', '두': 'du', '드': 'deu', '디': 'di',
    '댜': 'dya', '됴': 'dyo', '듀': 'dyu', '데': 'de', '뎨': 'dye',
    '라': 'ra', '러': 'reo', '로': 'ro', '루': 'ru', '르': 'reu', '리': 'ri',
    '랴': 'rya', '려': 'ryeo', '료': 'ryo', '류': 'ryu', '레': 're', '례': 'rye',
    '마': 'ma', '머': 'meo', '모': 'mo', '무': 'mu', '므': 'meu', '미': 'mi',
    '먀': 'mya', '묘': 'myo', '뮤': 'myu', '메': 'me', '몌': 'mye',
    '바': 'ba', '버': 'beo', '보': 'bo', '부': 'bu', '브': 'beu', '비': 'bi',
    '뱌': 'bya', '벼': 'byeo', '뵤': 'byo', '뷰': 'byu', '베': 'be', '볘': 'bye',
    '사': 'sa', '서': 'seo', '소': 'so', '수': 'su', '스': 'seu', '시': 'si',
    '샤': 'sya', '셔': 'syeo', '쇼': 'syo', '슈': 'syu', '세': 'se', '셰': 'sye',
    '아': 'a', '어': 'eo', '오': 'o', '우': 'u', '으': 'eu', '이': 'i',
    '야': 'ya', '여': 'yeo', '요': 'yo', '유': 'yu', '예': 'ye',
    '자': 'ja', '저': 'jeo', '조': 'jo', '주': 'ju', '즈': 'jeu', '지': 'ji',
    '쟈': 'jya', '져': 'jyeo', '죠': 'jyo', '쥬': 'jyu', '제': 'je', '졔': 'jye',
    '차': 'cha', '처': 'cheo', '초': 'cho', '추': 'chu', '츠': 'cheu', '치': 'chi',
    '챠': 'chya', '쳐': 'chyeo', '쵸': 'chyo', '츄': 'chyu', '체': 'che', '쳬': 'chye',
    '카': 'ka', '커': 'keo', '코': 'ko', '쿠': 'ku', '크': 'keu', '키': 'ki',
    '캬': 'kya', '쿄': 'kyo', '큐': 'kyu', '케': 'ke', '켸': 'kye',
    '타': 'ta', '터': 'teo', '토': 'to', '투': 'tu', '트': 'teu', '티': 'ti',
    '탸': 'tya', '툐': 'tyo', '튜': 'tyu', '테': 'te', '톄': 'tye',
    '파': 'pa', '퍼': 'peo', '포': 'po', '푸': 'pu', '프': 'peu', '피': 'pi',
    '퍄': 'pya', '표': 'pyo', '퓨': 'pyu', '페': 'pe', '폐': 'pye',
    '하': 'ha', '허': 'heo', '호': 'ho', '후': 'hu', '흐': 'heu', '히': 'hi',
    '햐': 'hya', '혀': 'hyeo', '효': 'hyo', '휴': 'hyu', '헤': 'he', '혜': 'hye',
    '개': 'gae', '걔': 'gyae', '괘': 'gwae', '괴': 'goe', '궤': 'gwe', '귀': 'gwi', '긔': 'gui',
    '내': 'nae', '냬': 'nyae', '놰': 'nwae', '뇌': 'noe', '눼': 'nwe', '뉘': 'nwi', '늬': 'nui',
    '대': 'dae', '댸': 'dyae', '돼': 'dwae', '되': 'doe', '뒈': 'dwe', '듸': 'dui',
    '래': 'rae', '럐': 'ryae', '뢔': 'rwae', '뢰': 'roe', '뤠': 'rwe', '뤼': 'rwi', '릐': 'rui',
    '매': 'mae', '먜': 'myae', '뫠': 'mwae', '뫼': 'moe', '뭬': 'mwe', '뮈': 'mwi', '믜': 'mui',
    '배': 'bae', '뱨': 'byae', '봬': 'bwae', '뵈': 'boe', '붸': 'bwe', '뷔': 'bwi', '븨': 'bui',
    '새': 'sae', '쌔': 'syae', '쇄': 'swae', '쇠': 'soe', '쉐': 'swe', '쉬': 'swi', '싀': 'sui',
    '애': 'ae', '얘': 'yae', '왜': 'wae', '외': 'oe', '웨': 'we', '위': 'wi', '의': 'ui',
    '재': 'jae', '쨰': 'jyae', '좨': 'jwae', '죄': 'joe', '줴': 'jwe', '쥐': 'jwi', '즤': 'jui',
    '채': 'chae', '쳬': 'chyae', '쵀': 'chwae', '최': 'choe', '췌': 'chwe', '츼': 'chwi',
    '캐': 'kae', '컈': 'kyae', '쾌': 'kwae', '쾨': 'koe', '퀘': 'kwe', '퀴': 'kwi', '킈': 'kui',
    '태': 'tae', '턔': 'tyae', '퇘': 'twae', '퇴': 'toe', '퉤': 'twe', '튀': 'twi', '틔': 'tui',
    '패': 'pae', '퍠': 'pyae', '퐤': 'pwae', '푀': 'poe', '풰': 'pwe', '퓌': 'pwi', '픠': 'pui',
    '해': 'hae', '햬': 'hyae', '홰': 'hwae', '회': 'hoe', '훼': 'hwe', '휘': 'hwi', '희': 'hui'
}

BASE_ROMAJI = BASE_CHINESE

library_words = {}
for key in RAW_TEXTS:
    library_words[key] = RAW_TEXTS[key].split()

def ensure_all_words_covered():
    all_words = set()
    for words in library_words.values():
        all_words.update(words)
    for word in all_words:
        if word not in BASE_CHINESE:
            BASE_CHINESE[word] = word
        if word not in BASE_ROMAJI:
            BASE_ROMAJI[word] = word

ensure_all_words_covered()

library_status = {4: True, 5: False, 6: False, 7: False}
pronunciation_status = {'chinese': False, 'romaji': False}
pronunciation_locked = False
last_click_time = 0
current_word = '가'

dialogs = {}
contents = {}

desktop_config = {
    1: {'left': '38%', 'top': '10%', 'width': '36%', 'height': '54%', 'font_size': '230px'},
    2: {'left': '75%', 'top': '20%', 'width': '23%', 'height': '18%', 'font_size': '76px'},
    3: {'left': '75%', 'top': '40%', 'width': '23%', 'height': '18%', 'font_size': '76px'},
    4: {'left': '1%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '子音', 'icon_size': '24px'},
    5: {'left': '10%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '母音', 'icon_size': '24px'},
    6: {'left': '19%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '基本', 'icon_size': '24px'},
    7: {'left': '28%', 'top': '83%', 'width': '8%', 'height': '14%', 'icon': '複合', 'icon_size': '24px'},
    8: {'left': '59%', 'top': '70%', 'width': '15%', 'height': '27%', 'font_size': '40px'},
    9: {'left': '75%', 'top': '70%', 'width': '15%', 'height': '27%', 'font_size': '40px'}
}

mobile_config = {
    1: {'font_size': '90px', 'icon': None},
    2: {'font_size': '30px', 'icon': None},
    3: {'font_size': '30px', 'icon': None},
    4: {'icon': '子音', 'icon_size': '14px'},
    5: {'icon': '母音', 'icon_size': '14px'},
    6: {'icon': '基本', 'icon_size': '14px'},
    7: {'icon': '複合', 'icon_size': '14px'},
    8: {'font_size': '18px'},
    9: {'font_size': '18px'}
}

def create_dialog(dialog_id, base_config):
    config = base_config.copy()
    width = window.innerWidth
    is_mobile = width <= 567
    if is_mobile:
        if dialog_id in mobile_config:
            mobile_settings = mobile_config[dialog_id]
            if 'font_size' in mobile_settings:
                config['font_size'] = mobile_settings['font_size']
            if 'icon' in mobile_settings:
                config['icon'] = mobile_settings['icon']
            if 'icon_size' in mobile_settings:
                config['icon_size'] = mobile_settings['icon_size']
    else:
        if dialog_id in desktop_config:
            config.update(desktop_config[dialog_id])
    dialog = document.createElement('div')
    dialog.id = f'dialog-{dialog_id}'
    dialog.className = f'dialog {config["class"]}'
    if not is_mobile:
        if 'left' in config:
            dialog.style.left = config['left']
        if 'top' in config:
            dialog.style.top = config['top']
        if 'width' in config:
            dialog.style.width = config['width']
        if 'height' in config:
            dialog.style.height = config['height']
    if config.get('is_clickable', False):
        dialog.className += ' clickable'
    content_div = document.createElement('div')
    content_div.id = f'content-{dialog_id}'
    content_div.className = 'display-content'
    if 'font_size' in config:
        content_div.style.fontSize = config['font_size']
    dialog.appendChild(content_div)
    if dialog_id in [4, 5, 6, 7]:
        icon_div = document.createElement('div')
        icon_div.className = 'library-icon'
        icon_div.textContent = config['icon']
        if 'icon_size' in config:
            icon_div.style.fontSize = config['icon_size']
        content_div.appendChild(icon_div)
    elif dialog_id == 8:
        content_div.textContent = '讀音'
    elif dialog_id == 9:
        content_div.textContent = '下一個'
    
    if dialog_id == 1:
        speaker_btn = document.createElement('div')
        speaker_btn.id = 'speaker-btn-red'
        speaker_btn.className = 'speaker-btn-red'
        speaker_btn.textContent = '🔊'
        speaker_btn.title = '朗讀目前顯示的文字'
        dialog.appendChild(speaker_btn)
    
    if is_mobile:
        create_mobile_layout(dialog, dialog_id)
    else:
        main_container.appendChild(dialog)
    return dialog, content_div

def create_mobile_layout(dialog, dialog_id):
    if dialog_id == 1:
        main_container.innerHTML = ''
        main_container.appendChild(dialog)
    elif dialog_id == 2:
        if not document.getElementById('pronunciation-row'):
            row = document.createElement('div')
            row.id = 'pronunciation-row'
            row.className = 'pronunciation-row'
            main_container.appendChild(row)
        row = document.getElementById('pronunciation-row')
        row.appendChild(dialog)
    elif dialog_id == 3:
        row = document.getElementById('pronunciation-row')
        if row:
            row.appendChild(dialog)
    elif dialog_id in [4, 5, 6, 7]:
        if not document.getElementById('library-grid'):
            grid = document.createElement('div')
            grid.id = 'library-grid'
            grid.className = 'library-grid'
            main_container.appendChild(grid)
        grid = document.getElementById('library-grid')
        grid.appendChild(dialog)
    elif dialog_id in [8, 9]:
        if not document.getElementById('action-row'):
            row = document.createElement('div')
            row.id = 'action-row'
            row.className = 'action-row'
            main_container.appendChild(row)
        row = document.getElementById('action-row')
        row.appendChild(dialog)

base_config = {
    1: {'class': 'dialog-1', 'is_clickable': False},
    2: {'class': 'dialog-2', 'is_clickable': False},
    3: {'class': 'dialog-3', 'is_clickable': False},
    4: {'class': 'dialog-4', 'is_clickable': True, 'icon': '子音'},
    5: {'class': 'dialog-5', 'is_clickable': True, 'icon': '母音'},
    6: {'class': 'dialog-6', 'is_clickable': True, 'icon': '基本'},
    7: {'class': 'dialog-7', 'is_clickable': True, 'icon': '複合'},
    8: {'class': 'dialog-8', 'is_clickable': True},
    9: {'class': 'dialog-9', 'is_clickable': True}
}

for dialog_id in range(1, 10):
    dialog, content = create_dialog(dialog_id, base_config[dialog_id])
    dialogs[dialog_id] = dialog
    contents[dialog_id] = content

if loading_div:
    loading_div.style.display = 'none'

# ========== 朗讀功能（韓文版） ==========
from js import speechSynthesis, SpeechSynthesisUtterance

best_ko_voice = None
voices_loaded = False
speaker_red_btn = None

def init_voices():
    global best_ko_voice, voices_loaded
    voices = speechSynthesis.getVoices()
    for voice in voices:
        if 'ko' in voice.lang and not best_ko_voice:
            best_ko_voice = voice
    voices_loaded = True
    if best_ko_voice:
        print(f"韓文語音: {best_ko_voice.name}")

def speak_text(event):
    global best_ko_voice
    if not voices_loaded:
        init_voices()
    current_word_element = document.getElementById('content-1')
    if not current_word_element:
        print("找不到當前文字元素")
        return
    text_to_speak = current_word_element.textContent
    if not text_to_speak or text_to_speak == '':
        print("沒有文字可朗讀")
        return
    if speaker_red_btn:
        speaker_red_btn.classList.add('speaking')
    utterance = SpeechSynthesisUtterance.new(text_to_speak)
    utterance.lang = 'ko-KR'
    utterance.rate = 0.85
    utterance.pitch = 1.05
    if best_ko_voice:
        utterance.voice = best_ko_voice
    def on_end(event):
        if speaker_red_btn:
            speaker_red_btn.classList.remove('speaking')
    def on_error(event):
        if speaker_red_btn:
            speaker_red_btn.classList.remove('speaking')
        print(f"朗讀錯誤: {event.error}")
    utterance.onend = create_proxy(on_end)
    utterance.onerror = create_proxy(on_error)
    speechSynthesis.cancel()
    speechSynthesis.speak(utterance)
    print(f"朗讀: {text_to_speak} (語言: 韓文)")

def on_voices_changed(event=None):
    init_voices()

speechSynthesis.onvoiceschanged = create_proxy(on_voices_changed)
init_voices()

def bind_speaker_button():
    global speaker_red_btn
    speaker_red_btn = document.getElementById('speaker-btn-red')
    if speaker_red_btn:
        speaker_red_btn.addEventListener('click', create_proxy(speak_text))
        print("音量按鈕已綁定")
    else:
        window.setTimeout(create_proxy(bind_speaker_button), 500)

bind_speaker_button()

def update_library_appearance():
    for lib_id in [4, 5, 6, 7]:
        dialog = dialogs[lib_id]
        if library_status[lib_id]:
            dialog.classList.remove('library-off')
        else:
            dialog.classList.add('library-off')

def update_displays():
    contents[1].textContent = current_word
    show_pronunciation = pronunciation_locked or pronunciation_status['chinese'] or pronunciation_status['romaji']
    if show_pronunciation and current_word in BASE_CHINESE:
        contents[2].textContent = BASE_CHINESE[current_word]
    else:
        contents[2].textContent = ''
    if show_pronunciation and current_word in BASE_ROMAJI:
        contents[3].textContent = BASE_ROMAJI[current_word]
    else:
        contents[3].textContent = ''
    update_library_appearance()
    if pronunciation_locked:
        contents[8].textContent = '鎖定'
        dialogs[8].classList.add('locked')
    else:
        if pronunciation_status['chinese'] or pronunciation_status['romaji']:
            contents[8].textContent = '隱藏'
        else:
            contents[8].textContent = '讀音'
        dialogs[8].classList.remove('locked')

def update_current_word(force=False):
    global current_word
    available_words = []
    for lib_id in [4, 5, 6, 7]:
        if library_status[lib_id]:
            available_words.extend(library_words[lib_id])
    if not available_words:
        current_word = ''
        return
    if not force and current_word in available_words:
        return
    else:
        current_word = random.choice(available_words)

def on_library_click(lib_id):
    def handler(event):
        global library_status
        library_status[lib_id] = not library_status[lib_id]
        update_current_word(force=False)
        update_displays()
    return handler

def on_pronunciation_click(event):
    global last_click_time, pronunciation_locked, pronunciation_status
    current_time = time() * 1000
    time_diff = current_time - last_click_time
    if time_diff < 300:
        pronunciation_locked = not pronunciation_locked
        if pronunciation_locked:
            pronunciation_status['chinese'] = True
            pronunciation_status['romaji'] = True
        else:
            pronunciation_status['chinese'] = False
            pronunciation_status['romaji'] = False
    else:
        if not pronunciation_locked:
            if pronunciation_status['chinese'] or pronunciation_status['romaji']:
                pronunciation_status['chinese'] = False
                pronunciation_status['romaji'] = False
            else:
                pronunciation_status['chinese'] = True
                pronunciation_status['romaji'] = True
    last_click_time = current_time
    update_displays()

def on_next_click(event):
    global pronunciation_status, pronunciation_locked
    if not pronunciation_locked:
        pronunciation_status['chinese'] = False
        pronunciation_status['romaji'] = False
    update_current_word(force=True)
    update_displays()

dialogs[4].addEventListener('click', create_proxy(on_library_click(4)))
dialogs[5].addEventListener('click', create_proxy(on_library_click(5)))
dialogs[6].addEventListener('click', create_proxy(on_library_click(6)))
dialogs[7].addEventListener('click', create_proxy(on_library_click(7)))
dialogs[8].addEventListener('click', create_proxy(on_pronunciation_click))
dialogs[9].addEventListener('click', create_proxy(on_next_click))

current_word = random.choice(library_words[4])
update_library_appearance()
update_displays()

print('=' * 50)
print('王又贏學韓文四十音 1.6.0 - 音量按鈕在紅色框右下角')
print('音量按鈕放大兩倍，手機版同樣顯示在紅色框內部右下角')
print('=' * 50)
