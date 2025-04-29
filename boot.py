#! /usr/bin/env python3
# Coded by:
#     /\                                  | |      
#    /  \   _ __ ___ __ _ _ __   __ _  ___| | ___  
#   / /\ \ | '__/ __/ _` | '_ \ / _` |/ _ \ |/ _ \ 
#  / ____ \| | | (_| (_| | | | | (_| |  __/ | (_) |
# /_/    \_\_|  \___\__,_|_| |_|\__, |\___|_|\___/ 
#                                __/ |             
import string
import subprocess
import tempfile
import sys
import curses
import time
import random
import os
import sys
import socket
import signal
import platform
import psutil
import wifi
from threading import Thread
import uuid
from datetime import datetime
import re
import json

# AVOID EXITTING SCRIPT
def handler(signum, frame):
    pass
   
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTSTP, handler)

# .................DIR.FUNCTIONS............................
dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # pega o diretorio do arquivo
home_dir = os.environ["HOME"]
def expand_home(path):
    return os.path.expanduser(path)
# ..................-------------------......................


# BREACH LOGIN ....................................
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
    attempts = ATTEMPTS_ALLOWED
    success = False
    ref_positions = pick_reference_positions(GRID_SIZE, REFERENCE_LEN)

    while attempts > 0 and not success:
        grid, reference = make_new_grid_with_ref(GRID_SIZE, ref_positions)
        picks, visited = [], set()
        cursor = ref_positions[0]

        while len(picks) < PICKS_PER_ATTEMPT:
            draw_game(scr, grid, cursor, picks, attempts, reference)
            key = scr.getch()

            if key == curses.KEY_F3:
                success = True
                break

            r, c = cursor
            axis = get_axis(picks[-1] if picks else None, len(picks))

            def can_move(nr, nc):
                return axis is None or ((axis == 'col' and nc == c) or (axis == 'row' and nr == r))

            nr, nc = r, c
            if key in (curses.KEY_UP, ord('k')): nr = max(0, r - 1)
            elif key in (curses.KEY_DOWN, ord('j')): nr = min(GRID_SIZE - 1, r + 1)
            elif key in (curses.KEY_LEFT, ord('h')): nc = max(0, c - 1)
            elif key in (curses.KEY_RIGHT, ord('l')): nc = min(GRID_SIZE - 1, c + 1)
            elif key in (10, 13):
                valid = get_valid_picks(picks[-1] if picks else None, len(picks), visited)
                if cursor in valid: picks.append(cursor); visited.add(cursor)
                else: curses.flash()
                continue
            elif key in (ord('q'), ord('Q')): return False
            if can_move(nr, nc): cursor = (nr, nc)
            else: curses.flash()

        picked = {grid[r][c] for r, c in picks}
        if all(b in picked for b in reference): success = True
        else: attempts -= 1

    draw_game(scr, grid, cursor, picks, attempts, reference)

    if success:
        h, w = scr.getmaxyx()
        gw = GRID_SIZE * 5 + 2
        gh = GRID_SIZE * 2 + 2
        sy, sx = max(2, (h - gh) // 2), max(2, (w - gw - 60) // 2)
        for r in range(GRID_SIZE * 2 + 2): scr.addstr(sy + r, sx, ' ' * (gw - 2))
        scr.clear()
        typeT(scr, '\n\n\n\n\n\n//// NETRUNNER_V3.1 BREACH PROTOCOL RUNNING\n')
        typeT(scr, '> ::: ENGAGING PROTOCOL//0x002D03F\n')
        typeT(scr, '> :: INITIATING_NET_OVERRIDE //\n')
        typeT(scr, '> ==>> NETVH_UPLOADED [███░░]\n')
        typeT(scr, '> >>> ROOT_NODE_ACCESS//GRANTED\n')
    else:
        bloquearTela()
    scr.refresh()
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
def shutdown_program(stdscr):
    curses.endwin()  
    sys.exit() 


#................TEXTS............................
icon_top = " ╔═╗╔═╗ "
icon_bot = " ╚═╣╠═╝ "



import socket
import subprocess
import psutil
import platform
import random
import string
import uuid
import os
from datetime import datetime
import time


def get_kernel_modules():
    try:
        # Run `lsmod` and capture the output
        result = subprocess.check_output("lsmod", shell=True).decode('utf-8')
        # Parse the output, splitting by new lines
        modules = result.splitlines()
        # Extract module names (first column)
        kernel_modules = [line.split()[0] for line in modules[1:]]  # Skip header
        return kernel_modules
    except subprocess.CalledProcessError:
        return []

def get_system_info():
    global HEADEROUTPUT

    def random_user():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def get_dns_servers():
        try:
            with open('/etc/resolv.conf', 'r') as f:
                dns_servers = [line.split()[1] for line in f.readlines() if line.startswith('nameserver')]
            return dns_servers
        except FileNotFoundError:
            return ["[ / ]"]
    def get_scheduled_tasks():
        try:
            cron_jobs = subprocess.check_output("crontab -l", shell=True).decode().splitlines()
            return cron_jobs if cron_jobs else ["No Cron Jobs"]
        except subprocess.CalledProcessError:
            return ["No Cron Jobs"]
    def selinux_status():
        try:
            status = subprocess.check_output("sestatus", shell=True).decode("utf-8")
            if "enabled" in status.lower():
                return "ENABLED"
            elif "disabled" in status.lower():
                return "DISABLED"
            else:
                return "[/]"
        except subprocess.CalledProcessError:
            return "[/]"
    def get_cpu_info():
        try:
            result = subprocess.run(['lscpu'], capture_output=True, text=True)
            if result.returncode == 0:
                info = result.stdout.splitlines()
                cpu_info = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in info}
                return f"{cpu_info.get('Model name', '[/]')} @ {cpu_info.get('CPU MHz', '[/]')} MHz, {cpu_info.get('CPU(s)', '[/]')} Cores"
            return "[/]"
        except:
            return "[/]"
    def get_gpu_info():
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.free,memory.used,driver_version', '--format=csv,noheader,nounits'],
                                    capture_output=True, text=True)
            return result.stdout.strip().replace("\n", ", ") if result.returncode == 0 else "[/]"
        except:
            return "[/]"
    def get_firewall_rules():
        try:
            result = subprocess.check_output(['iptables', '-L'], stderr=subprocess.PIPE)
            return result.decode()
        except subprocess.CalledProcessError:
            return "[ / ]"
    def open_ports():
        try:
            output = subprocess.check_output("ss -tuln", shell=True, text=True)
            ports = set()
            for line in output.splitlines():
                parts = line.split()
                if len(parts) >= 5:
                    address = parts[4]
                    if ":" in address:
                        port = address.rsplit(":", 1)[-1]
                        if port.isdigit():
                            ports.add(port)
            return ", ".join(sorted(ports, key=int))
        except:
            return "[ / ]"
    def get_current_wifi_signal_strength(interface='wlan0'):
        if not os.path.exists(f'/sys/class/net/{interface}'):
            return "[]"
        try:
            networks = wifi.Cell.all(interface)
            if not networks:
                return "NO SIGNAL"
            current_signal_strength = next((network.signal for network in networks if network.encrypted), None)
            if current_signal_strength is not None:
                return current_signal_strength
            else:
                return "NO SIGNAL"
        except wifi.exceptions.InterfaceError:
            return "NO SIGNAL"
    signal = get_current_wifi_signal_strength()
    def get_bssid(interface='wlan0'):
        if not os.path.exists(f'/sys/class/net/{interface}'):
            return "[/]"
        try:
            networks = wifi.Cell.all(interface) 
            if not networks:
                return "NO SIGNAL"  
            current_bssid = next((network.address for network in networks if network.encrypted), None)
            if current_bssid:
                return current_bssid
            else:
                return "NO SIGNAL"  
        except wifi.exceptions.InterfaceError:
            return "NO SIGNAL"  
    def get_channel(interface='wlan0'):
        if not os.path.exists(f'/sys/class/net/{interface}'):
            return "[/]"
        
        try:
            networks = wifi.Cell.all(interface)
            if not networks:
                return "NO SIGNAL"
            
            current_channel = next((network.channel for network in networks if network.encrypted), None)
            if current_channel is not None:
                return current_channel
            else:
                return "NO SIGNAL"
        
        except wifi.exceptions.InterfaceError:
            return "NO SIGNAL"
   
    def get_ssid(interface='wlan0'):
        if not os.path.exists(f'/sys/class/net/{interface}'):
            return "[/]"
        try:
            networks = wifi.Cell.all(interface)  
            if not networks:
                return "NO SIGNAL" 
            current_ssid = next((network.ssid for network in networks if network.encrypted), None)
            if current_ssid:
                return current_ssid
            else:
                return "NO SIGNAL"  #
        except wifi.exceptions.InterfaceError:
            return "NO SIGNAL"  
            
    ip_address = socket.gethostbyname(socket.gethostname())
    public_ip = subprocess.getoutput("curl -s http://checkip.amazonaws.com")
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    hostname = socket.gethostname()
    session_key = f"0x{''.join(random.choices(string.hexdigits, k=4))}-{random_user()}"
    os_info = platform.system() + " " + platform.release()
    kernel_version = platform.uname().release
    architecture = platform.architecture()[0]
    distro_info = platform.linux_distribution() if hasattr(platform, 'linux_distribution') else ('', '', '')
    distro_name, distro_version, distro_id = distro_info
    cpu_temp = psutil.sensors_temperatures().get('coretemp', [{'current': '/' }])
    if cpu_temp and isinstance(cpu_temp[0], dict):
        cpu_temp = cpu_temp[0].get('current', '/')
    else:
        cpu_temp = '/'
    
    gpu_memory = psutil.virtual_memory().total / (1024 ** 3)
    cpu_load = psutil.cpu_percent(interval=1)
    load_avg_str = ' '.join(map(str, os.getloadavg()))
    memory = psutil.virtual_memory()
    ram_info = f"{memory.total / (1024 ** 3):.2f} GB, {memory.percent}% used"

    disk_partitions = [p.device for p in psutil.disk_partitions()]
    network_bandwidth = (
    f"{psutil.net_if_addrs()['eth0'][1].address}"
    if 'eth0' in psutil.net_if_addrs() and len(psutil.net_if_addrs()['eth0']) > 1
    else "[ / ]"
    )
   

    active_connections = len(psutil.net_connections())
    active_processes = len(psutil.pids())
    kernel_modules = ', '.join(get_kernel_modules())
    usb_devices_count = len([d for d in psutil.disk_partitions() if 'usb' in d.device.lower()])
    pci_devices_count = len([p for p in psutil.disk_partitions() if 'pci' in p.device.lower()])
    cron_jobs_count = len(get_scheduled_tasks())

    swap_used = psutil.swap_memory().used / (1024 ** 3)
    swap_free = psutil.swap_memory().free / (1024 ** 3)
    tor_status = checkNet()
    system_uptime = str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))

    dns_servers = get_dns_servers()
    firewall_rules_summary = get_firewall_rules()
    running_services = subprocess.getoutput("systemctl --type=service --state=running").splitlines()
    scheduled_tasks = get_scheduled_tasks()
    
    HEADEROUTPUT = [
        "[ SYSTEM ONLINE ] <> NET::TECH",
        ">>> NETRUNNER_V3.1",
        f"// IADDRESS..........: {ip_address}",
        f"// W_ADDRESS.......: {public_ip}",
        f"// M_ADDRESS.......: {mac_address}",
        f"// CUR_TIME......: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
        f"// RUNNER_ID.........: {hostname}",
        f"// SESSION_KEY.......: {session_key}",
        f"// GET_ACCESSV_SSID......: {get_ssid()}",
        f"// PACCESSV_BSID......: {get_bssid()}",
        f"// SIGNAL............: {signal}% ... CH: {get_channel()}",
        f"// OPEN_PORTS........: {open_ports()}",
        f"// SYS_OS................: {os_info}",
        f"// KERNEL_LH....: {kernel_version}",
        f"// DISTRO............: {distro_name} {distro_version} ({distro_id})",
        f"// NV4_ARCH......: {architecture}",
        f"// CPU_DATA..........: {get_cpu_info()}",
        f"// CPU_TEMP..........: {cpu_temp}°C",
        f"// GPU_DATA........: {get_gpu_info()}",
        f"// GPU_MEMORY........: {gpu_memory} GB",
        f"// DISK_PART...: {', '.join(disk_partitions)}",
        f"// GET_CONNECTIONS.: {active_connections}",
        f"// ACTIVE_PS..: {active_processes}",
        f"// GET_USBDEVICES.......: {usb_devices_count}",
        f"// GET_PCIDEVICES.......: {pci_devices_count}",
        f"// LOAD_DNS.......: {', '.join(dns_servers)}",
        f"// SELINUX_STATUS....: {selinux_status()}",
        f"// FIREWALL_RULES....: {firewall_rules_summary}",
        f"// SCHED_TASKS...: {', '.join(scheduled_tasks)}",
        f"// DARKNET_V2........: {'RUNNING' if checkNet() else 'NOT RUNNING' }",
        f"// RUNNER_UPTIME.....: {system_uptime}",
        "...................................................................."
       
    ]


