#!/bin/bash
# Coded by:
#     /\                                  | |      
#    /  \   _ __ ___ __ _ _ __   __ _  ___| | ___  
#   / /\ \ | '__/ __/ _` | '_ \ / _` |/ _ \ |/ _ \ 
#  / ____ \| | | (_| (_| | | | | (_| |  __/ | (_) |
# /_/    \_\_|  \___\__,_|_| |_|\__, |\___|_|\___/ 
#  
loading() { #progbar
    local ts=$1 p=0 w=$(($(tput cols) - 10)) fs b pct
    while [ $p -le $ts ]; do
        fs=$((p * w / ts))
        b=$(printf "%0.s#" $(seq 1 $fs))
        b+=$(printf "%0.s-" $(seq 1 $((w - fs))))
        pct=$((p * 100 / ts))
        printf "\r[%s] %d%% " "$b" "$pct"
        sleep 0.1
        p=$((p + 1))
    done
    echo
}
echo "// INSTALLATION_SEQUENCE . . . . . . . . . . . " | pv -qL 45
loading 17
chsh -s $(which zsh)
if ! command -v zsh &> /dev/null; then
  echo "Zsh not found. Installing..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install zsh
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update && sudo apt install -y zsh
  fi
else
  echo "Zsh already installed."
fi
echo ""
clear
sudo apt update -qq > /dev/null 2>&1
echo ">>>> FETCHING NECESSARY MODULES. . . . . . . . " | pv -qL 45
sudo apt-get install gnome-terminal ffmpeg curl wget fonts-powerline zip ufw htop  -y curl > /dev/null 2>&1
loading 10
echo "NET::TECH INTERFACE INSTALLATION. . . . . . . . " | pv -qL 45
sudo apt-get install cool-retro-term git nmtui nmap figlet micro toilet tor python pip3 ffmpeg pv -y curl > /dev/null 2>&1
echo "//////// LOADING CONFIGURATIONS FOR NETRUNNER_V3:TMUX. . . . . . . . . . . . . . . . . . . " | pv -qL 25
echo "[::]> Installing tmux, curl, and zsh..."
sudo apt update && sudo apt install -y tmux curl  gawk net-tools coreutils > /dev/null 2>&1
loading 15
echo "[::]> Writing tmux configuration to ~/.tmux.conf..."
echo "Code added to .zshrc and .bashrc."
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
cat << 'EOF' > ~/.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'o0th/tmux-nova'
set -g @plugin 'yumiriam/tmux-disk'
set -g @plugin 'xamut/tmux-weather'
set -g @plugin 'tmux-plugins/tmux-cpu'
set -g @plugin 'AngryMorrocoy/tmux-neolazygit'
set -g @plugin 'xamut/tmux-network-bandwidth'
set -g @nova-segment-time "󱇏 #H | #(date +'%H:%M') 󰄾"
set -g @nova-segment-time-colors "#000000 #ff0000"
set -g status-interval 60
set-option -g @tmux-weather-interval 5
set-option -g @tmux-weather-format "  %t+%w"
set -g @nova-segment-weather "     #{weather}/ "
set -g @nova-segment-weather-colors "#000000 #ff0000"
set -g @disk_mount_point "/"
set -g @nova-segment-disk " #{disk_available}b/ "
set -g @nova-segment-disk-colors "#000000 #ff0000"
set -g @nova-segment-cpu " CPU: #{cpu_percentage}/ "
set -g @nova-segment-cpu-colors "#000000 #ff0000"
set -g @nova-segment-ram " RAM: #{ram_percentage}/ "
set -g @nova-segment-ram-colors "#000000 #ff0000"
set -g @nova-segment-net " #{network_bandwidth}/ "
set -g @nova-segment-net-colors "#000000 #ff0000"
set -g @nova-nerdfonts true
set -g @nova-pane-active-border-style "#44475a"
set -g @nova-pane-border-style "#282a36"
set -g @nova-status-style-bg 'default'
set -g @nova-status-style-fg '#000000'
set -g @nova-status-style-active-bg "#000000"
set -g @nova-status-style-active-fg "#ff0000"
set -g @nova-status-style-double-bg "#ff6666"
set -g window-style 'fg=colour247,bg=#00ff00'
set -g window-active-style 'fg=colour250,bg=black'
set -g @nova-pane-active-border-style "#ffa500"
set -g @nova-pane-border-style "#282a36"
set -g window-status-style "bg=default,fg=default"
set -g window-status-current-style "bg=default,fg=default"
set -g @nova-pane-border-style "#ffa500"
set -g @nova-pane "#I#{?pane_in_mode,  #{pane_mode},}  #W"
set -g @nova-segment-mode "#{?client_prefix,󰋘,󰋙} |"
set -g @nova-segment-mode-colors "#000000 #ff0000"
set -g @nova-segment-whoami "󰛡 NETRUNNER_V3"
set -g @nova-segment-whoami-colors "#000000 #ff0000"
set -g status-right-length 300
set -g @nova-rows 0
set -g @nova-segments-0-left "mode time"
set -g @nova-segments-0-right "weather disk cpu ram net whoami"
run '~/.tmux/plugins/tpm/tpm'
EOF
loading 12
echo "[::]> PIP_INSTALL" | pv -qL 25
pip install wifi psutil --break-system-packages
echo "" 
echo "" 
echo "" 
echo "" 
echo "[::]> Appending tmux autostart to ~/.bashrc and ~/.zshrc..." | pv -qL 25
ALIAS="alias menu='python3 \$HOME/.boot/boot.py firstMenu'"
TMUX_START='
if command -v tmux &>/dev/null && [ -z "$TMUX" ]; then
  tmux has-session -t main 2>/dev/null
  if [ $? -eq 0 ]; then
    tmux attach-session -t main
  else
    tmux new-session -s main -d "python3 /root/.boot/init.py"
    tmux attach-session -t main
  fi
