#! /usr/bin/env python3
# Coded by:
#     /\                                  | |      
#    /  \   _ __ ___ __ _ _ __   __ _  ___| | ___  
#   / /\ \ | '__/ __/ _` | '_ \ / _` |/ _ \ |/ _ \ 
#  / ____ \| | | (_| (_| | | | | (_| |  __/ | (_) |
# /_/    \_\_|  \___\__,_|_| |_|\__, |\___|_|\___/ 
#                                __/ |             
   
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


# funcao para lidar co m interrupcoes do teclado
def handler(signum, frame):
    pass

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTSTP, handler)

# -------------------- VARIAVEIS GERAIS --------------------------

dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # pega o diretorio do arquivo

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

# tela bloqueada
LOCK_TXT1 = 'TERMINAL LOCKED'
LOCK_TXT2 = 'PLEASE CONTACT AN ADMINISTRATOR'
LOCK_TXT3 = '! SECURITY BYPASS ATTEMPT DETECTED !'
BLOQUEIO = 10000000

novaLinha = ord('\n')


# ----------- funcoes --------------------

def audio(filepath, repeats=1):
    os.system(f"ffplay -nodisp -autoexit -loop {repeats} {filepath} > /dev/null 2>&1 &")

        
def checkPS(processName):
    '''
    Funcao para checar se servicos estao em execucao
    '''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False


def editHost():
    subprocess.run("sudo vim /etc/hostname", shell=True)
def createCron():
    os.environ['EDITOR'] = 'micro'
    subprocess.run("crontab -e", shell=True)
def getNetstat():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write("[+] Fetching netstat/ss output...\n")
        try:
            result = subprocess.check_output("netstat -tulpn || ss -tulpn", shell=True, stderr=subprocess.DEVNULL).decode()
            tmp.write(result + "\n")
        except subprocess.CalledProcessError:
            tmp.write("[-] Failed to retrieve netstat/ss output.\n")
        tmp_path = tmp.name
    subprocess.run(f"vim {tmp_path}", shell=True)
    os.remove(tmp_path)

def getCrons():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write("[+] Fetching crontab and system-wide cron jobs...\n")
        try:
            result = subprocess.check_output("crontab -l && ls /etc/cron.*", shell=True, stderr=subprocess.DEVNULL).decode()
            tmp.write(result + "\n")
        except subprocess.CalledProcessError:
            tmp.write("[-] Failed to retrieve crontab and cron job output.\n")
        tmp_path = tmp.name
    subprocess.run(f"vim {tmp_path}", shell=True)
    os.remove(tmp_path)
def monitor():
    try:
        curses.endwin()
    except:
        pass
    try:
        subprocess.run(['htop'])
    except KeyboardInterrupt:
        pass
    try:
        curses.doupdate()
    except:
        pass
def check_tor_running():
    try:
        # Use pgrep to check if tor process exists
        result = subprocess.run(['pgrep', '-x', 'tor'], capture_output=True, text=True)
        if result.stdout.strip():
            return True
        else:
            return False
    except Exception:
        return False

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


def checkNet():
    try:
        result = subprocess.run(['sudo', 'torctl', 'status'], capture_output=True, text=True, check=True)
        output = result.stdout.lower()
        # If output contains "torctl is stopped" or "tor service is: inactive", consider not running
        if "torctl is stopped" in output or "tor service is: inactive" in output:
            return False
        return True
    except subprocess.CalledProcessError:
        # If command fails, assume not running
        return False


def keyboardModelLayout():
    subprocess.run("sudo dpkg-reconfigure keyboard-configuration", shell=True)
def getNmtui():
    subprocess.run("nmtui", shell=True)