MENUDK = [
    "[:]|/ RETURN_TO_NODE",
    "[:]|/ CHECK_STATUS",
    "[:]|/ INIT_DARKNET_PROXY",
    "[:]|/ AUTOWIPE_SCHEDULE",
    "[:]|/ ENABLE_ON_BOOT",
    "[:]|/ LOCATE_LOCAL_IP",
    "[:]|/ ALTER_NETWORK_IDENTITY",
    "[:]|/ SPOOF_CHIPSET_MAC",
    "[:]|/ RESTORE_CHIPSET_MAC"
]


MENU1 = [
    "[:]|/ CONNECT_TTY",
    "[:]|/ SYS_LOGS",
    "[:]|/ ACCESS_SERVICES",  
    "[:]|/ NETRUNNER_V4_CONFIG",
    "[:]|/ EXIT_NODE",      
    "[:]|/ RESTART_NR4",
    "[:]|/ POWER_OFF"
]

MENU_SERVICES = [
    "[:]|/ RETURN_TO_NODE",            
    "[:]|/ INIT_DARKNET_PROXY",        
    "[:]|/ LAUNCH_APACHE",       
    "[:]|/ BOOT_MYSQL",                
    "[:]|/ EXECUTE_TOR",       
    "[:]|/ ACTIVATE_UFW"               
]

