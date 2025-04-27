#! /usr/bin/env python3
import sys
import curses
import time
import random
import os
import socket
import signal
import platform
from playsound import playsound
import psutil
from threading import Thread


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# funcao para lidar com interrupcoes do teclado


def handler(signum, frame):
    pass


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTSTP, handler)

# -------------------- VARIAVEIS GERAIS --------------------------

dir = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))  # pega o diretorio do arquivo

# boot

r"""\
 _______  ______ _______                    _____  _______
 |_____| |_____/ |                         |     | |______
 |     | |    \_ |_____  _____ _____ _____ |_____| ______|
                                                          
 """


# menu de selecao

MENU_HEAD = (' _______  ______ _______                    _____  _______',
             ' |_____| |_____/ |                         |     | |______',
             ' |     | |    \_ |_____  _____ _____ _____ |_____| ______|', 
             '',
             '-サーバ  6-',
              '')

MENU_HEAD2 = (
              '>\\ こんいちは, ' + socket.gethostname(), '')

MENU1 = ['端末を入る', 'ログ', '選択肢の献立を開', 'ログアウト', 'シャットダウンシステム']

MENU2 = [
    '戻る',
    'フスマを始める',
    'アパッチを始める',
    'データベースを始める',
    'スナップを始める',
    'ブルートゥースを始める',
    '匿名ネットワークリレーを始める',
    '匿名ネットワークリレーを停止',
]

# pagina de login

LOGIN_TXT = '                                                            DEVICE_OVERVIEW:'

NUMCHARS = 16

SQUARE_X = 39
SQUARE_Y = 13

TENTATIVAS_MAX = 4

LINHAS_HD = 4

LOGIN_PAUSE = 1000

POINTER = 0xf650

ELEMNT = '0123456789ABCDEF1'


LOGIN_PASS = 'パスワードを入力してください'

LOGIN_ERROR = 'パスワードが間違っています。 もう一度やり直してください'

LOGIN_USER = 'LOGON '

# tela bloqueada


BLOQUEIO = 10000000

# ----------- funcoes --------------------