def vaultpeek():
    try:
        curses.endwin()
    except Exception:
        pass
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        def run(cmd, label=None):
            tmp.write(f"\n==> {label or cmd}\n")
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode()
                tmp.write(result + "\n")
            except subprocess.CalledProcessError:
                tmp.write("[-] Failed or no output.\n")

        tmp.write("[+] VAULTPEEK SYSTEM ENUMERATION INITIALIZED...\n")

        run("uname -a", "System Info")
        run("cat /etc/os-release", "OS Release")
        run("hostnamectl", "Hostname Info")
        run("timedatectl", "System Time")
        run("whoami", "Current User")
        run("id", "User ID Info")
        run("w", "Logged-in Users")
        run("lastlog | grep -v 'Never'", "Login History")
        run("cat /etc/passwd", "User List (/etc/passwd)")
        run("cat /etc/group", "Groups")
        run("sudo -l", "Sudo Privileges")
        run("echo $PATH", "PATH Variable")
        run("ip a", "Interfaces")
        run("ip route", "Routing Table")
        run("cat /etc/resolv.conf", "DNS Resolver")
        run("ss -tuln", "Open Ports (ss)")
        run("find / -type f -perm -04000 -ls 2>/dev/null", "SUID Files")
        run("find / -type f -perm -02000 -ls 2>/dev/null", "SGID Files")
        run("find / -type f -perm -0002 -exec ls -l {} + 2>/dev/null | grep -v '/proc'", "World-Writable Files")
        run("find /home /root -name '*.bash_history' -o -name 'id_rsa' -o -name 'authorized_keys' 2>/dev/null", "Credential Artifacts")
        run("find / -name '*.conf' -o -name '*.bak' -o -name '*.old' 2>/dev/null", "Config, Backup, Old Files")
        run("crontab -l", "Current User Cron")
        run("ls -alh /etc/cron* /var/spool/cron 2>/dev/null", "System-wide Crons")
        run("ps aux --sort=-%mem | head -n 15", "Top Memory-Heavy Processes")
        run("systemctl list-units --type=service --state=running", "Running Systemd Services")
        run("lsmod", "Kernel Modules")
        run("dpkg -l | grep '^ii' | awk '{print $2}' | head -n 20 || rpm -qa | head -n 20", "Installed Packages")
        run("env", "Environment Variables")
        run("ls -al /root /home 2>/dev/null", "Root/Home Directory Listings")

        tmp.write("\n[+] VAULTPEEK COMPLETE.\n")
        tmp.flush()
        tmp_path = tmp.name
    subprocess.run(f"less +G {tmp_path}", shell=True)
    os.remove(tmp_path)
    try:
        stdscr = curses.initscr()
        curses.cbreak()
        stdscr.keypad(True)
    except Exception:
        pass

def lock_screen():
    try:
        if os.path.exists('/usr/bin/gdbus'):
            subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.gnome.ScreenSaver', '--object-path', '/org/gnome/ScreenSaver', '--method', 'org.gnome.ScreenSaver.Lock'])
            return
        elif os.path.exists('/usr/bin/qdbus'):
            subprocess.run(['qdbus', 'org.kde.screensaver', '/ScreenSaver', 'Lock'])
            return
        elif os.path.exists('/usr/bin/xdg-screensaver'):
            subprocess.run(['xdg-screensaver', 'lock'])
            return
        elif os.path.exists('/usr/bin/gnome-screensaver-command'):
            subprocess.run(['gnome-screensaver-command', '--lock'])
            return
        elif os.path.exists('/usr/bin/i3lock'):
            subprocess.run(['i3lock'])
            return
        else:
            print("/.F==: NO LOCKER DEFINED FOR VAULT TERMINAL")
    
    except Exception as e:
        print(f"Journal Entry:\n AN ERROR HAS OCURRED==: {e}")






###### RENDERING FUNCTIONS NOW BELOW




