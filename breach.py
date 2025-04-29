import subprocess
import tempfile
import sys
import curses
import time
import random
import os
import socket
import signal
import platform
import psutil
from threading import Thread
import uuid

Lpausa = 3
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
    centr(scr, 'C0NNECTION_TERMINATED__!\nSYSTEM_FAILURE [0x9F37C] //\n\n')
    centr(scr, 'ERROR CODE: 0x5A_X12T | TRACE DETECTED!!\n')    
    scr.refresh()
    curses.napms(BLOQUEIO)
def get_mac_address():
    mac = uuid.getnode()
    mac_addr = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
    return mac_addr

def get_cpu_usage():
    return f"{psutil.cpu_percent()}%" if psutil else "UNKNOWN"

def get_memory_usage():
    if psutil:
        memory = psutil.virtual_memory()
        return f"{memory.percent}% USED"
    else:
        return "UNKNOWN"

def get_disk_usage():
    if psutil:
        disk = psutil.disk_usage('/')
        return f"{disk.percent}% FULL"
    else:
        return "UNKNOWN"

Ipausa = 50  
delay = 40
mascara = '*'
# boot
TXT1 = 'SECURITY RESET... '
TXT2 = 'WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK'
TXT3 = 'SET TERMINAL/INQUIRE'
TXT4 = 'RIT-V300'
TXT5 = 'SET FILE/PROTECTION=OWNER:RWED ACCOUNTS.F'
TXT6 = 'SET HALT RESTART/MAIN'

# menu de selecao
MENU_HEAD = ('ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM',
             'COPYRIGHT 2075-2077 ROBCO INDUSTRIES', '- SERVER 6 -', '')

MENU_HEAD2 = ('      SoftLock Solutions, Inc\n'
              '"Your Security is Our Security"',
              '>\\ Welcome, ' + socket.gethostname(), '')

MENUDK = [
    'RETURN',
    'STATUS',
    'START OVERSEER NETWORK',
    'AUTOWIPE',
    'START ON BOOT',
    'LOCAL ROBCO IP',
    'CHANGE NETWORK IDENTITY',
    'CHANGE ROBCO CHIPSET MAC',
    'RESTORE ROBCO CHIPSET MAC',
]

MENU1 = [
    'TERMINAL LINK',
    'JOURNAL',
    'VAULT TOOLS',
    'SYSTEM TUNING',
    'SECURE EXIT',
    'CORE RESTART',
    'POWER OFF'
]

MENU_SERVICES = [
    'RETURN',
    'START OVERSEER NETWORK',
    'START ROBCO SERVER',
    'START CRYPTBASE',
    'START RADNET',
    'START VAULTSEC UFW'
]
icon_top = " ╔═╗╔═╗ "
icon_bot = " ╚═╣╠═╝ "

MENU_OPTIONS  = [
    'RETURN',
    'UPDATE VAULT',
    'KEYALIGN',
    'VAULT STATUS',
    'OVERSEER EYE',
    'NETCORE',
    'RADSWEEP',
    'PIPSNIFF',
    'NAMEFORGE',
    'CRONSTART',
    'CRONWATCH'
]

# pagina de login
LOGIN_TXT = 'ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL'
NUMCHARS = 16
SQUARE_X = 19
SQUARE_Y = 3
TENTATIVAS_MAX = 4
LINHAS_HD = 5
LOGIN_PAUSE = 1000
POINTER = 0xf650
ELEMNT = '!@#$%^*()_-+={}[]|\\:;\'",<>./?'
LOGIN_TXT = '// NET::TECH SYSTEM INTERFACE v2.7\n// BOOT_SEQUENCE_INITIATED\n// ACCESS_REQUEST\n\n'
LOGIN_PASS = 'ENTER PASSWORD NOW'
LOGIN_ERROR = 'INCORRECT PASSWORD, PLEASE TRY AGAIN'
LOGIN_USER = 'LOGON '

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
    pathss = os.path.join(home_dir, ".boot", "pass")
    with open(pathss) as senha_ln:
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