MENU_OPTIONS = [
    "[:]|/ RETURN_TO_NODE",
    "[:]|/ UPDATE_DB [UPGRADE SEQUENCE]",
    "[:]|/ CONFIGURE_KB_LAYOUT",
    "[:]|/ ENUMERATE_SYSTEM_INFO",
    "[:]|/ RUN_SYS_MONITOR",
    "[:]|/ OPEN_NETWORK_INTERFACE",
    "[:]|/ WIPE_TEMP_FILES",
    "[:]|/ NETSTAT_SCAN [ACTIVE_CONNECTIONS]",
    "[:]|/ RECONFIGURE_HOSTNAME",
    "[:]|/ INIT_CRONJOBS",
    "[:]|/ MONITOR_CRONJOBS"
]



LINHAS_HD = 5
LOGIN_PAUSE = 1000
ELEMNT = '!@#$%^*()_-+={}[]|\\:;\'",<>./?'
LOGIN_TXT = '// NET::TECH SYSTEM INTERFACE v2.7\n// BOOT_SEQUENCE_INITIATED\n// ACCESS_REQUEST\n\n'
BLOQUEIO = 10000000

novaLinha = ord('\n')


# ----------- funcoes --------------------
def draw_matrix(win, matrix, sel_y=None, sel_x=None):
    win.clear()
    win.box()
    for y, row in enumerate(matrix, start=1):
        for x, code in enumerate(row, start=1):
            # calculate cell position
            cx = x * 5  # (4 chars + 1 space)
            cy = y
            if y-1 == sel_y and x-1 == sel_x:
                win.attron(curses.A_REVERSE)
                win.addstr(cy, cx, code)
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(cy, cx, code)
    win.refresh()