def menuOptions(scr):

    keyInput = 0
    selection = 0
    selection_count = len(MENU_OPTIONS)
    selection_start_y = scr.getyx()[0]
    largura = scr.getmaxyx()[1]

    while keyInput != novaLinha:
        scr.move(selection_start_y, 0)
        line = 0
        for sel in MENU_OPTIONS:
            whole_line = '> ' + MENU_OPTIONS[line]
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

            scr.erase()
            menu()

        elif keyInput == ord('\n') and selection == 1:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nUPDATING VAULT SHELL. . . ")
            time.sleep(2)
            os.system('sudo apt update && sudo apt-get upgrade')
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 2:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nROBCO KEYMAPPING CONFIGURATION. . . ")
            time.sleep(2)
            keyboardModelLayout()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 3:  
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nGETTING VAULTPEEK MODULE. . . ")
            vaultpeek()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 4:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nLOADING OVERSEER EYE. . . ")
            time.sleep(2)
            monitor()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 5:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nLOADING NETCORE. . . ")
            time.sleep(2)
            getNmtui()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 6:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nCLEARING ROBCO TEMPORARY LOGS AND FILES. . . ")
            time.sleep(2)
            os.system('sudo apt-get autoremove -y && sudo apt-get clean && sudo apt-get autoclean -y && sudo rm -rf /tmp/* /var/tmp/* /var/cache/apt/archives/* /var/log/*.log && sudo journalctl --vacuum-time=7d')
            print("\n\nALL TEMPORARY DATA DELETED!")
            time.sleep(5)
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 7:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nLOADING PIPSNIFF 3000 ")
            time.sleep(2)
            getNetstat()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 8:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nUPDATING NAMEFORGE . . . ")
            time.sleep(2)
            editHost()
            scr.erase()
            options()


        elif keyInput == ord('\n') and selection == 9:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nSETTING CRONSTART INIT . . . ")
            time.sleep(2)
            createCron()
            scr.erase()
            options()


        elif keyInput == ord('\n') and selection == 10:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nOPENING CRONWATCH . . . ")
            time.sleep(2)
            getCrons()
            scr.erase()
            options()



def menuServicos(scr):

    keyInput = 0
    selection = 0
    selection_count = len(MENU_SERVICES)
    selection_start_y = scr.getyx()[0]
    largura = scr.getmaxyx()[1]

    if checkNet():
        MENU_SERVICES[1] = "OVERSEER NETWORK [RUNNING]"
    else:
        MENU_SERVICES[1] = "OVERSEER NETWORK [INACTIVE]"


    if checkPS('apache2'):
        MENU_SERVICES[2] = "STOP ROBCO SERVER"
    else:
        MENU_SERVICES[2] = "START ROBCO SERVER"

    if checkPS('mariadb' or 'mysqld'):
        MENU_SERVICES[3] = "STOP CRYPTBASE"
    else:
        MENU_SERVICES[3] = "START CRYPTBASE"

    if check_tor_running():
        MENU_SERVICES[4] = "STOP RADNET"
    else:
        MENU_SERVICES[4] = "START RADNET"

    if checkPS('ufw'):
        MENU_SERVICES[5] = "STOP VAULTSEC UFW"
    else:
        MENU_SERVICES[5] = "START VAULTSEC UFW"

    while keyInput != novaLinha:
        scr.move(selection_start_y, 0)
        line = 0
        for sel in MENU_SERVICES:
            whole_line = '> ' + MENU_SERVICES[line]
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
            audio(os.path.join(dir, "audio/keyenter.wav"))
            scr.erase()
            menu()

        elif keyInput == ord('\n') and selection == 1:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            scr.erase()
            darknet()

        elif keyInput == ord('\n') and selection == 2:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            if checkPS('apache2'):
                print("\n\nSTOPPING ROBCO SERVER. . . ")
                time.sleep(2)
                os.system('sudo service apache2 stop')
                scr.erase()
                servicos()
            else:
                print("\n\nSTARTING ROBCO SERVER. . . ")
                time.sleep(2)
                os.system('sudo service apache2 start')
                scr.erase()
                servicos()

        elif keyInput == ord('\n') and selection == 3:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            if checkPS('mariadb') or checkPS('mysql'):
                print("\n\nSTOPPING CRYPTBASE. . . ")
                time.sleep(2)
                os.system('sudo service mysql stop || sudo service mariadb stop')
                scr.erase()
                servicos()
            else:
                print("\n\nSTARTING CRYPTBASE. . . ")
                time.sleep(2)
                os.system('sudo service mysql start || sudo service mariadb start')
                scr.erase()
                servicos()
        elif keyInput == ord('\n') and selection == 4:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            if checkPS('tor'):
                print("\n\nSTOPPING RADNET. . . ")
                time.sleep(2)
                os.system('sudo pkill tor')
                scr.erase()
                servicos()
            else:
                print("\n\nSTARTING RADNET. . . ")
                time.sleep(2)
                os.system('tor &')
                scr.erase()
                servicos()

        elif keyInput == ord('\n') and selection == 5:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            if checkPS('ufw'):

                print("\n\nSTOPPING VAULTSEC UFW")
                time.sleep(2)
                os.system('service ufw stop')
                scr.erase()
                servicos()
            else:
                print("\n\nSTARTING VAULTSEC UFW")
                time.sleep(2)
                os.system('service ufw start')
                scr.erase()
                servicos()
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
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\n\n/.F==: ACCESSING VAULT TERMINAL. . .")

            time.sleep(2)
            os.system('cd $HOME')
            os.system('tmux')

        elif keyInput == ord('\n') and selection == 1:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\n\nVault 138\n Journal entry:")


            time.sleep(2)

            print(os.system('journalctl'))

            exit = scr.getch()
            if exit == ord('\n'):
                scr.erase()
                menu()
            scr.erase()
            menu()

        elif keyInput == ord('\n') and selection == 2:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            servicos()
        elif keyInput == ord('\n') and selection == 3:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            options()
        elif keyInput == ord('\n') and selection == 4:
            audio(os.path.join(dir, "audio/keyenter.wav"))
               #logout
            lock_screen()
        elif keyInput == ord('\n') and selection == 5:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\n\nREBOOTING ROBCO INDUSTRIES (TM) UNIFIED OPERATIONAL SYSTEM")

            time.sleep(5)
            os.system("sudo shutdown -r now")
        
        elif keyInput == ord('\n') and selection == 6:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\n\nG O O D    B Y E ! ")

            time.sleep(5)
            os.system("sudo shutdown -h now")