def checkPS(processName):
    '''
    Funcao para checar se servicos estao em execucao
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False

def menuOpcoes(scr):

    keyInput = 0
    selection = 0
    selection_count = len(MENU2)
    selection_start_y = scr.getyx()[0]
    largura = scr.getmaxyx()[1]

    if checkPS('fusuma'):
        MENU2[1] = "フスマを停止"
    else:
        MENU2[1] = "フスマを始める"

    if checkPS('apache2'):
        MENU2[2] = "アパッチを停止"
    else:
        MENU2[2] = "アパッチを始める"
#
    if checkPS('mariadb' or 'mysqld'):
        MENU2[3] = "データベースを停止"
    else:
        MENU2[3] = "データベースを始める"

    if checkPS('snapd'):
        MENU2[4] = "スナップを停止"
    else:
        MENU2[4] = "スナップを始める"

    if checkPS('bluetoothd'):
        MENU2[5] = "ブルートゥースを停止"
    else:
        MENU2[5] = "ブルートゥースを始める"

    while keyInput != novaLinha:
        scr.move(selection_start_y, 0)
        line = 0
        for sel in MENU2:
            whole_line = '> ' + MENU2[line]
            whole_line += '\n'

            if line == selection:
                scr.addstr(whole_line, curses.A_REVERSE)
            else:
                scr.addstr(whole_line)
            line += 1
            scr.refresh()

        keyInput = scr.getch()

        if keyInput == curses.KEY_UP and selection > 0:
            selection -= 1
        elif keyInput == curses.KEY_DOWN and selection < selection_count - 1:
            selection += 1

        if keyInput == ord('\n') and selection == 0:
                thread = Thread(target=playKey)
                thread.start()
                playsound(os.path.join(dir, "audio/goBack.mp3"))

                scr.erase()
                menu()

        elif keyInput == ord('\n') and selection == 1:
            thread = Thread(target=playKey)
            thread.start()
            if checkPS('fusuma'):
                playsound(os.path.join(dir, "audio/fusumaOff.mp3"))
                print("\n\nフスマを停車ている")
                time.sleep(2)
                os.system('killall fusuma')
                scr.erase()
                opcoes()
            else:
                playsound(os.path.join(dir, "audio/fusumaOn.mp3"))
                print("\n\nフスマを始めている")
                time.sleep(2)
                os.system('fusuma -d')
                scr.erase()
                opcoes()

        elif keyInput == ord('\n') and selection == 2:
            thread = Thread(target=playKey)
            thread.start()
            if checkPS('apache'):
                playsound(os.path.join(dir, "audio/apacheOff.mp3"))
                print("\n\nアパッチを停車ている")
                time.sleep(2)
                os.system('echo {sudo password} | sudo -S -k service apache2 stop')
                scr.erase()
                opcoes()
            else:
                playsound(os.path.join(dir, "audio/apacheOn.mp3"))
                print("\n\nアパッチを始ている")
                time.sleep(2)
                os.system('echo {sudo password} | sudo -S -k service apache2 start')
                scr.erase()

                opcoes()

        elif keyInput == ord('\n') and selection == 3:
            playsound(os.path.join(dir, "audio/keyenter.wav"))

            if checkPS('mariadb'):
                playsound(os.path.join(dir, "audio/sqlOff.mp3"))
                print("\n\nデータベースを停車ている")
                time.sleep(2)
                os.system('echo {sudo password} | sudo -S -k service mysql stop')
                scr.erase()
                opcoes()
            else:
                playsound(os.path.join(dir, "audio/sqlOn.mp3"))
                print("\n\nデータベースを始ている")
                time.sleep(2)
                os.system('echo {sudo password} | sudo -S -k service mysql start')
                scr.erase()
                opcoes()
        elif keyInput == ord('\n') and selection == 4:
            thread = Thread(target=playKey)
            thread.start()
            if checkPS('snapd'):
                playsound(os.path.join(dir, "audio/snapOff.mp3"))
                print("\n\nスナップを停車ている")
                time.sleep(2)
                os.system('echo {sudo password} | sudo -S -k service snapd stop')
                scr.erase()
                opcoes()
            else:
                playsound(os.path.join(dir, "audio/snapOn.mp3"))
                print("\n\nスナップを始ている")
                time.sleep(2)
                os.system(
                    'echo {sudo password} | sudo -S -k service snapd start && echo {sudo password} | sudo -S -k service apparmor starrt'
                )
                scr.erase()
                opcoes()

        elif keyInput == ord('\n') and selection == 5:
            playsound(os.path.join(dir, "audio/keyenter.wav"))

            if checkPS('bluetoothd'):
                playsound(os.path.join(dir, "audio/bluetoothOff.mp3"))

                print("\n\nブルートゥースを停車ている")
                time.sleep(2)
                os.system('echo {sudo password} | sudo -S -k killall bluetoothd')
                scr.erase()
                opcoes()
            else:
                playsound(os.path.join(dir, "audio/bluetoothOn.mp3"))
                print("\n\nブルートゥースを始ている")
                time.sleep(2)
                os.system('echo {sudo password} | sudo -S -k bluetoothd & disown')
                scr.erase()
                opcoes()

        elif keyInput == ord('\n') and selection == 6:
            thread = Thread(target=playKey)
            thread.start()
            playsound(os.path.join(dir, "audio/torOn.mp3"))
            print("\n\n匿名ネットワークリレーを始めている")
            time.sleep(2)
            os.system('echo {sudo password} | sudo -S -k anonsurf start')
            scr.erase()
            opcoes()

        elif keyInput == ord('\n') and selection == 7:
            thread = Thread(target=playKey)
            thread.start()
            playsound(os.path.join(dir, "audio/torOff.mp3"))
            print("\n\n匿名ネットワークリレーを停車ている")
            time.sleep(2)
            os.system('echo {sudo password} | sudo -S -k anonsurf stop')
            scr.erase()
            opcoes()


def criarMenu(scr):

    keyInput = 0
    selection = 0
    selection_count = len(MENU1)
    selection_start_y = scr.getyx()[0]
    largura = scr.getmaxyx()[1]

    while keyInput != novaLinha:
        scr.move(selection_start_y, 0)
        line = 0
        for sel in MENU1:
            whole_line = '> ' + MENU1[line]
            space = largura - len(whole_line) % largura + 20
            whole_line += '\n'

            if line == selection:
                scr.addstr(whole_line, curses.A_REVERSE)
            else:
                scr.addstr(whole_line)
            line += 1
            scr.refresh()

        keyInput = scr.getch()

        # move up and down
        if keyInput == curses.KEY_UP and selection > 0:
            selection -= 1
        elif keyInput == curses.KEY_DOWN and selection < selection_count - 1:
            selection += 1

        if keyInput == ord('\n') and selection == 0:
            thread = Thread(target=playKey)
            thread.start()
            print("\n\n\nTTYの端末を入るている")
            playsound(os.path.join(dir, "audio/EnterTerminal.mp3"))

            time.sleep(2)
            os.system('tmux')

        elif keyInput == ord('\n') and selection == 1:

            thread = Thread(target=playKey)
            thread.start()
            print("\n\n\n荒坂ログを開く")

            playsound(os.path.join(dir, "audio/logs.mp3"))

            time.sleep(2)

            print(os.system('journalctl'))

            exit = scr.getch()
            if exit == ord('\n'):
                scr.erase()
                menu()
            scr.erase()
            menu()

        elif keyInput == ord('\n') and selection == 2:

            thread = Thread(target=playKey)
            thread.start()
            playsound(os.path.join(dir, "audio/options.mp3"))

            opcoes()

        elif keyInput == ord('\n') and selection == 3:
            thread = Thread(target=playKey)
            thread.start()
            playsound(os.path.join(dir, "audio/logout.mp3"))
            print("\n\n\nセッションを離れている")
            time.sleep(3)
            pid = os.getppid()
            os.kill(pid, 9)

        elif keyInput == ord('\n') and selection == 4:
            thread = Thread(target=playKey)
            thread.start()
            print("\n\n\nシャットダウン。。。")
            playsound(os.path.join(dir, "audio/shutdown.mp3"))

            time.sleep(5)
            os.system("systemctl poweroff")


def initMenu(scr):

    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)
    curses.curs_set(0)

    largura = scr.getmaxyx()[1]

    for header in MENU_HEAD:
        centr(scr, header + '\n')

    for header in MENU_HEAD2:
        typeT(scr, header + '\n')

    for i in range(largura):
        scr.addch(curses.ACS_BSBS)
    scr.refresh()

    return criarMenu(scr)


def initOpcoes(scr):

    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)
    curses.curs_set(0)

    largura = scr.getmaxyx()[1]

    for header in MENU_HEAD:
        centr(scr, header + '\n')

    for header in MENU_HEAD2:
        typeT(scr, header + '\n')

    for i in range(largura):
        scr.addch(curses.ACS_BSBS)
    scr.refresh()

    return menuOpcoes(scr)


def menu():

    res = curses.wrapper(initMenu)
    return res
def opcoes():
    res = curses.wrapper(initOpcoes)
    return res
def gPointer(n):

    num = POINTER
    point_array = []
    for i in range(n):
        point_array.append(num)
        num += 12
    return point_array
def getELEMNT(n):

    count = len(ELEMNT)
    simbolos = ""
    for i in range(int(n)):
        simbolos += ELEMNT[random.randint(0, count - 1)]
    return simbolos
def f_senhas():

    senha_array = []

    with open(os.path.join(dir, "pass")) as senha_ln:
        for line in senha_ln:
            if not line.strip():
                senha_array.append([])
            elif len(senha_array) > 0:
                senha_array[len(senha_array) - 1].append(line[:-1])

    senhas = senha_array[random.randint(0, len(senha_array) - 1)]

    random.shuffle(senhas)
    return senhas
def SCREENF(length, senhas):

    tela = getELEMNT(length)

    senhaLen = len(senhas[0])
    senhaCount = len(senhas)
    i = 0
    for senha in senhas:
        maxSkip = int(length / senhaCount - senhaLen)
        i += random.randint(maxSkip - 2, maxSkip)
        tela = tela[:i] + senha + tela[i + senhaLen:]
        i += senhaLen
    return tela
def sInit(scr):

    tTamanho = scr.getmaxyx()
    altura = tTamanho[0]
    largura = tTamanho[1]
    tAltura = altura - LINHAS_HD

    pCols = gPointer(tAltura * 2)

    coluna1 = pCols[:tAltura]
    coluna2 = pCols[tAltura:]

    tQuant = largura / 2 * tAltura
    senhas = f_senhas()
    tela = SCREENF(tQuant, senhas)
    tCol1, tCol2 = tela[0:len(tela) // 2], tela[len(tela) // 2:]

    tLargura = int(largura / 4)

    typeT(scr, '\n\n' + LOGIN_TXT)
    typeT(scr, '\n\n\nSTATUS:ONLINE\nMACHINE_DATA:'+ platform.system() +' '+ platform.release() +'\nCURRENT_USER:'+socket.gethostname()+'\n\nPROTOCOL 21F25532.... ACTIVATED.\nSYSTEM BREACH DETECTED... 0X94EF8C.\n「荒坂の端末」\n\n')

    typeT(scr, '\n\n\n\n')
    typeT(scr, '                                                                             SEQUENCE REQUIRED TO ACCESS: \n')
    typeT(scr, '\n\n')
    typeT(scr, '                                    -' + '---------------' + '\n')
    for i in range(len(senhas)):
      
       typeT(scr, '                                 | ' + senhas[i] + '  | \n')
    typeT(scr, '                                    -' + '---------------' + '\n')

   

    scr.refresh()

    return senhas
def mvPad(scr, keypad):

    tTamanho = scr.getmaxyx()
    altura = tTamanho[0] - 6
    largura = tTamanho[1]

    keypad.addstr('\n>')

    cursorPos = keypad.getyx()

    keypad.refresh(0, 0, int(altura - cursorPos[0] - 1),
                   int(largura / 2 + NUMCHARS), int(altura - 1),
                   int(largura - 1))
def userPad(scr, senhas):

    tTamanho = scr.getmaxyx()
    altura = tTamanho[0] - 6
    largura = tTamanho[1]

    keypad = curses.newpad(altura, int(largura / 2 + NUMCHARS))

    tentativas = TENTATIVAS_MAX

    senha = senhas[random.randint(0, len(senhas) - 1)]
    senhaHack = '[/ADMIN.F PASS]'

    curses.noecho()

    while tentativas > 0:
        scr.move(int(altura - 1), int(largura / 2 + NUMCHARS + 1))

        mvPad(scr, keypad)

        guess = cap_string(scr, False, False)
        cursorPos = keypad.getyx()

        keypad.move(cursorPos[0] - 1, cursorPos[1] - 1)

        if guess.upper() == senhaHack.upper():
            thread = Thread(target=playKey)
            thread.start()
            keypad.addstr('>' + senha + '\n')
            playsound(os.path.join(dir, "audio/beep.wav"))
            continue

        elif guess.upper() == senha.upper():
            thread = Thread(target=playKey)
            thread.start()
            keypad.addstr('>完璧にマッチ!\n')
            keypad.addstr('>システムにアクセス\n')
            keypad.addstr('>するまで\n')
            keypad.addstr('>お待ちください.\n')
            mvPad(scr, keypad)
            playsound(os.path.join(dir, "audio/correctpass.wav"))
            curses.napms(LOGIN_PAUSE)

            return senha

        else:

            thread = Thread(target=playKey)
            thread.start()
            senhaLen = len(senha)

            keypad.addstr('>ACCESS DENIED!\n\n')

            thread = Thread(target=playError)
            thread.start()

        tentativas -= 1
        scr.move(SQUARE_Y, 0)
        scr.move(SQUARE_Y, SQUARE_X)
        scr.addstr(str(tentativas) + ' BREACHES LEFT:  ' )
        for i in range(TENTATIVAS_MAX):
            if i < tentativas:
                scr.addch(curses.ACS_BLOCK)
            else:
                scr.addstr(' ')
            scr.addstr(' ')

    # Out of tentativas
    return None
def login_menu(scr):

    curses.use_default_colors()
    tTamanho = scr.getmaxyx()
    largura = tTamanho[1]
    altura = tTamanho[0]
    random.seed()
    scr.erase()
    scr.move(0, 0)
    senhas = sInit(scr)
    return userPad(scr, senhas)
def login():

    return curses.wrapper(login_menu)
def initLock(scr):
    """
    Start the locked out portion of the terminal
    """
    curses.use_default_colors()
    tTamanho = scr.getmaxyx()
    largura = tTamanho[1]
    altura = tTamanho[0]
    scr.erase()
    curses.curs_set(0)
    scr.move(int(altura / 2 - 1), 0)
    os.system("cat " + os.path.join(dir, 'banner') + "| pv -qL 10000 " )
    scr.move(int(altura / 2 + 1), 0)
    centr(scr, '__!SYSTEM FA_ILUR_E 0x9f37c')
    scr.refresh()
    curses.napms(BLOQUEIO)
def bloquearTela():
    """
    Initialize curses and start the locked out process
    """
    curses.wrapper(initLock)
def initBoot():

    os.system("cat " + os.path.join(dir, 'arasaka') + "| pv -qL 10000 " )
    # time.sleep(5)
    os.system("cat " + os.path.join(dir, 'arasaka_space') + "| pv -qL 10000 " )
    return True
    res = curses.wrapper(initLogin)
    return res
def iniciar():
    
    return initBoot()
def initLogin(scr, username, password):

    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)

    curses.noecho()
    scr.scrollok(True)

    typeT(scr, LOGIN_TXT + '\n\n')

    typeT(scr, '> ')
    curses.napms(Ipausa)
    typeT(scr, LOGIN_USER + username.upper() + '\n', delay)

    typeT(scr, '\n' + LOGIN_PASS + '\n\n')

    typeT(scr, '> ')
    curses.napms(Ipausa)
    password_stars = mascara * len(password)
    typeT(scr, password_stars + '\n', delay)

    curses.napms(500)
Lpausa = 3
Ipausa = 50  
delay = 40
mascara = '*'
novaLinha = 10
def playBeep():
    playsound(os.path.join(dir, "audio/beep.wav"))
def playError():
    playsound(os.path.join(dir, "audio/wrongpass.wav"))
def playKey():
    playsound(os.path.join(dir, "audio/keyenter.wav"))
def typeT(window, text, pause=Lpausa):

    thread = Thread(target=playBeep)
    thread.start()
 
    for i in range(len(text)):
        window.addstr(text[i])
        window.refresh()
        curses.napms(pause)



''
def cap_string(window, hidden=False, can_novaLinha=True):

    keyInput = 0
    def_string = ''
    try:
        while keyInput != novaLinha:
            keyInput = window.getch()
            if keyInput > 96 and keyInput < 123:
                keyInput -= 32
            if keyInput == ord('\b'):
                if len(def_string) > 0:
                    def_string = def_string[:-1]
                    cur = window.getyx()
                    window.move(cur[0], cur[1] - 1)
                    window.clrtobot()
                else:
                    continue
            elif keyInput > 255:
                continue
            elif keyInput != novaLinha:
                def_string += chr(keyInput)
                if hidden:
                    window.addch(mascara)
                else:
                    window.addch(keyInput)
            elif can_novaLinha:
                window.addch(novaLinha)
        return def_string

    except ValueError:
        # We might have Unicode chars in here, let's use unichr instead
        login()


def centr(window, text, pause=Lpausa):

    largura = window.getmaxyx()[1]
    window.move(window.getyx()[0], int(largura / 2 - len(text) / 2))
    typeT(window, text, pause)


if __name__ == '__main__':
    globals()[sys.argv[1]]()
