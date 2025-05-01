#!/bin/bash
loading() {
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
loading 60
echo ""
clear
sudo apt update -qq > /dev/null 2>&1
echo ">>>> FETCHING NECESSARY MODULES. . . . . . . . " | pv -qL 45
sudo apt-get install gnome-terminal ffmpeg curl wget zip htop  -y curl > /dev/null 2>&1
loading 10
echo "NET::TECH INTERFACE INSTALLATION. . . . . . . . " | pv -qL 45
sudo apt-get install git nmtui nmap figlet micro toilet tor python pip3 ffmpeg pv -y curl > /dev/null 2>&1
pip3 install -r requirements.txt --break-system-packages
echo "//////// LOADING CONFIGURATIONS FOR NETRUNNER_V3:TMUX. . . . . . . . . . . . . . . . . . . " | pv -qL 25


echo "[::]> Installing tmux, curl, and zsh..."
sudo apt update && sudo apt install -y tmux curl zsh > /dev/null 2>&1
loading 70
echo "[::]> Writing tmux configuration to ~/.tmux.conf..."

cat << 'EOF' > ~/.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'o0th/tmux-nova'
set -g @plugin 'yumiriam/tmux-disk'
set -g @plugin 'xamut/tmux-weather'
set -g @plugin 'tmux-plugins/tmux-cpu'
set -g mouse on
set -g @plugin 'AngryMorrocoy/tmux-neolazygit'
set -g @plugin 'xamut/tmux-network-bandwidth'

WEATHER='#(curl -s wttr.in/London:Stockholm:Moscow?format=%25l:+%25c%20%25t%60%25w&period=60)'

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
loading 20
echo "[::]> Appending tmux autostart to ~/.bashrc and ~/.zshrc..."

for rc in ~/.bashrc ~/.zshrc; do
  grep -qxF '[ -z "$TMUX" ] && exec tmux' "$rc" || \
    echo -e '\nif command -v tmux >/dev/null 2>&1; then\n  [ -z "$TMUX" ] && exec tmux\nfi' >> "$rc"
done
loading 20
sleep 4
echo "" 
echo "[✓] Setup complete."

sleep 3
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

loading 70

echo ""
grep -q "tmux" "$RC_FILE" || echo "tmux" >> "$RC_FILE"

grep -q "python $HOME/.boot/init.py" "$RC_FILE" || echo "python $HOME/.boot/init.py" >> "$RC_FILE"
echo ""


cd $HOME
echo "[::]> INSTALLING DEPENDENCIES AND TOOLS. . . . . . . .   " | pv -qL 60

for ((i = 1; i <= blh; i++)); do
    filled=$(printf "%*s" "$i" | tr ' ' "$fc")
    empty=$(printf "%*s" "$((blh - i))" | tr ' ' "$xc")
    printf "\r[%s%s]" "$filled" "$empty"
    sleep 0.07
done
echo ""
echo ""
loading 50
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
for i in {1..5}; do
  echo -n "Loading"
  for j in {1..3}; do
    echo -n "."
    sleep 0.5
  done
  echo ""
done

echo ""
loading 60
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
loading 100
sleep 5
clear
figlet -f ~/.local/share/fonts/starwars.flf "NET::TECH"
echo "NET::TECH UI BOOT SCRIPT INSTALLED SUCCESSFULLY ✔" | pv -qL 45
echo " "
echo " "
cd $HOME
read -n 1 -s -r -p "Press any key to restart your shell..."
clear 
cd $HOME;