def criarDarknet(scr):

    keyInput = 0
    selection = 0
    selection_count = len(MENUDK)
    selection_start_y = scr.getyx()[0]
    largura = scr.getmaxyx()[1]

    while keyInput != novaLinha:
        scr.move(selection_start_y, 0)
        line = 0
        for sel in MENUDK:
            whole_line = '> ' + MENUDK[line]
            space = largura - len(whole_line) % largura + 20
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
            audio(os.path.join(dir, "audio/keyenter.wav"))
            scr.erase()
            servicos()

        if keyInput == ord('\n') and selection == 1:
           print("\n\n- - OVERSEER NETWORK STATUS - -")
           time.sleep(2)
           os.system('sudo torctl status | micro')
           scr.erase()
           darknet()
       
        elif keyInput == ord('\n') and selection == 2:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            if checkNet():
                print("\n\nDISCONNECTING OVERSEER NETWORK. . . ")
                time.sleep(2)
                os.system('sudo torctl stop')
                scr.erase()
                darknet()
            else:
                print("\n\nCONNECTING OVERSEER NETWORK. . . ")
                time.sleep(2)
                os.system('sudo torctl start')
                scr.erase()
                darknet()

        elif keyInput == ord('\n') and selection == 3:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nACTIVATING AUTOWIPE. . . ")
            time.sleep(2)
            os.system('sudo torctl autowipe')
            scr.erase()
            darknet()

        elif keyInput == ord('\n') and selection == 4:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nACTIVATING AUTO START. . . ")
            time.sleep(2)
            os.system('sudo torctl autostart')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 5:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nFETCHING LOCAL TERMINAL COORDINATES. . . ")
            time.sleep(2)
            os.system('sudo torctl ip | micro ')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 6:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nCHANGE OVERSEER NETWORK IDENTITY. . . ")
            time.sleep(2)
            os.system('sudo torctl chngid')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 7:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nCHANGE OVERSEER NETWORK IDENTITY. . . ")
            time.sleep(2)
            os.system('sudo torctl chngid')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 8:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nCHANGING LOCAL ROBCO CHIPSET MAC. . . ")
            time.sleep(2)
            os.system('sudo torctl chngmac')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 9:
            audio(os.path.join(dir, "audio/keyenter.wav"))
            print("\n\nRESTORING LOCAL ROBCO CHIPSET MAC. . . ")
            time.sleep(2)
            os.system('sudo torctl rvmac')
            scr.erase()
            darknet()


