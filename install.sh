#!/bin/bash
echo "// INSTALLATION_SEQUENCE . . . . . . . . . . . " | pv -qL 45
echo ""
clear
sudo apt update -qq > /dev/null 2>&1
sudo apt-get install curl wget zip git nmap figlet toilet tor python pip3 ffmpeg pv -y curl > /dev/null 2>&1
echo ">>>> FETCHING NECESSARY MODULES. . . . . . . . " | pv -qL 45
sudo apt-get install gnome-terminal ffmpeg
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
cl30

echo "///// SETTING PATH " | pv -qL 30
echo ""
echo ""
grep -q "python $HOME/.boot/init.py" "$RC_FILE" || echo "python $HOME/.boot/init.py" >> "$RC_FILE"
echo ""


cd $HOME
echo "[::]> INSTALLING DEPENDENCIES AND TOOLS. . . . . . . .   " | pv -qL 60
echo ""
echo ""
sudo systemctl stop tor
wget https://github.com/JohnMcLaren/torctl-bridged/releases/download/torctl-bridged/torctl-bridged_0.5.7-1_amd64.deb
sudo apt install $HOME/torctl-bridged_0.5.7-1_amd64.deb

git clone https://github.com/ARCANGEL0/EzyMap.git $HOME/.local/EzyMap
cd $HOME/.local/EzyMap 
chmod +x install.sh
sudo ./install.sh 
cd $HOME;
clear    
sleep 5 
echo " "
echo " "
echo " "
echo "NET::TECH UI BOOT SCRIPT INSTALLED SUCCESSFULLY ✔" | pv -qL 45
echo " "
echo " "
echo " "
sleep 5
clear 
cd $HOME;
tmux