fi
'
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  grep -qxF "$ALIAS" "$rc" || echo "$ALIAS" >> "$rc"
  echo "$TMUX_START" >> "$rc"
done
loading 16
sleep 4
echo "" 
echo "//// [✓] COMPLETED"
sleep 3
clear
FILES_ALIAS="alias files='files'"
DISK_ALIAS="alias disk='echo -e \"CURRENT FILE SYSTEM FOR [\$(uname -o), \$(hostname)]\\n\" && df -hT | awk '\''NR==1{print \"Filesystem :: Type :: Size :: Used :: Avail :: Mounted on\"; print \"___________________________________________________\"} NR>1{print \$1 \" :: \" \$2 \" :: \" \$3 \" :: \" \$4 \" :: \" \$5 \" :: \" \$7}'\'''"
PORTS_ALIAS="alias ports='ss -tuln'"
WEATT="alias weather='curl wttr.in/\?d'"
UPDATES_ALIAS="alias updates='sudo apt update && sudo apt list --upgradable'"
UPGRADES_ALIAS="alias netupgrade='sudo apt update && sudo apt-get upgrade -y '"
IPINFO_ALIAS="alias ipinfo='echo Local IP: \$(hostname -I) && echo Public IP: \$(curl -s ifconfig.me)'"
UPTIME_ALIAS="alias uptimeinfo='uptime -p && uptime'"
PSG_ALIAS="alias psg='ps aux | grep -v grep | grep -i'"
EXTRACT_FUNC="
extract () {
    if [ -f \"\$1\" ]; then
        case \"\$1\" in
            *.tar.bz2)   tar xvjf \"\$1\"    ;;
            *.tar.gz)    tar xvzf \"\$1\"    ;;
            *.tar.xz)    tar xvJf \"\$1\"    ;;
            *.bz2)       bunzip2 \"\$1\"     ;;
            *.rar)       unrar x \"\$1\"     ;;
            *.gz)        gunzip \"\$1\"      ;;
            *.tar)       tar xvf \"\$1\"     ;;
            *.tbz2)      tar xvjf \"\$1\"    ;;
            *.tgz)       tar xvzf \"\$1\"    ;;
            *.zip)       unzip \"\$1\"       ;;
            *.Z)         uncompress \"\$1\"  ;;
            *.7z)        7z x \"\$1\"        ;;
            *)           echo \"Don't know how to extract '\$1'...\" ;;
        esac
    else
        echo \"'\$1' is not a valid file!\"
    fi
}
"

TARGET_FILES=(~/.bashrc ~/.zshrc)
add_aliases() {
    for target in "${TARGET_FILES[@]}"; do
        if [ -f "$target" ]; then
            {
                echo ""
                echo "# === Custom Aliases Installation ==="

                echo "$FILES_ALIAS"
                echo "$WEATT"            
                echo "$DISK_ALIAS"
                echo "$PORTS_ALIAS"
                echo "$UPGRADES_ALIAS"
                echo "$UPDATES_ALIAS"
                echo "$IPINFO_ALIAS"
                echo "$UPTIME_ALIAS"
                echo "$PSG_ALIAS"
                echo "$EXTRACT_FUNC"
            } >> "$target"
            echo "Added aliases to $target"
        fi
    done
}