def initDarknet(scr):

    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)
    curses.curs_set(0)

    largura = scr.getmaxyx()[1]

    audio(os.path.join(dir, "audio/beep.wav",3))
    for header in MENU_HEAD:
        centr(scr, header + '\n')

    audio(os.path.join(dir, "audio/beep.wav",3))
    for header in MENU_HEAD2:   
        typeT(scr, header + '\n')

    audio(os.path.join(dir, "audio/beep.wav",4))
    for i in range(largura):
        scr.addch(curses.ACS_BSBS)
    scr.refresh()

    return criarDarknet(scr)



def initMenu(scr):

    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)
    curses.curs_set(0)

    largura = scr.getmaxyx()[1]

    audio(os.path.join(dir, "audio/beep.wav",3))
    for header in MENU_HEAD:
        centr(scr, header + '\n')

    audio(os.path.join(dir, "audio/beep.wav",3))
    for header in MENU_HEAD2:   
        typeT(scr, header + '\n')

    audio(os.path.join(dir, "audio/beep.wav",4))
    for i in range(largura):
        scr.addch(curses.ACS_BSBS)
    scr.refresh()

    return criarMenu(scr)



def initOptions(scr):

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

    return menuOptions(scr)




def initServicos(scr):

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

    return menuServicos(scr)


def darknet():

    res = curses.wrapper(initDarknet)
    return res

def menu():

    res = curses.wrapper(initMenu)
    return res



def options():
    res = curses.wrapper(initOptions)
    return res




def servicos():
    res = curses.wrapper(initServicos)
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
    typeT(scr, f"// STATUS: ONLINE\n// MACHINE_INFO: {platform.system()} {platform.release()} ({platform.machine()})\n// CURRENT_USER: {os.getlogin()}\n// HOSTNAME: {socket.gethostname()}\n// IP_ADDRESS: {socket.gethostbyname(socket.gethostname())}\n// MAC_ADDRESS: {get_mac_address()}\n// SYSTEM_TIME_UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n// CPU_USAGE: {get_cpu_usage()}\n// MEMORY_STATUS: {get_memory_usage()}\n// DISK_STATUS: {get_disk_usage()}\n\n// BREACH_PROTOCOL: ACTIVE\n// BREACH_SOURCE: [ARASAKA TERMINAL - 港区, 東京]\n\n// INITIATING PACKET COLLECTION\n>>> COLLECTING_PACKET_1........COMPLETE\n>>> COLLECTING_PACKET_2........COMPLETE\n>>> COLLECTING_PACKET_3........COMPLETE\n>>> COLLECTING_PACKET_4........COMPLETE\n\n// UPLOAD_SEQUENCE\n>>> UPLOAD_IN_PROGRESS\n>>> UPLOAD_COMPLETE\n\n「システム侵入成功」")

    typeT(scr, '\n\n\n\n')
    center(scr, '              SEQUENCE REQUIRED TO ACCESS: \n')
    typeT(scr, '\n\n')
    centr(scr, '---------------' + '\n')
    for i in range(len(senhas)):
       center(scr, '| ' + senhas[i] + ' | \n')
    center(scr, '---------------' + '\n')

   

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
    senhaHack = '.unlock'

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
            audio(os.path.join(dir, "audio/beep.wav"))
            continue

        elif guess.upper() == senha.upper():
            thread = Thread(target=playKey)
            thread.start()
            keypad.addstr('>完璧にマッチ!\n')
            keypad.addstr('>システムにアクセス\n')
            keypad.addstr('>するまで\n')
            keypad.addstr('>お待ちください.\n')
            mvPad(scr, keypad)
            audio(os.path.join(dir, "audio/correctpass.wav"))
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
    audio(os.path.join(dir, "audio/beep.wav"))
def playError():
    audio(os.path.join(dir, "audio/wrongpass.wav"))
def playKey():
    audio(os.path.join(dir, "audio/keyenter.wav"))
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