# tela bloqueada
LOCK_TXT1 = 'TERMINAL LOCKED'
LOCK_TXT2 = 'PLEASE CONTACT AN ADMINISTRATOR'
LOCK_TXT3 = '! SECURITY BYPASS ATTEMPT DETECTED !'
BLOQUEIO = 10000000
novaLinha = ord('\n')

novaLinha = 10

# Assume helper functions audio, playKey, playError, cap_string, typeT, centr, f_senhas, gPointer, SCREENF, userPad etc. are defined elsewhere
dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # pega o diretorio do arquivo
home_dir = os.environ["HOME"]

def expand_home(path):
    return os.path.expanduser(path)

def audio(filepath, repeats=1):
    os.system(f"ffplay -nodisp -autoexit -loop {repeats} {filepath} > /dev/null 2>&1 &")

def playBeep():
    audio(expand_home("~/.boot/audio/beep.wav"))

def playError():
    audio(expand_home("~/.boot/audio/wrongpass.wav"))

def playKey():
    audio(expand_home("~/.boot/audio/keyenter.wav"))



# --- Helper Function Implementation ---
def typeT(window, text, pause=Lpausa):

    thread = Thread(target=playBeep)
    thread.start()

    for i in range(len(text)):
        window.addstr(text[i])
        window.refresh()
        curses.napms(pause)

def centr(window, text, pause=Lpausa):

    largura = window.getmaxyx()[1]
    window.move(window.getyx()[0], int(largura / 2 - len(text) / 2))
    typeT(window, text, pause)

def get_mac_address():
    """Return the MAC address of the primary network interface."""
    node = uuid.getnode()
    mac = ':'.join(f"{(node >> ele) & 0xff:02x}" for ele in range(0, 8*6, 8)[::-1])
    return mac.upper()

# --- Breach Protocol Game Functions ---

GRID_SIZE = 6
ATTEMPTS_ALLOWED = 3
PICKS_PER_ATTEMPT = 8
REFERENCE_LEN = 4

def generate_grid(n):
    return [[f"{random.choice('0123456789ABCDEF')}{random.choice('0123456789ABCDEF')}" \
             for _ in range(n)] for _ in range(n)]

def pick_reference_positions(n, length):
    path, visited = [], set()
    r, c = random.randrange(n), random.randrange(n)
    path.append((r, c)); visited.add((r, c))
    for step in range(1, length):
        axis = 'col' if step % 2 else 'row'
        if axis == 'col':
            candidates = [(rr, c) for rr in range(n) if (rr, c) not in visited]
        else:
            candidates = [(r, cc) for cc in range(n) if (r, cc) not in visited]
        pos = random.choice(candidates); path.append(pos); visited.add(pos)
    return path


def make_new_grid_with_ref(n, ref_positions):
    grid = generate_grid(n); ref_codes = []
    for (r, c) in ref_positions:
        code = f"{random.choice('0123456789ABCDEF')}{random.choice('0123456789ABCDEF')}"
        grid[r][c] = code; ref_codes.append(code)
    return grid, ref_codes

def get_axis(prev, step):
    if step == 0: return None
    return 'col' if step % 2 else 'row'


def get_valid_picks(prev, step, visited):
    axis = get_axis(prev, step); n = GRID_SIZE
    if axis is None:
        return {(r, c) for r in range(n) for c in range(n) if (r, c) not in visited}
    r0, c0 = prev
    if axis == 'col': return {(r, c0) for r in range(n) if (r, c0) not in visited}
    return {(r0, c) for c in range(n) if (r0, c) not in visited}

def draw_single_box(scr, y, x, h, w, title=None):
    scr.addstr(y, x, '┌' + '─'*(w-2) + '┐')
    for i in range(1, h-1): scr.addstr(y+i, x, '│'); scr.addstr(y+i, x+w-1, '│')
    scr.addstr(y+h-1, x, '└' + '─'*(w-2) + '┘')
    if title: scr.addstr(y, x+2, f' {title} ')