def draw_sequence(win, seq):
    win.erase()
    win.box()
    win.addstr(0, 2, " SEQUENCE REQUIRED ")
    for idx, code in enumerate(seq, start=1):
        win.addstr(idx, 2, f"{idx:02d}: {code}")
    win.refresh()


def breach_protocol(scr, matrix, req_seq):
    # hide cursor, enable mouse
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    scr.clear()
    h, w = scr.getmaxyx()
    mid = w // 2

    # carve out two windows
    left = curses.newwin(h-2, mid-2, 1, 1)
    right = curses.newwin(h-2, w-mid-2, 1, mid+1)

    sel = (None, None)
    draw_matrix(left, matrix)
    draw_sequence(right, req_seq)

    while True:
        ch = scr.getch()
        if ch == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            # if the click landed inside the left panel...
            if 1 < mx < mid-1 and 1 < my < h-1:
                # convert to matrix indices
                cell_x = (mx - 1) // 5 - 1
                cell_y = my - 1
                if (0 <= cell_y < len(matrix) and
                    0 <= cell_x < len(matrix[0])):
                    sel = (cell_y, cell_x)
                    # highlight the clicked cell
                    draw_matrix(left, matrix, *sel)

        elif ch in (ord('\n'), 27):  # ENTER or ESC to finish
            break

    # once done, clear and return to main flow
    scr.clear()
    scr.refresh()
    
        
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nUPDATING VAULT SHELL. . . ")
            time.sleep(2)
            os.system('sudo apt update && sudo apt-get upgrade')
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 2:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nROBCO KEYMAPPING CONFIGURATION. . . ")
            time.sleep(2)
            keyboardModelLayout()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 3:  
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nGETTING VAULTPEEK MODULE. . . ")
            vaultpeek()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 4:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nLOADING OVERSEER EYE. . . ")
            time.sleep(2)
            monitor()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 5:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nLOADING NETCORE. . . ")
            time.sleep(2)
            getNmtui()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 6:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nCLEARING ROBCO TEMPORARY LOGS AND FILES. . . ")
            time.sleep(2)
            os.system('sudo apt-get autoremove -y && sudo apt-get clean && sudo apt-get autoclean -y && sudo rm -rf /tmp/* /var/tmp/* /var/cache/apt/archives/* /var/log/*.log && sudo journalctl --vacuum-time=7d')
            print("\n\nALL TEMPORARY DATA DELETED!")
            time.sleep(5)
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 7:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nLOADING PIPSNIFF 3000 ")
            time.sleep(2)
            getNetstat()
            scr.erase()
            options()

        elif keyInput == ord('\n') and selection == 8:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nUPDATING NAMEFORGE . . . ")
            time.sleep(2)
            editHost()
            scr.erase()
            options()


        elif keyInput == ord('\n') and selection == 9:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nSETTING CRONSTART INIT . . . ")
            time.sleep(2)
            createCron()
            scr.erase()
            options()


        elif keyInput == ord('\n') and selection == 10:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            scr.erase()
            menu()

        elif keyInput == ord('\n') and selection == 1:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            scr.erase()
            darknet()

        elif keyInput == ord('\n') and selection == 2:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
    selection_start_x = scr.getyx()[1]
    largura = scr.getmaxyx()[0]
    typeT(scr, "---- NODE: NETWATCH_HKG_CORE ----" + '\n')
    while keyInput != novaLinha:
        scr.move(selection_start_y, selection_start_x)
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\n\n/.F==: ACCESSING VAULT TERMINAL. . .")
            time.sleep(2)
            os.system("clear"); 
            os.system("cat " + os.path.join(dir, 'arasaka') + "| pv -qL 16000 " )
            shutdown_program(scr)

        elif keyInput == ord('\n') and selection == 1:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            servicos()
        elif keyInput == ord('\n') and selection == 3:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            options()
        elif keyInput == ord('\n') and selection == 4:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
               #logout
            lock_screen()
        elif keyInput == ord('\n') and selection == 5:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\n\nREBOOTING ROBCO INDUSTRIES (TM) UNIFIED OPERATIONAL SYSTEM")

            time.sleep(5)
            os.system("sudo shutdown -r now")
        
        elif keyInput == ord('\n') and selection == 6:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            scr.erase()
            servicos()

        if keyInput == ord('\n') and selection == 1:
           print("\n\n- - OVERSEER NETWORK STATUS - -")
           time.sleep(2)
           os.system('sudo torctl status | micro')
           scr.erase()
           darknet()
       
        elif keyInput == ord('\n') and selection == 2:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nACTIVATING AUTOWIPE. . . ")
            time.sleep(2)
            os.system('sudo torctl autowipe')
            scr.erase()
            darknet()

        elif keyInput == ord('\n') and selection == 4:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nACTIVATING AUTO START. . . ")
            time.sleep(2)
            os.system('sudo torctl autostart')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 5:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nFETCHING LOCAL TERMINAL COORDINATES. . . ")
            time.sleep(2)
            os.system('sudo torctl ip | micro ')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 6:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nCHANGE OVERSEER NETWORK IDENTITY. . . ")
            time.sleep(2)
            os.system('sudo torctl chngid')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 7:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nCHANGE OVERSEER NETWORK IDENTITY. . . ")
            time.sleep(2)
            os.system('sudo torctl chngid')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 8:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
            print("\n\nCHANGING LOCAL ROBCO CHIPSET MAC. . . ")
            time.sleep(2)
            os.system('sudo torctl chngmac')
            scr.erase()
            darknet()
        elif keyInput == ord('\n') and selection == 9:
            audio(expand_home("~/.boot/audio/keyenter.wav"))
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

    audio(expand_home("~/.boot/audio/beep.wav"),3)
    for header in HEADEROUTPUT:   
        typeT(scr, header + '\n')
     
    scr.refresh()

    return criarDarknet(scr)



