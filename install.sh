#!/bin/bash
echo "// INSTALLATION_SEQUENCE . . . . . . . . . . . " | pv -qL 45
echo ""
clear
sudo apt update -qq > /dev/null 2>&1
echo ">>>> FETCHING NECESSARY MODULES. . . . . . . . " | pv -qL 45
sudo apt-get install gnome-terminal ffmpeg curl wget zip htop  -y curl > /dev/null 2>&1
echo "NET::TECH INTERFACE INSTALLATION. . . . . . . . " | pv -qL 45
sudo apt-get install git nmtui nmap figlet micro toilet tor python pip3 ffmpeg pv -y curl > /dev/null 2>&1
pip3 install -r requirements.txt --break-system-packages
echo "//////// LOADING CONFIGURATIONS FOR NETRUNNER_V3:TMUX. . . . . . . . . . . . . . . . . . . " | pv -qL 25
sudo apt install -y tmux curl zsh > /dev/null 2>&1
echo "set -g @plugin 'tmux-plugins/tpm'\nset -g @plugin 'o0th/tmux-nova'\nset -g @plugin 'yumiriam/tmux-disk'\nset -g @plugin 'xamut/tmux-weather'\nset -g @plugin 'tmux-plugins/tmux-cpu'\nset -g mouse on\nset -g @plugin 'AngryMorrocoy/tmux-neolazygit'\nset -g @plugin 'xamut/tmux-network-bandwidth'\n\nWEATHER='#(curl -s wttr.in/London:Stockholm:Moscow?format=%25l:+%25c%20%25t%60%25w&period=60)'\nset -g @nova-segment-time \"󱇏 #H | #(date +'%H:%M') 󰄾\"\nset -g @nova-segment-time-colors \"#000000 #ff0000\"\nset -g status-interval 60\n\nset-option -g @tmux-weather-interval 5\nset-option -g @tmux-weather-format \"  %t+%w\"\nset -g @nova-segment-weather \"     #{weather}/ \"\nset -g @nova-segment-weather-colors \"#000000 #ff0000\"\n\nset -g @disk_mount_point \"/\"\nset -g @nova-segment-disk \" #{disk_available}b/ \"\nset -g @nova-segment-disk-colors \"#000000 #ff0000\"\n\nset -g @nova-segment-cpu \" CPU: #{cpu_percentage}/ \"\nset -g @nova-segment-cpu-colors \"#000000 #ff0000\"\n\nset -g @nova-segment-ram \" RAM: #{ram_percentage}/ \"\nset -g @nova-segment-ram-colors \"#000000 #ff0000\"\n\nset -g @nova-segment-net \" #{network_bandwidth}/ \"\nset -g @nova-segment-net-colors \"#000000 #ff0000\"\n\nset -g @nova-nerdfonts true\n\nset -g @nova-pane-active-border-style \"#44475a\"\nset -g @nova-pane-border-style \"#282a36\"\nset -g @nova-status-style-bg 'default'\nset -g @nova-status-style-fg '#000000'\nset -g @nova-status-style-active-bg \"#000000\"\nset -g @nova-status-style-active-fg \"#ff0000\"\nset -g @nova-status-style-double-bg \"#ff6666\"\nset -g window-style 'fg=colour247,bg=#00ff00'\nset -g window-active-style 'fg=colour250,bg=black'\n\nset -g @nova-pane-active-border-style \"#ffa500\"\nset -g @nova-pane-border-style        \"#282a36\"\n\nset -g window-status-style         \"bg=default,fg=default\"\nset -g window-status-current-style \"bg=default,fg=default\"\nset -g @nova-pane-border-style \"#ffa500\"\n\nset -g @nova-pane \"#I#{?pane_in_mode,  #{pane_mode},}  #W\"\n\nset -g @nova-segment-mode \"#{?client_prefix,󰋘,󰋙} |\"\nset -g @nova-segment-mode-colors \"#000000 #ff0000\"\nset -g @nova-segment-whoami \"󰛡 NETRUNNER_V3\"\nset -g @nova-segment-whoami-colors \"#000000 #ff0000\"\nset -g status-right-length 300\nset -g @nova-rows 0\nset -g @nova-segments-0-left \"mode time\"\nset -g @nova-segments-0-right \"weather disk cpu ram net whoami\"\n\nrun '~/.tmux/plugins/tpm/tpm'" > ~/.tmux.conf && echo "if command -v tmux >/dev/null 2>&1; then\n  [ -z \"\$TMUX\" ] && exec tmux\nfi" >> ~/.bashrc && echo "if command -v tmux >/dev/null 2>&1; then\n  [ -z \"\$TMUX\" ] && exec tmux\nfi" >> ~/.zshrc
blh=30
fc="█"
xc="░"
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
for ((i = 1; i <= blh; i++)); do
    filled=$(printf "%*s" "$i" | tr ' ' "$fc")
    empty=$(printf "%*s" "$((blh - i))" | tr ' ' "$xc")
    printf "\r[%s%s]" "$filled" "$empty"
    sleep 0.07
done
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
figlet -f ~/.local/share/fonts/starwars.flf "NET::TECH"
echo "NET::TECH UI BOOT SCRIPT INSTALLED SUCCESSFULLY ✔" | pv -qL 45
echo " "
echo " "
cd $HOME
read -n 1 -s -r -p "Press any key to restart your shell..."
clear 
cd $HOME;