add_aliases
loading 12 
sleep 3
echo "//// [✓] COMPLETED"
clear 
[ ! -d "$HOME/.boot" ] && mkdir -p "$HOME/.boot"
for item in *; do
  [ -d "$item" ] && cp -r "$item" "$HOME/.boot/" || cp "$item" "$HOME/.boot/"
done

if [[ "$SHELL" == *"zsh"* ]]; then
  RC_FILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
  RC_FILE="$HOME/.bashrc"
else
  exit 1
fi

mkdir -p ~/.local/share/fonts
[ ! -f ~/.local/share/fonts/starwars.flf ] && curl -o ~/.local/share/fonts/starwars.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/starwars.flf
[ ! -f ~/.local/share/fonts/Doom.flf ] && curl -o ~/.local/share/fonts/Doom.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/Doom.flf
echo "///// SETTING PATH " | pv -qL 30
echo ""
loading 10
echo ""
echo ""
cd $HOME
echo "[::]> INSTALLING DEPENDENCIES AND TOOLS. . . . . . . .   " | pv -qL 60
echo ""
echo ""
loading 10
wget https://github.com/JohnMcLaren/torctl-bridged/releases/download/torctl-bridged/torctl-bridged_0.5.7-1_amd64.deb
sudo apt install $HOME/torctl-bridged_0.5.7-1_amd64.deb
git clone https://github.com/ARCANGEL0/EzyMap.git $HOME/.local/EzyMap
cd $HOME/.local/EzyMap 
echo "Installing..."
echo "Updating package lists..."
sudo apt-get update -qq > /dev/null 2>&1
echo "Installing curl..."
sudo apt-get install -y curl > /dev/null 2>&1
echo "Installing nmap..."
sudo apt-get install -y nmap > /dev/null 2>&1
loading 45
mkdir -p ~/.local/share/fonts
[ ! -f ~/.local/share/fonts/starwars.flf ] && curl -o ~/.local/share/fonts/starwars.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/starwars.flf
[ ! -f ~/.local/share/fonts/Doom.flf ] && curl -o ~/.local/share/fonts/Doom.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/Doom.flf
sudo systemctl stop tor
echo ""
loading 20
figlet -f ~/.local/share/fonts/starwars.flf "EzyMap"
sudo cp ezymap ~/.local/bin/
SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" == "bash" ]; then
  echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc
elif [ "$SHELL_NAME" == "zsh" ]; then
  echo "export PATH=\$PATH:$(pwd)" >> ~/.zshrc
else
  sudo cp ezymap /usr/bin/
fi
cd $HOME;
clear    
sleep 5 
echo " "
echo " "
echo " "
loading 50
sleep 5
clear
echo ""
echo "/// [≜]:INSTALLING_TERMINAL_UI" | pv -qL 65
grep 'alias crterm="cool-retro-term --fullscreen --profile 'Futuristic' &"' ~/.zshrc || echo 'alias crterm="cool-retro-term --fullscreen --profile 'Futuristic' &"' >> ~/.zshrc; grep -qxF 'alias crterm="cool-retro-term --fullscreen --profile 'Futuristic' &"' ~/.bashrc || echo 'alias crterm="cool-retro-term --fullscreen --profile 'Futuristic' &"' >> ~/.bashrc
loading 40
sleep 5
echo "/// [✔]:TASK_COMPLETED" | pv -qL 45
echo ">>> Type crterm on any terminal to boot NETRUNNER or start by CRT desktop app." | pv -qL 20
echo ">>> Type 'menu' anywhere to open NETRUNNER menu" | pv -qL 20
clear
cp $HOME/.boot/arasakaUI.json $HOME/arasakaUI.json
figlet -f ~/.local/share/fonts/starwars.flf "NET::TECH"
echo "// NETRUNNER_V3:BOOT_SEQUENCE " | pv -qL 45
echo "// INSTALLED_SUCCESSFULLY_[✔]" | pv -qL 45
echo " "
echo " "
cd $HOME
read -n 1 -s -r -p "Press any key to restart your shell...".
cd $HOME;
cool-retro-term --fullscreen --profile 'Futuristic'
clear 
PPPID=$(awk '{print $4}' "/proc/$PPID/stat")
kill $PPPID