def initMenu(scr):

    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)
    curses.curs_set(0)
    get_system_info()
    largura = scr.getmaxyx()[1]
    
    audio(expand_home("~/.boot/audio/beep.wav"),3)
    for header in HEADEROUTPUT:   
        typeT(scr, header + '\n')
     
    scr.refresh()

    return criarMenu(scr)



def initOptions(scr):

    curses.use_default_colors()
    scr.erase()
    scr.move(0, 0)
    curses.curs_set(0)

    largura = scr.getmaxyx()[1]

    audio(expand_home("~/.boot/audio/beep.wav"),3)
    for header in HEADEROUTPUT:   
        typeT(scr, header + '\n')
     
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


def sInit(scr):

    typeT(scr, '\n\n' + LOGIN_TXT)
    typeT(scr, f"// STATUS: ONLINE\n// MACHINE_INFO: {platform.system()} {platform.release()} ({platform.machine()})\n// CURRENT_USER: {os.getlogin()}\n// HOSTNAME: {socket.gethostname()}\n// IP_ADDRESS: {socket.gethostbyname(socket.gethostname())}\n// MAC_ADDRESS: {get_mac_address()}\n// SYSTEM_TIME_UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n// CPU_USAGE: {get_cpu_usage()}\n// MEMORY_STATUS: {get_memory_usage()}\n// DISK_STATUS: {get_disk_usage()}\n\n// BREACH_PROTOCOL: ACTIVE\n// BREACH_SOURCE: [ARASAKA TERMINAL - 港区, 東京]\n\n// INITIATING PACKET COLLECTION\n>>> COLLECTING_PACKET_1........COMPLETE\n>>> COLLECTING_PACKET_2........COMPLETE\n>>> COLLECTING_PACKET_3........COMPLETE\n>>> COLLECTING_PACKET_4........COMPLETE\n\n// UPLOAD_SEQUENCE\n>>> UPLOAD_IN_PROGRESS\n\n「荒坂インターフェース 」")
    typeT(scr, '')
    # Run breach protocol 
    success = run_breach(scr)
    if not success:
        bloquearTela()
    else:
        typeT(scr,'/// LOADING NETRUNNER_V3.1............\n')
        typeT(scr,'/// BOOT_SEQUENCE INITIATED.........\n')
        menu()
    scr.refresh()