def draw_double_box(scr, y, x, h, w, title=None):
    scr.addstr(y, x, '╔' + '═'*(w-2) + '╗')
    for i in range(1, h-1): scr.addstr(y+i, x, '║'); scr.addstr(y+i, x+w-1, '║')
    scr.addstr(y+h-1, x, '╚' + '═'*(w-2) + '╝')
    if title: scr.addstr(y, x+2, f' {title} ')


def run_breach(scr):
    curses.curs_set(0)
    attempts = ATTEMPTS_ALLOWED; success = False
    ref_positions = pick_reference_positions(GRID_SIZE, REFERENCE_LEN)
    while attempts > 0 and not success:
        grid, reference = make_new_grid_with_ref(GRID_SIZE, ref_positions)
        picks, visited = [], set(); cursor = ref_positions[0]
        while len(picks) < PICKS_PER_ATTEMPT:
            draw_game(scr, grid, cursor, picks, attempts, reference)
            key = scr.getch(); r,c = cursor; axis = get_axis(picks[-1] if picks else None, len(picks))
            def can_move(nr,nc): return axis is None or ((axis=='col' and nc==c) or (axis=='row' and nr==r))
            nr,nc = r,c
            if key in (curses.KEY_UP,ord('k')): nr = max(0,r-1)
            elif key in (curses.KEY_DOWN,ord('j')): nr = min(GRID_SIZE-1,r+1)
            elif key in (curses.KEY_LEFT,ord('h')): nc = max(0,c-1)
            elif key in (curses.KEY_RIGHT,ord('l')): nc = min(GRID_SIZE-1,c+1)
            elif key in (10,13):
                valid = get_valid_picks(picks[-1] if picks else None, len(picks), visited)
                if cursor in valid: picks.append(cursor); visited.add(cursor)
                else: curses.flash()
                continue
            elif key in (ord('q'), ord('Q')): return False
            if can_move(nr,nc): cursor = (nr,nc)
            else: curses.flash()
        picked = {grid[r][c] for r,c in picks}
        if all(b in picked for b in reference): success = True
        else: attempts -= 1
    draw_game(scr, grid, cursor, picks, attempts, reference)
    if success:
        h, w = scr.getmaxyx()
        gw = GRID_SIZE * 5 + 2
        gh = GRID_SIZE * 2 + 2
        sy, sx = max(2, (h - gh) // 2), max(2, (w - gw - 60) // 2)
        for r in range(GRID_SIZE * 2 + 2): scr.addstr(sy + r, sx, ' ' * (gw - 2))
        typeT(scr, '\n\n\n\n\n\nBREACH PROTOCOL SUCCESS! CONTINUING...')
        typeT(scr, '> ::: ENGAGING PROTOCOL//0xC0D3\n')
        typeT(scr, '> :: INITIATING_NET_OVERRIDE //\n')
        typeT(scr, '> ==>> UPLINK STABILIZED [███░░]\n')
        typeT(scr, '> >>> ROOT_NODE_ACCESS//GRANTED\n')
        time.sleep(5)
    else:
        typeT(scr, '\nBREACH PROTOCOL FAILED! ACCESS DENIED')
    scr.refresh()
    time.sleep(1)
    return success

def draw_game(scr, grid, cursor, picks, attempts, reference):
    h,w = scr.getmaxyx()
    gw = GRID_SIZE*5+2; gh=GRID_SIZE*2+2
    iw = max(60,REFERENCE_LEN*6+PICKS_PER_ATTEMPT*4); ih = PICKS_PER_ATTEMPT+8
    sy, sx = max(2,(h-gh)//2), max(2,(w-gw-iw-6)//2)
    scr.addstr(sy-2, sx, "NET::TECH PROTOCOL", curses.A_BOLD)
    scr.addstr(sy-1, sx, "// TERMINAL_ST", curses.A_BOLD)
    draw_single_box(scr, sy, sx, gh, gw, " GRID ")
    ix = sx+gw+4; draw_double_box(scr, sy, ix, ih, iw, " PROTOCOL ")
    curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_BLACK,curses.COLOR_GREEN)
    curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    valid = get_valid_picks(picks[-1] if picks else None, len(picks), set(picks))
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            y,x = sy+1+r*2, sx+1+c*5; code=grid[r][c]
            if (r,c)==cursor: attr=curses.color_pair(4)|curses.A_REVERSE|curses.A_BOLD
            elif (r,c) in picks: attr=curses.color_pair(3)|curses.A_BOLD
            elif (r,c) in valid: attr=curses.color_pair(2)|curses.A_UNDERLINE
            else: attr=curses.color_pair(1)
            scr.addstr(y,x,code,attr)
    iy=sy+2; scr.addstr(iy,ix+2,f"[{attempts}]::> ATTEMPTS LEFT")
    slots=[grid[r][c] for r,c in picks]+['__']*(PICKS_PER_ATTEMPT-len(picks))
    scr.addstr(iy + 2, ix + 2, "BUFFER [ " + ' | '.join(slots) + " ]")
    scr.addstr(iy+4,ix+2,">>> SEQUENCE REQUIRED TO UPLOAD:  ")
    sequence = ' '.join(f"[{b}]" for b in reference)
    scr.addstr(iy + 4, ix +2 , f"{sequence:<30}{icon_top}  DATAMINER_V1")
    scr.addstr(iy + 5, ix+32, f"{icon_bot}  // BIND_SHELL")
    # Refresh screen
    scr.refresh()

# --- Integration into Login Flow ---

def login_menu(scr):
    curses.use_default_colors()
    scr = scr
    scr.erase()
    senhas = sInit(scr)
    # return userPad(scr, senhas)


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
    typeT(scr, f"// STATUS: ONLINE\n// MACHINE_INFO: {platform.system()} {platform.release()} ({platform.machine()})\n// CURRENT_USER: {os.getlogin()}\n// HOSTNAME: {socket.gethostname()}\n// IP_ADDRESS: {socket.gethostbyname(socket.gethostname())}\n// MAC_ADDRESS: {get_mac_address()}\n// SYSTEM_TIME_UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n// CPU_USAGE: {get_cpu_usage()}\n// MEMORY_STATUS: {get_memory_usage()}\n// DISK_STATUS: {get_disk_usage()}\n\n// BREACH_PROTOCOL: ACTIVE\n// BREACH_SOURCE: [ARASAKA TERMINAL - 港区, 東京]\n\n// INITIATING PACKET COLLECTION\n>>> COLLECTING_PACKET_1........COMPLETE\n>>> COLLECTING_PACKET_2........COMPLETE\n>>> COLLECTING_PACKET_3........COMPLETE\n>>> COLLECTING_PACKET_4........COMPLETE\n\n// UPLOAD_SEQUENCE\n>>> UPLOAD_IN_PROGRESS\n\n「荒坂インターフェース 」")
    typeT(scr, '')
    # Run breach protocol game here
    success = run_breach(scr)
    if not success:
        typeT(scr, '\nBREACH PROTOCOL FAILED! ACCESS DENIED')
    else:
        scr.clear()
        typeT(scr, '\n\n\n\n\n\nBREACH PROTOCOL SUCCESS! CONTINUING...')
        typeT(scr, '> ::: ENGAGING PROTOCOL//0xC0D3\n')
        typeT(scr, '> :: INITIATING_NET_OVERRIDE //\n')
        typeT(scr,'> ==>> UPLINK STABILIZED [███░░]\n')
        typeT(scr,'> >>> TESTING\n')
    scr.refresh()
    time.sleep(1)
    # After game, return the list of passwords to proceed
    return f_senhas()

# Entry point
if __name__ == '__main__':
    curses.wrapper(login_menu) 