def login_menu(scr):
    curses.use_default_colors()
    scr = scr
    scr.erase()
    breach = sInit(scr)


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
    centr(scr, 'C0NNECTION_TERMINATED__!\nSYSTEM_FAILURE [0x9F37C] //\n\n')
    centr(scr, 'ERROR CODE: 0x5A_X12T | TRACE DETECTED!!\n')    
    scr.refresh()
    curses.napms(BLOQUEIO)
def bloquearTela():
    """
    Initialize curses and start the locked out process
    """
    curses.wrapper(initLock)
def initBoot():

    os.system("cat " + os.path.join(dir, 'arasaka') + "| pv -qL 10000 " )
    return True
    res = curses.wrapper(initLogin)
    return res
def iniciar():
    
    return initBoot()

Lpausa = 3
Ipausa = 50  
delay = 40
mascara = '*'
novaLinha = 10
def playBeep():
    audio(expand_home("~/.boot/audio/beep.wav"))
def playError():
    audio(expand_home("~/.boot/audio/wrongpass.wav"))
def playKey():
    audio(expand_home("~/.boot/audio/keyenter.wav"))
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
    novaLinha = ord('\n')  # ASCII for newline

    try:
        while keyInput != novaLinha:
            keyInput = window.getch()

            # Convert lowercase to uppercase
            if 96 < keyInput < 123:
                keyInput -= 32

            # Handle backspace
            if keyInput == ord('\b'):
                if len(def_string) > 0:
                    def_string = def_string[:-1]
                    cur = window.getyx()
                    window.move(cur[0], cur[1] - 1)
                    window.clrtobot()  # Clear from current cursor to bottom
                else:
                    continue  # Ignore if nothing to delete

            # Ignore keys greater than 255 (extended keys)
            elif keyInput > 255:
                continue

            # Handle regular input (characters)
            elif keyInput != novaLinha:
                def_string += chr(keyInput)
                if hidden:
                    window.addch('*')  # Show a mask (e.g., *) if hidden is True
                else:
                    window.addch(chr(keyInput))  # Show the character normally

            # Handle new line input
            elif can_novaLinha:
                window.addch(novaLinha)

        return def_string

    except ValueError:
        # Handle Unicode characters, if needed, and re-call the login function
        login()  # Or handle as appropriate



def centr(window, text, pause=Lpausa):

    largura = window.getmaxyx()[1]
    window.move(window.getyx()[0], int(largura / 2 - len(text) / 2))
    typeT(window, text, pause)


if __name__ == '__main__':
    globals()[sys.argv[1]]()
